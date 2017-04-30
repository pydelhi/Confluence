from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^attendance/(?P<ticketing_platform>\w+)/$',
        views.mark_attendance,
        name="attendance"),
]
