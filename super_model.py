from django.db import models
from typing import Optional, Iterable
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
