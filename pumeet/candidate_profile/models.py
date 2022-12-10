from django.db import models
from django.utils.translation import ugettext_lazy as _

from pumeet.utils.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(BaseModel):
    """
    Profile model
    """

    GENERAl = "general"
    SCHEDULED_CASTE = "scheduled_caste"
    SCHEDULED_TRIBE = "schedule_tribe"

    CATEGORY_CHOICES = ((GENERAl, "General"), (SCHEDULED_CASTE, "Scheduled Caste"), (SCHEDULED_TRIBE, "Scheduled Tribe"))

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other"))

    name = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    father_name = models.CharField(max_length=256, blank=True, null=True)
    mother_name = models.CharField(max_length=256, blank=True, null=True)
    date_of_birth = models.DateField(_("Date of birth"), auto_now=False, auto_now_add=False, blank=True, null=True)
    category = models.CharField(
        _("Category"),
        help_text=_("Category of candidate"),
        max_length=255,
        default=GENERAl,
        choices=CATEGORY_CHOICES,
        blank=True, 
        null=True
    )
    email = models.EmailField(blank=True, null=True)
    mobile_no = models.CharField(max_length=256, blank=True, null=True)
    gender = models.CharField(
        _("Gender"),
        max_length=256,
        help_text=_("Gender of candidate"),
        choices=GENDER_CHOICES,
        blank=True, 
        null=True
    )
    nationality = models.CharField(max_length=256, blank=True, null=True)
    correspondance_address = models.TextField(blank=True, null=True)
    permanenty_address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=256, blank=True, null=True)
    tenth_board = models.TextField(blank=True, null=True)
    tenth_marks = models.DecimalField(
        _("Marks in tenth"),
        max_digits=5,
        decimal_places=2,
        db_index=True,
        null=True,
        blank=True,
    )
    tenth_passing_year = models.IntegerField(blank=True, null=True)
    tweleveth_board = models.TextField(blank=True, null=True)
    tweleveth_makrs = models.DecimalField(
        _("Marks in twelveth"),
        max_digits=5,
        decimal_places=2,
        db_index=True,
        null=True,
        blank=True,
    )
    tweleveth_passing_year = models.IntegerField(blank=True, null=True)
    diploma_branch = models.CharField(max_length=256, blank=True, null=True)
    diploma_passing_year = models.IntegerField(blank=True, null=True)
    diploma_board = models.TextField(blank=True, null=True)
    diploma_institute = models.TextField(blank=True, null=True)
    diploma_marks = models.DecimalField(
        _("Marks in diploma"),
        max_digits=5,
        decimal_places=2,
        db_index=True,
        null=True,
        blank=True,
    )
    all_india_rank = models.IntegerField(blank=True, null=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

