from django.urls import include, path

from pumeet.seat_management.api.views import PreferenceListView, PreferenceView, BranchListView, AllotmentView

app_name = "seat_management"

urlpatterns = [ 
    path('branch/list/', BranchListView.as_view(), name='branches'),
    path('prefrence/list/', PreferenceListView.as_view(), name='prefrences'),
    path('prefrence/', PreferenceView.as_view(), name='prefrence'),
    path("allotment/", AllotmentView.as_view(), name="allotment")
]
