from typing import Union, Optional, Iterable, List, Dict
from django.db import models
from django.utils.text import slugify
from . import SlugField


class SuperModel(models.Model):
    def save(
        self,
        force_insert: bool,
        force_update: bool,
        using: Optional[str],
        update_fields: Optional[Iterable[str]],
    ) -> None:

        for field in self._meta.get_fields():
            if field.get_internal_type() == "SuperSlugField":
                if isinstance(field, SlugField):
                    try:
                        source_field = getattr(self, field.slug_from)

                    except AttributeError:
                        raise ("slug_from property does not target a valid field")

                    if self.pk:
                        old = self.objects.get(pk=self.pk)

                        if getattr(old, field.slug_from) != source_field:
                            setattr(self, field.name, slugify(source_field))

                    else:
                        setattr(self, field.name, slugify(source_field))

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class SlugField(models.SlugField):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]],
        name: Optional[str],
        primary_key: bool,
        max_length: Optional[int],
        allow_unicode: bool,
        unique: bool,
        blank: bool,
        null: bool,
        db_index: bool,
        default: str,
        editable: bool,
        auto_created: bool,
        serialize: bool,
        unique_for_date: Optional[str],
        unique_for_month: Optional[str],
        unique_for_year: Optional[str],
        choices: Optional[Union[List[str], List[int]]],
        help_text: str,
        db_column: Optional[str],
        db_tablespace: Optional[str],
        error_messages: Optional[Union[Dict[str, str], str]],
        slug_from: str,
        validators=None,
    ):
        if slug_from:
            self.slug_from = slug_from

        super().__init__(
            verbose_name=verbose_name,
            name=name,
            primary_key=primary_key,
            max_length=max_length,
            allow_unicode=allow_unicode,
            unique=unique,
            blank=blank,
            null=null,
            db_index=db_index,
            default=default,
            editable=editable,
            auto_created=auto_created,
            serialize=serialize,
            unique_for_date=unique_for_date,
            unique_for_month=unique_for_month,
            unique_for_year=unique_for_year,
            choices=choices,
            help_text=help_text,
            db_column=db_column,
            db_tablespace=db_tablespace,
            validators=validators,
            error_messages=error_messages,
        )

    def get_internal_type(self) -> str:
        return "SuperSlugField"