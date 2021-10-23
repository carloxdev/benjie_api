# Django's Libraries
from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_date = models.DateTimeField(
        verbose_name="fecha registro",
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        verbose_name="fecha edición",
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'core.User',
        verbose_name="creado por",
        related_name="%(class)s_created",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        'core.User',
        verbose_name="editado por",
        related_name="%(class)s_updated",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class ModelValidator:

    @classmethod
    def check_DontHaveWhitespaces(self, value):
        if ' ' in value:
            raise ValidationError(
                "No puede contener espacios en blanco.",
                code='with_whitespaces',
            )


class KeyCharField(models.CharField):
    # def __init__(self, *args, **kwargs):
    #     super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            return str(value).upper()

        return value


class NameCharField(models.CharField):

    def get_prep_value(self, value):
        new_value = str(value).lower()
        return new_value.title()


class DescriptionCharField(models.CharField):

    def get_prep_value(self, value):
        new_value = str(value).lower()
        return new_value.capitalize()
