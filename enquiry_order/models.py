from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from datetime import datetime
from hoitymoppet.models import *

# Create your models here.

class Businessorder(models.Model):
    businessorder_name = models.CharField(max_length=255)
    businessorder_url = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.company_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "business Order"