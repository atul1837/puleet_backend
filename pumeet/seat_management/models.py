from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from pumeet.utils.models import BaseModel

user = get_user_model()
class Branch(BaseModel):
    branch_name=models.CharField(max_length=256)
    total_seats = models.IntegerField()
    general_seats = models.IntegerField()
    sc_seats = models.IntegerField()
    st_seats = models.IntegerField()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.total_seats != self.general_seats + self.sc_seats + self.st_seats:
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


class Allotment(BaseModel):

    GENERAl = "general"
    SCHEDULED_CASTE = "scheduled_caste"
    SCHEDULED_TRIBE = "schedule_tribe"

    CATEGORY_CHOICES = ((GENERAl, "General"), (SCHEDULED_CASTE, "Scheduled Caste"), (SCHEDULED_TRIBE, "Scheduled Tribe"))


    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    allotment_category = models.CharField(
        _("Allotment Category"),
        help_text=_("Category of allotment"),
        max_length=255,
        default=GENERAl,
        choices=CATEGORY_CHOICES,
        blank=True, 
        null=True
    )

    def general_count(self, branch):
        return Allotment.objects.filter(branch=branch, allotment_category=self.GENERAl).count()

    def sc_count(self, branch):
        return Allotment.objects.filter(branch=branch, allotment_category=self.SCHEDULED_CASTE).count()

    def st_count(self, branch):
        return Allotment.objects.filter(branch=branch, allotment_category=self.SCHEDULED_TRIBE).count()

    def total_count(self, branch):
        return Allotment.objects.filter(branch=branch).count()