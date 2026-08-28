import resend

from app.config import settings


def resend_configured() -> bool:
    return bool(settings.RESEND_API_KEY and settings.RESEND_FROM)


def send_password_reset_email(to_email: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    subject = "Reinitialisation de votre mot de passe - PANCRA"
    html = f"""
<p>Bonjour,</p>
<p>Vous avez demande la reinitialisation de votre mot de passe.</p>
<p>
    Cliquez sur le lien ci-dessous pour choisir un nouveau mot de passe
    (valable {settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes) :
</p>
<p><a href="{reset_url}">{reset_url}</a></p>
<p>Si vous n'etes pas a l'origine de cette demande, ignorez cet email.</p>
"""

    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send(
        {
            "from": settings.RESEND_FROM,
            "to": [to_email],
            "subject": subject,
            "html": html,
        }
    )