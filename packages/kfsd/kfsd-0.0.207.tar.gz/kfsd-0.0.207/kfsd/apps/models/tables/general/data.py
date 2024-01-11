from django.db import models
from django.utils.text import slugify
from slugify import slugify as uslugify

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.file import File


def gen_data_id(name):
    return "{}={}".format("DATA", name)


class Data(BaseModel):
    SOURCE_TYPE_CHOICES = (
        ("RAW", "RAW"),
        ("FILE", "FILE"),
        ("ENDPOINT", "ENDPOINT"),
    )
    name = models.CharField(max_length=MAX_LENGTH)
    is_template = models.BooleanField(default=False)
    default_template_values = models.JSONField(default=dict)
    content_type = models.CharField(max_length=MAX_LENGTH)
    source_type = models.CharField(
        max_length=MAX_LENGTH, choices=SOURCE_TYPE_CHOICES, default="RAW"
    )
    raw_body = models.TextField(blank=True, null=True)
    raw_json_body = models.JSONField(default=dict)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    endpoint = models.ForeignKey(
        "Endpoint", on_delete=models.CASCADE, blank=True, null=True
    )
    key = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.key:
            self.key = uslugify(self.name, separator="_")
        if not self.identifier:
            self.identifier = gen_data_id(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Data"
        verbose_name_plural = "Data"
