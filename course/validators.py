from django.core.exceptions import ValidationError

class YoutubeLinkValidator:
    def __init__(self, domain="youtube.com"):
        self.domain = domain

    def __call__(self, value):
        if not value.startswith(f"https://www.{self.domain}/"):
            raise ValidationError(f"Ссылка должна вести на {self.domain}.")

