"""Cycle de vie des comptes : inscription, connexion, validation, blocage,
réinitialisation de mot de passe.

Les règles qui portent un enjeu de sécurité sont ici, et nulle part ailleurs :
les routes ne font que traduire les exceptions levées en codes HTTP.

Deux principes traversent le module :

* **Ne jamais révéler l'existence d'un compte.** Un login, une demande de
  réinitialisation et une inscription répondent tous de la même façon pour une
  adresse inconnue, sinon la page de connexion devient un oracle permettant de
  lister les médecins inscrits.
* **Un compte en attente ou bloqué n'a pas de session.** Le contrôle est fait à
  la connexion *et* à chaque requête, de sorte qu'un blocage prend effet
  immédiatement sur les sessions déjà ouvertes.
"""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.models.compte import Compte, DemandeReinitialisation
from app.models.enums import RoleCompte, StatutCompte, StatutDemandeReinit
from app.models.medecin import Medecin
from app.schemas.auth import describe_password_errors, failed_password_rules
from app.services import securite

# Message unique pour toute défaillance d'identifiants. Deux messages
# distincts (« compte inconnu » / « mot de passe faux ») permettraient d'énumérer
# les comptes existants.
ERREUR_IDENTIFIANTS = "Email ou mot de passe incorrect."


def _maintenant() -> datetime:
    return datetime.now(timezone.utc)


def _verifier_mot_de_passe(mot_de_passe: str) -> None:
    """Applique la politique de mot de passe, ou refuse avec le détail manquant."""
    echecs = failed_password_rules(mot_de_passe)
    if echecs:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=describe_password_errors(mot_de_passe),
        )


def normaliser_email(email: str) -> str:
    """Minuscules + espaces autour retirés.

    Sans cela `Sofiane.Benali@chu.dz` et `sofiane.benali@chu.dz` créeraient deux
    comptes distincts pour la même personne, et le second serait refusé à tort
    (« email déjà utilisé ») alors que c'est le premier qui s'est trompé de
    casse.
    """
    return (email or "").strip().lower()


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------


def inscrire_medecin(db: Session, payload) -> Compte:
    """Crée un compte médecin **en attente de validation**.

    Aucun profil `medecin` n'est créé ici : il le sera à l'acceptation. C'est
    ce qui garantit qu'un compte non validé ne peut pas se connecter, et donc
    qu'aucun dossier patient ne peut lui être rattaché avant validation.
    """
    email = normaliser_email(payload.email)
    if db.query(Compte).filter(func.lower(Compte.email) == email).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cette adresse email.",
        )

    _verifier_mot_de_passe(payload.password)

    compte = Compte(
        email=email,
        mot_de_passe_hash=securite.hacher_mot_de_passe(payload.password),
        role=RoleCompte.medecin,
        statut=StatutCompte.en_attente,
        nom=payload.nom.strip(),
        prenom=payload.prenom.strip(),
        telephone=(payload.telephone or "").strip() or None,
        hopital=(payload.hopital or "").strip() or None,
    )
    db.add(compte)
    db.commit()
    db.refresh(compte)
    return compte


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------


def _compte_par_email(db: Session, email: str) -> Compte | None:
    return db.query(Compte).filter(func.lower(Compte.email) == normaliser_email(email)).first()


def _refuser_jeton() -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ERREUR_IDENTIFIANTS,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _enregistrer_echec(db: Session, compte: Compte) -> None:
    """Compte un échec et verrouille le compte si le seuil est atteint.

    Le verrouillage est indispensable dès lors qu'il n'y a ni CAPTCHA ni
    notification : un mot de passe court se devine en quelques centaines
    d'essais, et rien n'autre ne stopperait l'énumération.
    """
    compte.tentatives_echouees = (compte.tentatives_echouees or 0) + 1
    if compte.tentatives_echouees >= settings.MAX_TENTATIVES_CONNEXION:
        compte.verrouille_jusqu_a = _maintenant() + timedelta(
            minutes=settings.DUREE_VERROUILLAGE_MINUTES
        )
        compte.tentatives_echouees = 0
    db.commit()


def _verrouille(compte: Compte) -> bool:
    echeance = compte.verrouille_jusqu_a
    if echeance is None:
        return False
    if echeance.tzinfo is None:
        # Postgres renvoie un timestamptz, mais SQLite (tests) un datetime
        # naïf : sans cette conversion, la comparaison lèverait TypeError.
        echeance = echeance.replace(tzinfo=timezone.utc)
    return echeance > _maintenant()


def connecter(db: Session, email: str, mot_de_passe: str) -> tuple[Compte, str]:
    """Authentifie un compte et renvoie `(compte, jeton)`.

    L'ordre des vérifications est délibéré : le contrôle de statut n'a lieu
    qu'après validation du mot de passe. Dans l'autre ordre, un attaquant
    pourrait distinguer « compte existant mais en attente » de « compte
    inexistant » sans jamais connaître le mot de passe.
    """
    compte = _compte_par_email(db, email)
    if compte is None:
        _refuser_jeton()

    if _verrouille(compte):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "Compte temporairement verrouillé après plusieurs tentatives "
                f"infructueuses. Réessayez dans {settings.DUREE_VERROUILLAGE_MINUTES} minutes."
            ),
        )

    if not securite.verifier_mot_de_passe(mot_de_passe, compte.mot_de_passe_hash):
        _enregistrer_echec(db, compte)
        _refuser_jeton()

    if compte.statut is StatutCompte.en_attente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Votre compte est en attente de validation par l'administration. "
                "Vous pourrez vous connecter dès son acceptation."
            ),
        )

    if compte.statut is StatutCompte.bloque:
        motif = f" Motif : {compte.motif_blocage}" if compte.motif_blocage else ""
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Votre compte a été bloqué par l'administration.{motif}",
        )

    compte.tentatives_echouees = 0
    compte.verrouille_jusqu_a = None
    compte.date_derniere_connexion = _maintenant()
    db.commit()

    jeton = securite.creer_jeton_session(compte.id_compte, compte.role.value)
    return compte, jeton


# ---------------------------------------------------------------------------
# Mot de passe oublié
# ---------------------------------------------------------------------------


def demander_reinitialisation(db: Session, email: str) -> DemandeReinitialisation | None:
    """Ouvre une demande de réinitialisation, ou ne renvoie rien.

    Le silence sur une adresse inconnue est volontaire : répondre « aucun
    compte » confirmerait au visiteur qu'il ne s'est pas trompé d'adresse.
    Seuls les comptes **actifs** sont concernés — un compte bloqué ou en
    attente doit passer par l'admin, pas par cette procédure.
    """
    compte = _compte_par_email(db, email)
    if compte is None or compte.statut is not StatutCompte.actif:
        return None

    # Une seule demande ouverte à la fois : relancer la procédure depuis le
    # formulaire ne doit pas empiler des lignes que l'admin traiterait à
    # l'aveugle.
    demande = (
        db.query(DemandeReinitialisation)
        .filter(
            DemandeReinitialisation.id_compte == compte.id_compte,
            DemandeReinitialisation.statut == StatutDemandeReinit.en_attente,
        )
        .order_by(DemandeReinitialisation.id_demande.desc())
        .first()
    )
    if demande is None:
        demande = DemandeReinitialisation(
            id_compte=compte.id_compte,
            statut=StatutDemandeReinit.en_attente,
        )
        db.add(demande)
    else:
        # Relance explicite du médecin : on repart d'une demande vierge.
        demande.jeton_hash = None
        demande.expire_le = None
        demande.date_traitement = None
        demande.traite_par = None

    db.commit()
    db.refresh(demande)
    return demande


def reinitialiser_mot_de_passe(db: Session, jeton: str, nouveau_mot_de_passe: str) -> None:
    """Applique un nouveau mot de passe à partir du jeton délivré par l'admin.

    Renvoie toujours 200 à l'appelant (une exception est levée en cas de jeton
    invalide, mais *sans* préciser si le jeton a existé) : la page de
    réinitialisation ne doit pas devenir un moyen de tester des jetons.
    """
    _verifier_mot_de_passe(nouveau_mot_de_passe)

    empreinte = securite.hacher_jeton(jeton or "")
    demande = (
        db.query(DemandeReinitialisation)
        .filter(
            DemandeReinitialisation.jeton_hash == empreinte,
            DemandeReinitialisation.statut == StatutDemandeReinit.en_attente,
        )
        .order_by(DemandeReinitialisation.id_demande.desc())
        .first()
    )
    if demande is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lien de réinitialisation invalide ou déjà utilisé.",
        )

    expiration = demande.expire_le
    if expiration is not None:
        if expiration.tzinfo is None:
            expiration = expiration.replace(tzinfo=timezone.utc)
        if expiration < _maintenant():
            demande.statut = StatutDemandeReinit.annulee
            demande.date_traitement = _maintenant()
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lien de réinitialisation expiré. Demandez-en un nouveau à l'administration.",
            )

    compte = db.get(Compte, demande.id_compte)
    if compte is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lien de réinitialisation invalide.",
        )

    compte.mot_de_passe_hash = securite.hacher_mot_de_passe(nouveau_mot_de_passe)
    compte.doit_changer_mdp = False
    compte.tentatives_echouees = 0
    compte.verrouille_jusqu_a = None

    # Le jeton est à usage unique : la demande passe en « traitée », donc ce
    # lien ne pourra pas être rejoué même s'il est intercepté.
    demande.statut = StatutDemandeReinit.traitee
    demande.jeton_hash = None
    demande.date_traitement = _maintenant()
    db.commit()


def changer_mot_de_passe(
    db: Session, compte: Compte, ancien: str, nouveau: str
) -> None:
    """Change le mot de passe du compte connecté, après vérification de l'ancien.

    Indispensable quand l'admin a posé un mot de passe provisoire : c'est le
    seul moyen pour le médecin de s'en dégager sans repasser par lui.
    """
    if not securite.verifier_mot_de_passe(ancien, compte.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect.",
        )
    if ancien == nouveau:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Le nouveau mot de passe doit être différent de l'ancien.",
        )

    _verifier_mot_de_passe(nouveau)
    compte.mot_de_passe_hash = securite.hacher_mot_de_passe(nouveau)
    compte.doit_changer_mdp = False
    db.commit()


# ---------------------------------------------------------------------------
# Actions du super admin
# ---------------------------------------------------------------------------


def exiger_compte(db: Session, id_compte: int) -> Compte:
    compte = db.get(Compte, id_compte)
    if compte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compte {id_compte} introuvable.",
        )
    return compte


def accepter_compte(db: Session, id_compte: int, admin: Compte) -> Compte:
    """Valide un compte en attente : il devient actif et reçoit son profil.

    C'est l'étape qui crée la ligne `medecin` : tant qu'elle n'existe pas, le
    compte n'a aucun accès clinique, seulement l'accès à la plateforme.
    """
    compte = exiger_compte(db, id_compte)

    if compte.role is RoleCompte.super_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte d'administration ne peut pas passer par la validation.",
        )
    if compte.statut is StatutCompte.actif:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce compte est déjà actif.",
        )

    if compte.id_medecin is None:
        medecin = (
            db.query(Medecin)
            .filter(func.lower(Medecin.email) == compte.email)
            .first()
        )
        if medecin is None:
            medecin = Medecin(
                nom=compte.nom,
                prenom=compte.prenom,
                email=compte.email,
                telephone=compte.telephone or "",
                hopital=compte.hopital or "",
            )
            db.add(medecin)
            db.flush()
        compte.id_medecin = medecin.id_medecin

    compte.statut = StatutCompte.actif
    compte.date_activation = _maintenant()
    compte.active_par = admin.id_compte
    compte.motif_blocage = None
    compte.tentatives_echouees = 0
    compte.verrouille_jusqu_a = None
    db.commit()
    db.refresh(compte)
    return compte


def bloquer_compte(db: Session, id_compte: int, admin: Compte, motif: str | None) -> Compte:
    """Bloque un compte : il ne peut plus se connecter, ses sessions cessent.

    Un compte d'administration ne peut pas être bloqué : il n'existe aucun
    super admin de secours pour le débloquer, et la plateforme resterait sans
    personne pour gérer les comptes.
    """
    compte = exiger_compte(db, id_compte)

    if compte.role is RoleCompte.super_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte d'administration ne peut pas être bloqué.",
        )
    if compte.id_compte == admin.id_compte:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vous ne pouvez pas bloquer votre propre compte.",
        )
    if compte.statut is StatutCompte.bloque:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce compte est déjà bloqué.",
        )

    compte.statut = StatutCompte.bloque
    compte.motif_blocage = (motif or "").strip() or None
    # Les demandes en attente d'un compte bloqué n'ont plus d'objet : sans
    # cela l'admin gérerait des demandes impossibles à satisfaire.
    for demande in db.query(DemandeReinitialisation).filter(
        DemandeReinitialisation.id_compte == compte.id_compte,
        DemandeReinitialisation.statut == StatutDemandeReinit.en_attente,
    ):
        demande.statut = StatutDemandeReinit.annulee
        demande.date_traitement = _maintenant()
        demande.traite_par = admin.id_compte

    db.commit()
    db.refresh(compte)
    return compte


def debloquer_compte(db: Session, id_compte: int) -> Compte:
    """Remet un compte bloqué en service.

    Le compte redevient actif s'il l'avait été avant le blocage (donc conserve
    ses dossiers), et doit sinon repasser par la validation : on ne redonne
    pas un accès clinique à un compte qui n'a jamais été accepté.
    """
    compte = exiger_compte(db, id_compte)
    if compte.statut is not StatutCompte.bloque:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce compte n'est pas bloqué.",
        )

    compte.motif_blocage = None
    compte.tentatives_echouees = 0
    compte.verrouille_jusqu_a = None
    compte.statut = (
        StatutCompte.actif if compte.date_activation is not None else StatutCompte.en_attente
    )
    db.commit()
    db.refresh(compte)
    return compte


def definir_mot_de_passe_temporaire(
    db: Session, id_compte: int, nouveau: str
) -> Compte:
    """L'admin impose un mot de passe, que le médecin devra changer ensuite.

    Complément du lien à usage unique : utile quand le médecin ne peut pas
    utiliser le lien (pas de smartphone, appel à passer). `doit_changer_mdp`
    garantit que le mot de passe connu de l'admin ne reste pas le mot de
    passe définitif.
    """
    _verifier_mot_de_passe(nouveau)
    compte = exiger_compte(db, id_compte)
    if compte.role is RoleCompte.super_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Le mot de passe d'un compte d'administration ne peut pas être défini ici.",
        )

    compte.mot_de_passe_hash = securite.hacher_mot_de_passe(nouveau)
    compte.doit_changer_mdp = True
    compte.tentatives_echouees = 0
    compte.verrouille_jusqu_a = None
    db.commit()
    db.refresh(compte)
    return compte


def generer_lien_reinitialisation(db: Session, id_compte: int, admin: Compte) -> tuple[str, DemandeReinitialisation]:
    """Émet un jeton de réinitialisation pour un compte et renvoie le lien.

    Le jeton en clair n'est renvoyé qu'ici, une seule fois : la base ne
    conserve que son empreinte. L'admin doit donc le transmettre au médecin
    immédiatement ; s'il le perd, il en génère un nouveau.
    """
    compte = exiger_compte(db, id_compte)

    # Un lien pour un compte bloqué ne servirait à rien : le mot de passe serait
    # changé mais la connexion resterait refusée. Mieux vaut renvoyer l'admin
    # vers « Débloquer », qui est l'action qui débloque réellement le médecin.
    if compte.statut is not StatutCompte.actif:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Ce compte n'est pas actif : un lien de réinitialisation ne lui "
                "donnerait pas accès. Utilisez « Débloquer » ou « Valider »."
            ),
        )

    demande = (
        db.query(DemandeReinitialisation)
        .filter(
            DemandeReinitialisation.id_compte == compte.id_compte,
            DemandeReinitialisation.statut == StatutDemandeReinit.en_attente,
        )
        .order_by(DemandeReinitialisation.id_demande.desc())
        .first()
    )
    if demande is None:
        demande = DemandeReinitialisation(id_compte=compte.id_compte)
        db.add(demande)

    jeton = securite.generer_jeton_reinitialisation()
    demande.statut = StatutDemandeReinit.en_attente
    demande.jeton_hash = securite.hacher_jeton(jeton)
    demande.expire_le = _maintenant() + timedelta(
        minutes=settings.DUREE_JETON_REINIT_MINUTES
    )
    demande.motif = "Réinitialisation demandée par l'administration."
    demande.traite_par = admin.id_compte
    demande.date_traitement = None
    db.commit()
    db.refresh(demande)

    lien = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?jeton={jeton}"
    return lien, demande


def cloturer_demande(db: Session, id_demande: int, admin: Compte, statut: StatutDemandeReinit) -> DemandeReinitialisation:
    """Clôt une demande : « traitée » (le médecin a récupéré son accès) ou
    « annulée » (sans objet). Dans les deux cas le jeton est détruit, pour
    qu'un lien oublié sur le papier ne reste pas valable."""
    demande = db.get(DemandeReinitialisation, id_demande)
    if demande is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Demande {id_demande} introuvable.",
        )
    if demande.statut is not StatutDemandeReinit.en_attente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette demande a déjà été traitée.",
        )

    demande.statut = statut
    demande.jeton_hash = None
    demande.expire_le = None
    demande.traite_par = admin.id_compte
    demande.date_traitement = _maintenant()
    db.commit()
    db.refresh(demande)
    return demande


# ---------------------------------------------------------------------------
# Statistiques
# ---------------------------------------------------------------------------


def statistiques(db: Session) -> dict:
    """Compteurs pour le tableau de bord de l'administration."""

    def par_statut(statut: StatutCompte) -> int:
        return (
            db.query(func.count(Compte.id_compte))
            .filter(Compte.statut == statut)
            .scalar()
            or 0
        )

    def par_role(role: RoleCompte) -> int:
        return (
            db.query(func.count(Compte.id_compte))
            .filter(Compte.role == role)
            .scalar()
            or 0
        )

    def sur_7_jours(colonne) -> int:
        return (
            db.query(func.count(Compte.id_compte))
            .filter(colonne >= _maintenant() - timedelta(days=7))
            .scalar()
            or 0
        )

    return {
        "total_comptes": par_role(RoleCompte.medecin) + par_role(RoleCompte.super_admin),
        "comptes_actifs": par_statut(StatutCompte.actif),
        "comptes_en_attente": par_statut(StatutCompte.en_attente),
        "comptes_bloques": par_statut(StatutCompte.bloque),
        "demandes_reinitialisation_en_attente": (
            db.query(func.count(DemandeReinitialisation.id_demande))
            .filter(DemandeReinitialisation.statut == StatutDemandeReinit.en_attente)
            .scalar()
            or 0
        ),
        "inscriptions_7_jours": sur_7_jours(Compte.date_creation),
        "activations_7_jours": sur_7_jours(Compte.date_activation),
        "connexions_7_jours": sur_7_jours(Compte.date_derniere_connexion),
    }