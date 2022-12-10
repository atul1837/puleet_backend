from django.urls import include, path

from pumeet.staff.api.views import PreferenceStaffView, BranchView

app_name = "staff"

urlpatterns = [ 
    path('prefrence/<str:user_id>', PreferenceStaffView.as_view(), name='prefrence'),
    path('branch', BranchView.as_view(), name='branch')
]
