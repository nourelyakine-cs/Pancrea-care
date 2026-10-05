from pydantic import model_validator
from pydantic_settings import BaseSettings

# Secret de développement : uniquement acceptable tant que l'environnement est
# `development`. Le validateur ci-dessous refuse de démarrer l'API en
# production avec cette valeur — un secret JWT par défaut en production
# permettrait à quiconque de forger un jeton d'admin.
SECRET_PAR_DEFAUT = "dev-secret-a-remplacer-en-production"


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    APP_NAME: str = "PANCRA"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # Mode développement : quand True, les routes protégées sont accessibles
    # SANS vérification du jeton (utilise un compte « démo » créé à la volée).
    # À garder à False en production.
    DISABLE_AUTH: bool = False

    # Signature des jetons de session (HS256). JWT_SECRET doit être tiré au
    # hasard et rester secret : il est la seule chose qui distingue un jeton
    # émis par l'API d'un jeton forgé.
    JWT_SECRET: str = SECRET_PAR_DEFAUT
    JWT_ALGORITHM: str = "HS256"
    # Durée de validité d'un jeton de connexion. Le compte est relu en base à
    # chaque requête : un blocage par l'admin prend effet immédiatement, sans
    # attendre l'expiration du jeton.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720

    # Anti-force brute : le compte est refusé jusqu'à `verrouille_jusqu_a`
    # après MAX_TENTATIVES_CONNEXION échecs consécutifs.
    MAX_TENTATIVES_CONNEXION: int = 5
    DUREE_VERROUILLAGE_MINUTES: int = 15

    # Durée de validité du jeton de réinitialisation que l'admin délivre au
    # médecin qui a oublié son mot de passe. La plateforme n'envoie aucun
    # email : le jeton est transmis par l'admin (téléphone, WhatsApp...).
    DUREE_JETON_REINIT_MINUTES: int = 60

    # URL du frontend : préfixe des liens de réinitialisation remis à l'admin.
    FRONTEND_URL: str = "http://localhost:3000"

    # `model_validator` et non `__post_init__` : sous Pydantic v2, une méthode
    # `__post_init__` n'est PAS appelée automatiquement. Écrite ainsi, la garde
    # ne s'exécutait jamais et l'API démarrait en production avec le secret par
    # défaut — anyone aurait alors pu forger un jeton d'administration.
    @model_validator(mode="after")
    def _refuser_secret_par_defaut_hors_developpement(self) -> "Settings":
        if self.ENVIRONMENT != "development" and self.JWT_SECRET == SECRET_PAR_DEFAUT:
            raise ValueError(
                "JWT_SECRET doit être défini (valeur aléatoire) hors "
                "développement : avec le secret par défaut, n'importe qui "
                "pourrait forger un jeton d'administration."
            )
        return self


settings = Settings()