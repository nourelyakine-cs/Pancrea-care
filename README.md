# PancreaCare (PANCRA)

**Plateforme web d'aide à la décision clinique pour le cancer du pancréas.**

PancreaCare assiste les médecins dans la prise en charge des adénocarcinomes
pancréatiques : constitution du dossier patient, **évaluation clinique
standardisée**, **classification TNM**, détermination de la **résécabilité**,
application des **critères ABC** et génération de **recommandations
thérapeutiques** fondées sur le référentiel **TNCD** (Thésaurus National de
Cancérologie Digestive, chapitre 9, cancer du pancréas).

Le moteur de règles est **déterministe** : chaque résultat affiche les faits
examinés, les critères croisés et la référence bibliographique citée, avec son
niveau de preuve. La plateforme ne décide pas à la place du médecin — elle
prépare et trace l'argumentaire avant la discussion en **RCP**.

---

## Table des matières

1. [Ce que fait le projet](#2-ce-que-fait-le-projet)
2. [Le moteur de règles cliniques](#3-le-moteur-de-règles-cliniques)
3. [Technologies utilisées](#4-technologies-utilisées)
4. [Architecture du dépôt](#5-architecture-du-dépôt)
5. [Prérequis](#6-prérequis)
6. [Installation pas à pas](#7-installation-pas-à-pas)
7. [Configuration](#8-configuration)
8. [Premier lancement](#9-premier-lancement)
9. [Manuel d'utilisation](#10-manuel-dutilisation)
10. [Faire évoluer le schéma de base de données](#11-faire-évoluer-le-schéma-de-base-de-données)
11. [Dépannage](#12-dépannage)

---

## 1. Ce qu'est le projet

PancreaCare est un duo **API (backend) + interface web (frontend)** destiné aux
services de cancérologie digestive.

Il couvre deux besoins :

- **Côté médecin** — créer et suivre des dossiers patients, saisir les données
  de l'évaluation (état clinique, biologie, imagerie, TNM, histologie,
  parcours de traitement), obtenir le calcul de classification et les
  recommandations proposées, avec l'historique complet des évaluations.
- **Côté administration** — gérer le cycle de vie des comptes médecins
  (inscription, validation, blocage, mots de passe), car les comptes sont
  validés par un **super admin** avant toute utilisation : la plateforme
  n'envoie aucun e-mail, toutes les réinitialisations passent par l'admin.

## 2. Ce que fait le projet

### Espace médecin (`/dashboard`)

- **Liste des patients** — vue des dossiers du médecin connecté, avec accès à
  leurs évaluations.
- **Création d'un patient en 8 étapes** — saisie guidée :

  1. **Démographie** — identité, âge, sexe, contact.
  2. **État clinique** — ECOG, état nutritionnel, comorbidités, douleur,
     ictère/angiocholite, diabète, opérabilité.
  3. **Biologie** — CA 19-9, bilirubine, albumine, statut DPD.
  4. **Imagerie** — localisation tumorale, taille, contacts vasculaires
     (AMS, tronc coeliaque, artère hépatique, VMS/VP), adénopathies, métastases.
  5. **TNM** — catégories T / N / M.
  6. **Histologie** — preuve histologique, mutations (BRCA, KRAS, MSI/dMMR,
     fusions NTRK/NRG1).
  7. **Parcours** — ligne de traitement, réponses aux traitements, progression.
  8. **Calcul & aide à la décision** — le moteur calcule et affiche le
     résultat avant la génération du rapport.

- **Évaluations par patient** — historique des évaluations avec leur contexte
  (diagnostic initial, pré-néoadjuvant, restaging, pré-chirurgie, adjuvant,
  surveillance, récidive) et le rapport détaillé de chacune.
- **Modification d'un dossier patient.**

### Espace administration (`/admin`)

- Statistiques (compteurs en tête du tableau de bord).
- **Comptes médecins** — validation des inscriptions, blocage/déblocage,
  recherche, attribution d'un mot de passe temporaire.
- **Demandes de réinitialisation** — génération d'un lien à usage unique à
  transmettre au médecin, clôture des demandes.

### Securité

- Hachage des mots de passe (`bcrypt`), sessions à jeton **JWT**.
- Contrôle d'accès par rôle (`medecin` / `super_admin`) et cloisonnement des
  dossiers : un médecin ne voit que ses patients.
- Politique de mot de passe stricte vérifiée côté serveur.
- Anti-force brute : verrouillage temporaire du compte après échecs répétés.

## 3. Le moteur de règles cliniques

Implémenté en Python (`app/services/clinical_rules/`), il est appliqué par
évaluation et produit des **données dérivées** persistées en base :

### Calcul de classification

| Sortie | Exemples |
|---|---|
| **Résécabilité** | `resecable` · `borderline` · `localement_avance` · `metastatique` |
| **Stade TNM** | T1a-T3, N0-N2, M0/M1, stade global IA–IV |
| **Critères ABC** | statut vasculaire + CA 19-9 + état général ; sous-catégorie dérivée |
| **Justification** | texte JSON détaillant la décision, les corrections appliquées et la référence |

### Recommandations

- **Règles R01–R18** — stratégies thérapeutiques (chirurgie, néoadjuvant,
  induction, lignes de chimiothérapie, soins de support, thérapies ciblées).
- **Règles transverses T1–T4** — drainage biliaire, contre-indications,
  ajustement DPD, preuve histologique.
- Chaque règle cite sa section **TNCD** et son **niveau de preuve** (A, B,
  accord d'experts).

### Trace

L'API renvoie un **chemin de décision** : toutes les règles évaluées
(déclenchées ou non), les critères examinés et les faits utilisés. Cette trace
est l'argumentaire destiné à la RCP.

## 4. Technologies utilisées

| Couche | Technologie |
|---|---|
| Backend | Python 3 · FastAPI · SQLAlchemy 2 · Uvicorn |
| Base de données | PostgreSQL (locale, aucune dépendance Supabase) |
| Authentification | JWT (`PyJWT`) + `bcrypt` |
| Frontend | Next.js 16 · React 19 · TypeScript · Tailwind CSS 4 · Framer Motion |
| Validation | Pydantic (`pydantic-settings`) |

## 5. Architecture du dépôt

```
Pancrea-care/
├─ backend/                      # API FastAPI
│  ├─ app/
│  │  ├─ models/                 # Modèles SQLAlchemy (tables)
│  │  ├─ routes/                 # Endpoints (auth, admin, patients, clinical-rules)
│  │  ├─ schemas/                # Contrats Pydantic (req/réponses)
│  │  └─ services/
│  │     └─ clinical_rules/      # Moteur TNM / ABC / résécabilité / recommandations
│  ├─ database/
│  │  ├─ schema_pancreacare.sql  # ⭐ Schéma unique et complet (source de vérité)
│  │  └─ LOCAL_POSTGRES.md       # Guide base locale détaillé
│  ├─ .env.example               # Modèle de configuration
│  └─ requirements.txt
├─ frontend/                     # Application web Next.js
│  ├─ app/                       # Pages (login, admin, dashboard, patients, evaluation)
│  ├─ components/                # Composants (formulaires, étapes, password…)
│  └─ lib/api.ts                 # Client HTTP vers l'API
└─ pancreacare_local_postgres.ps1  # ⭐ Provisionne PostgreSQL et charge le schéma
```

## 6. Prérequis

- **Windows** avec PowerShell 5.1+ (ou un OS avec un serveur PostgreSQL).
- **PostgreSQL 14+** installé — les outils CLI (`psql`, `pg_dump`) doivent être
  disponibles (le script les cherche aussi dans
  `C:\Program Files\PostgreSQL\*\bin`).
- **Python 3.11+**.
- **Node.js 20+** (avec `npm`).

### Variante Docker (backend + PostgreSQL)

Docker Desktop doit être démarré et utiliser le moteur **Linux containers**. Dans
PowerShell, placez-vous dans `backend` (le fichier Compose se trouve dans ce
dossier), puis lancez :

```powershell
cd backend
docker compose up --build
```

Cette configuration démarre PostgreSQL avec un volume persistant et l'API sur
`http://localhost:8000`. Elle crée les tables applicatives au premier démarrage.
Les identifiants PostgreSQL par défaut sont réservés au développement local ;
définissez `POSTGRES_PASSWORD` et `JWT_SECRET` dans l'environnement avant toute
utilisation hors poste local. Pour arrêter les conteneurs, utilisez
`docker compose down`. Les données restent dans le volume `postgres_data`.

L'erreur Windows `open //./pipe/dockerDesktopLinuxEngine: The system cannot
find the file specified` indique que Docker CLI ne parvient pas à joindre le
moteur Linux de Docker Desktop. Démarrez Docker Desktop, attendez que son état
indique qu'il fonctionne, puis réessayez. Si nécessaire, dans Docker Desktop,
choisissez **Switch to Linux containers**. Ce message intervient avant le
démarrage du projet : modifier le code du dépôt ne peut pas démarrer le moteur
Docker manquant.

Vérifications rapides :

```powershell
python --version
node --version
psql --version
```

## 7. Installation pas à pas

### Étape 1 — Provisionner la base de données locale

À la racine du projet :

```powershell
.\pancreacare_local_postgres.ps1
```

Ce script (idempotent) :

1. Vérifie/lance le service PostgreSQL ;
2. Demande le mot de passe du rôle administrateur `postgres` ;
3. Crée le rôle applicatif `pancreacare` (mot de passe généré) ;
4. Crée la base `pancreacare` ;
5. Charge le schéma complet `backend/database/schema_pancreacare.sql` ;
6. Affiche la `DATABASE_URL` à recopier dans `backend\.env`.

Si PostgreSQL n'est pas installé :

```powershell
winget install --id PostgreSQL.PostgreSQL
# puis
.\pancreacare_local_postgres.ps1 -AutoInstall
```

### Étape 2 — Installer et configurer le backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Créez le fichier `.env` à partir du modèle :

```powershell
Copy-Item .env.example .env
```

Puis renseignez `DATABASE_URL` avec la valeur affichée par le script (en
prélevant le mot de passe généré) :

```dotenv
DATABASE_URL=postgresql://pancreacare:<mot_de_passe>@localhost:5432/pancreacare
```

### Étape 3 — Installer le frontend

```powershell
cd ..\frontend
npm install
```

Le frontend appelle l'API sur `http://127.0.0.1:8000` par défaut (variable
`NEXT_PUBLIC_API_URL`), ce qui convient à un développement local sans autre
configuration.

## 8. Configuration

### Backend — `backend/.env`

| Variable | Rôle |
|---|---|
| `DATABASE_URL` | Chaîne de connexion PostgreSQL *(obligatoire)* |
| `ENVIRONMENT` | `development` ou `production` |
| `BACKEND_CORS_ORIGINS` | Origines autorisées (JSON) |
| `JWT_SECRET` | Secret de signature des jetons — générez un secret fort : `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de vie des sessions (720 = 12 h) |
| `MAX_TENTATIVES_CONNEXION` / `DUREE_VERROUILLAGE_MINUTES` | Anti-force brute |
| `DUREE_JETON_REINIT_MINUTES` | Validité des liens de réinitialisation |
| `FRONTEND_URL` | URL du frontend (liens de réinitialisation) |
| `DISABLE_AUTH` | ⚠ Développement uniquement (`True` court-circuite l'authentification) |

Multiples exemples et explications sont commentés dans `.env.example`. Le
fichier `.env` ne doit **jamais** être versionné (il est inscrit dans
`.gitignore`).

### Frontend — `frontend/.env.local`

Utilisez-le uniquement si l'API n'est pas sur `http://127.0.0.1:8000` :

```dotenv
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## 9. Premier lancement

### Créer le compte super administrateur

Le backend démarre avec **zéro compte** : le premier compte est créé par un
script dédié, qui le crée **directement actif** (l'admin valide les autres
comptes, il ne peut pas se valider lui-même).

```powershell
python -m app.bootstrap_admin
```

Le script demande l'email, le mot de passe (avec confirmation), le nom et le
prénom. Il crée aussi le profil médecin rattaché, pour que cet administrateur
puisse aussi utiliser l'espace clinique.

### Lancer le backend

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Sain : `GET http://127.0.0.1:8000/health` renvoie `{"status": "ok"}`. La
documentation interactive de l'API est disponible sur
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Lancer le frontend

```powershell
cd frontend
npm run dev
```

Ouvrez [http://localhost:3000](http://localhost:3000).

## 10. Manuel d'utilisation

### 10.1 Se créer un compte médecin

1. Ouvrez la page d'accueil puis **« S'inscrire »** (ou `/login?mode=signup`).
2. Renseignez nom, prénom, téléphone, établissement, email et un mot de passe
   conforme à la politique affichée en direct.
3. Validez : la demande est transmise. **Le compte est en attente** de
   validation par un administrateur — aucune connexion n'est possible avant.

Connectez-vous plus tard dans l'espace médecin :
[http://localhost:3000/login](http://localhost:3000/login).

### 10.2 Valider les comptes (super admin)

1. Connectez-vous avec le compte créé par `bootstrap_admin`.
2. Vous arrivez sur `/admin`.
3. Dans **« Comptes »**, filtrez par statut `en_attente`, vérifiez l'identité
   du demandeur puis **« Accepter »** — le compte devient actif.
4. Pour un compte actif : **bloquer** (avec motif), **débloquer**, ou imposer
   un **mot de passe temporaire** que le médecin devra changer.

### 10.3 Gérer un mot de passe oublié

1. Le médecin clique « Mot de passe oublié » et saisit son email.
2. L'admin voit la demande dans **« Demandes de réinitialisation »**.
3. L'admin génère le **lien à usage unique** et le transmet au médecin par un
   canal sûr (téléphone, messagerie) — il est valable
   `DUREE_JETON_REINIT_MINUTES` minutes et ne sert qu'une fois.
4. Le médecin ouvre le lien, choisit un nouveau mot de passe, puis se connecte.
5. L'admin clôt la demande comme **traitée** (ou **annulée** si elle est sans
   objet).

### 10.4 Créer un patient et calculer la décision (médecin)

1. Dans `<dashboard>/patients`, cliquez **« Nouveau patient »**.
2. Remplissez les **8 étapes** (Démographie → État clinique → Biologie →
   Imagerie → TNM → Histologie → Parcours → Calcul).
3. À l'**étape 8**, le backend crée le dossier **et** l'évaluation, puis calcule
   la classification. Résultats affichés :
   - **Critères ABC** (sous-catégorie, critères B/C),
   - **Stade TNM** (T / N / M + stade global),
   - **Résécabilité** (avec mention « à discuter en RCP » si non résécable).
4. **« Voir le Rapport d'Évaluation »** : rapport complet avec le contexte de
   l'évaluation, les faits, les recommandations R01–R18 / T1–T4 déclenchées et
   les références TNCD citées, ainsi que le chemin de décision.

### 10.5 Suivre un patient

- Depuis la liste des patients, ouvrez le dossier puis **« Évaluations »** :
  historique des évaluations daté et contexté (initial, restaging, chirurgie,
  surveillance, récidive…).
- Chaque évaluation peut être rouverte dans son rapport.
- Vous pouvez **modifier** les informations du dossier.

## 11. Faire évoluer le schéma de base de données

Le schéma est délibérément **unique et complet** : pas de migrations
incrémentales. Après une modification de la base locale, régénérez le fichier
de référence :

```powershell
$env:PGPASSWORD = "<mot de passe pancarecare>"
pg_dump -U pancreacare -h localhost -p 5432 -d pancreacare `
    --schema-only --no-owner --no-privileges `
    -f backend\database\schema_pancreacare.sql
```

Attention : ce fichier ne doit être rejoué que sur une **base vide** (ou une
nouvelle base). Un autre poste reproduira exactement la même base via
`pancreacare_local_postgres.ps1`.

## 12. Dépannage

### `relation "compte" does not exist`

La base n'a pas le schéma attendu. Rejouez le provisionnement :

```powershell
.\pancreacare_local_postgres.ps1
```

### `valeur trop longue pour le type character varying(15)`

Ce type d'erreur vient d'une colonne trop courte. Régénérez le schéma après
avoir appliqué le changement dans la base (voir section 11).

### « Impossible de joindre le serveur »

Le frontend n'atteint pas l'API. Vérifiez : backend démarré sur le port 8000,
et le cas échéant `NEXT_PUBLIC_API_URL` correct dans `frontend/.env.local`.

### Connexion refusée sur `localhost:5432`

- Mot de passe `postgres` erroné (relancez le script avec `-AdminPassword`).
- Le service PostgreSQL n'est pas démarré : `Start-Service postgresql*`.
- Autre port configuré dans `postgresql.conf`.

### `psql` n'est pas reconnu

Installez PostgreSQL (`winget install --id PostgreSQL.PostgreSQL`) ou ajoutez
son dossier `bin` au `PATH`.

---
