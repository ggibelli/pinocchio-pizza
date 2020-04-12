from django.contrib.auth.models import AbstractUser

from django.db import models
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    slug = AutoSlugField(populate_from='username')

