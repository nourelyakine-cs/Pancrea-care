"""Politique de mot de passe : source de vérité unique.

Les règles sont définies ici, appliquées par l'API (`/auth/signup`,
`/auth/reset-password`) ET publiées via `GET /auth/password-policy`. Le
formulaire consomme cet endpoint, donc les règles affichées au médecin sont
exactement celles qui sont contrôlées côté serveur — pas de divergence entre
ce qui est affiché et ce qui est refusé.
"""

from pydantic import BaseModel, Field

# Codes de règles stables, consommés tels quels par le frontend.
MIN_LENGTH = "min_length"
LOWERCASE = "lowercase"
UPPERCASE = "uppercase"
DIGIT = "digit"


class PasswordPolicy(BaseModel):
    min_length: int = Field(ge=1)
    require_lowercase: bool = True
    require_uppercase: bool = True
    require_digit: bool = True

    def rules(self) -> list[str]:
        """Liste ordonnée des codes de règles à satisfaire."""
        actives = [MIN_LENGTH]
        if self.require_lowercase:
            actives.append(LOWERCASE)
        if self.require_uppercase:
            actives.append(UPPERCASE)
        if self.require_digit:
            actives.append(DIGIT)
        return actives


# Supabase Auth n'impose par défaut qu'une longueur minimale (6 caractères) et
# ne rend ses refus que sous forme de message opaque. On durcit ici le
# minimum à 8 caractères + complexité, car l'application héberge des données
# patients. La connexion n'est jamais bloquée par ces règles : un compte créé
# avant ce durcissement doit rester accessible.
PASSWORD_POLICY = PasswordPolicy(
    min_length=8,
    require_lowercase=True,
    require_uppercase=True,
    require_digit=True,
)


def failed_password_rules(password: str, policy: PasswordPolicy | None = None) -> list[str]:
    """Retourne les codes de règles non respectés par `password`."""
    active = policy or PASSWORD_POLICY
    echecs: list[str] = []

    if len(password) < active.min_length:
        echecs.append(MIN_LENGTH)
    if active.require_lowercase and not any(c.islower() for c in password):
        echecs.append(LOWERCASE)
    if active.require_uppercase and not any(c.isupper() for c in password):
        echecs.append(UPPERCASE)
    if active.require_digit and not any(c.isdigit() for c in password):
        echecs.append(DIGIT)
    return echecs


# Libellés français, utilisés pour le message d'erreur de l'API.
RULE_LABELS: dict[str, str] = {
    MIN_LENGTH: "au moins {min_length} caractères",
    LOWERCASE: "une lettre minuscule",
    UPPERCASE: "une lettre majuscule",
    DIGIT: "un chiffre",
}


def describe_password_errors(password: str, policy: PasswordPolicy | None = None) -> str:
    """Phrase lisible listant ce qu'il manque au mot de passe."""
    active = policy or PASSWORD_POLICY
    echecs = failed_password_rules(password, active)
    if not echecs:
        return ""
    details = ", ".join(
        RULE_LABELS[code].format(min_length=active.min_length) for code in echecs
    )
    return f"Mot de passe non conforme : il doit contenir {details}."
