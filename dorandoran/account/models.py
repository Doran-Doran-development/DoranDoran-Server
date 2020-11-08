from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    email = models.EmailField(_('email address'), unique=True, max_length=128)
    
    USERNAME_FIELD = 'email'