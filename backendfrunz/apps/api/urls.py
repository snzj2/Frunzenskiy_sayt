from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("news/", views.news_list, name="news-list"),
    path("events/", views.event_list, name="event-list"),
    path("clubs/", views.club_list, name="club-list"),
    path("locations/", views.location_list, name="location-list"),
]
