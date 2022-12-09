from django.urls import include, path

from pumeet.seat_management.api.views import PreferenceListView, PreferenceView

app_name = "seat_management"

urlpatterns = [ 
    path('prefrence/list/', PreferenceListView.as_view(), name='prefrences'),
    path('prefrence/', PreferenceView.as_view(), name='prefrence')
]
