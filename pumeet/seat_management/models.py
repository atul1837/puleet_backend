from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from pumeet.utils.models import BaseModel

user = get_user_model()
class Branch(BaseModel):
    branch_name=models.CharField(max_length=256)
    total_seats = models.IntegerField()
    general_seat = models.IntegerField()
    sc_seat = models.IntegerField()
    st_seat = models.IntegerField()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.total_seats != self.general_seat + self.sc_seat + self.st_seat:
            raise Exception("Total seats not equal to sum of all seats")
        return super(Branch, self).save(force_insert, force_update, using)


class Preference(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    preference = models.IntegerField()
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if Preference.objects.filter(user=self.user, preference=self.preference).exists():
            raise Exception("Preference already exists")
        if Preference.objects.filter(user=self.user, branch=self.branch).exists():
            raise Exception("Branch already exists")
        return super(Preference, self).save(force_insert, force_update, using)
