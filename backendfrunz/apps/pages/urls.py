from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("events/", views.events_list, name="events_list"),
    path("events/<str:slug>/", views.event_detail, name="event_detail"),
    path("clubs/", views.clubs_list, name="clubs_list"),
    path("clubs/<str:slug>/", views.club_detail, name="club_detail"),
    path("news/", views.news_list, name="news_list"),
    path("news/<str:slug>/", views.news_detail, name="news_detail"),
    path("documents/", views.documents, name="documents"),
    path("dobrocenter/", views.dobrocenter, name="dobrocenter"),
    path("contacts/", views.contacts, name="contacts"),
    path("anticorruption/", views.anticorruption, name="anticorruption"),
]
