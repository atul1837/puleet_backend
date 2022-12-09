from django.urls import include, path

from pumeet.candidate_profile.api.views import ProfileDetailView

app_name = "candidate_profile"

urlpatterns = [ path('profile/', ProfileDetailView.as_view(), name='profile')]
