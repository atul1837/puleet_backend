from django.db import models
from django.utils.translation import ugettext_lazy as _

from pumeet.utils.models import BaseModel


class Seats(BaseModel):
    name=models.CharField(max_length=256)
    total_seats = models.IntegerField()
    category_seats = models.JSONField()