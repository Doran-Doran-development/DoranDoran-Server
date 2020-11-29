from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    email = models.EmailField(_('email address'), unique=True, max_length=128, primary_key=True)
    is_teacher = models.BooleanField(
        _('teacher status'),
        default = False,
        help_text=_('Can accept or refuse reservation request')
    )

    USERNAME_FIELD = 'email'