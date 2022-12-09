from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from pumeet.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls + [
   path("candidate-profile/", include("pumeet.candidate_profile.api.urls", namespace="candidate_profile")),
   path("seat-management/", include("pumeet.seat_management.api.urls", namespace="seat_management")),
]  
