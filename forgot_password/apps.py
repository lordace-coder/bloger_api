from django.apps import AppConfig


class ForgotPasswordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forgot_password'
    def ready(self) -> None:
        import forgot_password.signals
        return super().ready()