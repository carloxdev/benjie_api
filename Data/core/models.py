# Python's Libraries
import secrets

# Django's Libraries
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Third-party Libraries
from simple_history.models import HistoricalRecords

# Own's Libraries
from Utils.models import BaseModel
# from Utils.models import KeyCharField
# from Utils.models import NameCharField
# from Utils.models import DescriptionCharField
from Utils.managers import UserEmailManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(
        _('email'),
        unique=True,
        blank=False,
        null=True,
        error_messages={
            'unique': 'Ya existe otra cuenta asociada a '
            'este correo electrónico.',
        },
    )
    name = models.CharField(
        _('name'),
        max_length=100,
        blank=True,
        null=True
    )
    # position = models.ForeignKey(
    #     'Position',
    #     verbose_name="puesto",
    #     related_name="assign_to",
    #     on_delete=models.PROTECT,
    #     null=True,
    #     blank=True,
    # )
    is_staff = models.BooleanField(
        _('staff status'),
        null=True,
        help_text=_('Al ser Staff se permite acceso al administrador.'),
    )
    is_active = models.BooleanField(
        _('active'),
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(
        _('verificado'),
        null=True,
        blank=True
    )
    date_verified = models.DateTimeField(
        _('fecha de verificacion'),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )
    is_superuser = models.BooleanField(
        _('superusuario'),
        null=True,
        help_text=_(
            'Un usuario Superusuario tiene privilegios totales sobre '
            'el sitio.'
        )
    )
    first_login = models.BooleanField(
        "¿Primer ingreso?",
        null=True,
        blank=True
    )
    reset_password = models.BooleanField(
        "cambiar contraseña",
        null=True,
        blank=True
    )
    session_key = models.CharField(
        verbose_name="clave de sesión",
        max_length=40,
        null=True,
        blank=True
    )
    success_login_counter = models.PositiveIntegerField(
        verbose_name="cant. de accesos",
        null=True,
        blank=True,
        default=0
    )
    last_activity = models.DateTimeField(
        verbose_name="ultima actividad",
        null=True,
        blank=True
    )
    fail_login_counter = models.IntegerField(
        verbose_name="cant. de intentos de acceso",
        default=0,
        null=True,
        blank=True
    )
    last_pass_change = models.DateTimeField(
        verbose_name="ultimo cambio de password",
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    objects = UserEmailManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email
