from django.urls import include, path

from pumeet.staff.api.views import PreferenceStaffView, BranchView, AllotBranchesApi, CandidateListView, CandidateView, CandidateApproveApi

app_name = "staff"

urlpatterns = [ 
    path('prefrence/<str:user_id>', PreferenceStaffView.as_view(), name='prefrence'),
    path('branch', BranchView.as_view(), name='branch'),
    path('allot-branches', AllotBranchesApi.as_view(), name='allot'),
    path('candidate/list', CandidateListView.as_view(), name='candidates'),
    path('candidate/<str:user_id>', CandidateView.as_view(), name='candidate'),
    path('candidate/<str:user_id>/approve', CandidateApproveApi.as_view(), name='candidate_approve')
]
