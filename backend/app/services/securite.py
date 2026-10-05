"""Mots de passe et jetons : tout le cryptographique de l'authentification.

Deux mécanismes distincts, volontairement non interchangeables :

* les **mots de passe** sont vérifiés par bcrypt (hachage à sel, non
  réversible) ;
* les **jetons** — session et réinitialisation — sont signés (JWT HS256 pour la
  session, aléatoire opaque pour la réinitialisation) et lus par l'API, jamais
  stockés en clair.

Le module ne dépend que de la configuration : il est testable sans base.
"""

import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings


# ---------------------------------------------------------------------------
# Mots de passe
# ---------------------------------------------------------------------------


def _aplatir(mot_de_passe: str) -> bytes:
    """Réduit le mot de passe à 44 octets sans perte d'information.

    bcrypt ignore silencieusement tout ce qui dépasse 72 octets : deux mots de
    passe ne différant que par leur fin seraient alors acceptés comme
    identiques. On hache d'abord en SHA-256 puis on encode en base64 — le
    résultat fait 44 octets, quelle que soit la longueur d'origine, et deux
    entrées distinctes ont des empreintes distinctes.
    """
    return base64.b64encode(hashlib.sha256(mot_de_passe.encode("utf-8")).digest())


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    """Retourne l'empreinte bcrypt du mot de passe, prête à être stockée."""
    return bcrypt.hashpw(_aplatir(mot_de_passe), bcrypt.gensalt()).decode("ascii")


def verifier_mot_de_passe(mot_de_passe: str, empreinte: str | None) -> bool:
    """Vérifie un mot de passe contre son empreinte.

    Renvoie `False` — jamais d'exception — si l'empreinte est absente ou
    malformée : un compte migré sans hash exploitable doit se comporter comme
    un mot de passe qui ne correspond pas, pas comme une panne du serveur.
    """
    if not empreinte:
        return False
    try:
        return bcrypt.checkpw(_aplatir(mot_de_passe), empreinte.encode("ascii"))
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# Jetons de session (JWT)
# ---------------------------------------------------------------------------


def creer_jeton_session(id_compte: int, role: str, duree_minutes: int | None = None) -> str:
    """Signe un jeton de connexion pour le compte donné.

    Le jeton ne porte que l'identité et le rôle : le statut du compte est relu
    en base à chaque requête, ce qui garantit qu'un blocage par l'admin prend
    effet immédiatement, sans attendre l'expiration du jeton.
    """
    duree = duree_minutes if duree_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    maintenant = datetime.now(timezone.utc)
    charge = {
        "sub": str(id_compte),
        "role": role,
        "type": "session",
        "iat": maintenant,
        "exp": maintenant + timedelta(minutes=duree),
    }
    return jwt.encode(charge, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decoder_jeton_session(token: str) -> dict:
    """Décode et vérifie la signature d'un jeton de session.

    Lève `jwt.InvalidTokenError` si le jeton est expiré, altéré ou signé avec
    une autre clé. La signature est vérifiée avant toute lecture de contenu :
    un jeton forgé ne permet jamais d'obtenir un rôle.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def id_compte_du_jeton(token: str) -> int:
    """Extrait l'identifiant de compte d'un jeton de session vérifié."""
    charge = decoder_jeton_session(token)
    if charge.get("type") != "session":
        raise jwt.InvalidTokenError("Type de jeton inattendu.")
    return int(charge["sub"])


# ---------------------------------------------------------------------------
# Jeton de réinitialisation (opaque, à usage unique)
# ---------------------------------------------------------------------------


def generer_jeton_reinitialisation() -> str:
    """Jeton aléatoire destiné à être transmis au médecin par l'admin.

    256 bits d'entropie : aucune hopes de deviner le jeton n'est realistic, ce
    qui rend inutile un compteur de tentatives sur cette route.
    """
    return secrets.token_urlsafe(32)


def hacher_jeton(jeton: str) -> str:
    """Empreinte du jeton, seule conservée en base.

    SHA-256 suffit ici (et non bcrypt) parce que le jeton est lui-même
    aléatoire et à haute entropie : il n'y a pas de dictionnaire à énumérer,
    et une vérification doit rester instantanée.
    """
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()