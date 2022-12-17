from pumeet.candidate_profile.models import Profile
from pumeet.seat_management.models import Branch, Preference, Allotment

def allot_branches_based_on_preferences_and_rank():
    candidates = Profile.objects.filter(approved=True).order_by('all_india_rank')
    Allotment.objects.all().delete()
    for candidate in candidates:
        preferences = Preference.objects.filter(user=candidate.user).order_by('preference')
        for preference in preferences:
            branch = preference.branch
            if branch.general_seats > Allotment.general_count(branch=branch):
                Allotment.objects.create(user=candidate.user, branch=branch, allotment_category=Allotment.GENERAl, preference=preference)
                break
            elif candidate.category == Profile.SCHEDULED_CASTE and branch.sc_seats > Allotment.sc_count(branch):
                Allotment.objects.create(user=candidate.user, branch=branch, allotment_category=Allotment.SCHEDULED_CASTE, preference=preference)
                break
            elif candidate.category == Profile.SCHEDULED_TRIBE and branch.st_seats > Allotment.st_count(branch):
                Allotment.objects.create(user=candidate.user, branch=branch, allotment_category=Allotment.SCHEDULED_TRIBE, preference=preference)
                break
    return True