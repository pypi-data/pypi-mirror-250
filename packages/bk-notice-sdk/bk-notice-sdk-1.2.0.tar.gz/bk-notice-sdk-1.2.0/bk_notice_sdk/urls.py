from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^announcements/$", views.get_current_information, name="get_current_information"),
]
