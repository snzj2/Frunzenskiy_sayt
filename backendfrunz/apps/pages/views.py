from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.applications.models import Application
from apps.clubs.models import Club
from apps.core.models import Direction, DobroCenterPage, Document, HomepageSettings, Location, PublishStatus
from apps.events.models import Event
from apps.news.models import News

from .forms import BaseApplicationForm, FeedbackForm


def _published_news():
    return News.objects.filter(status=PublishStatus.PUBLISHED).select_related("direction", "author")


def _published_events():
    return Event.objects.filter(status=Event.Status.PUBLISHED).select_related("direction", "location")


def _active_clubs():
    return Club.objects.exclude(status=Club.Status.ARCHIVED).select_related("direction", "location")


def _paginate(request, queryset, per_page=9):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))


def home(request):
    settings = HomepageSettings.objects.order_by("-updated_at").first()
    news_count = settings.show_latest_news_count if settings else 3
    events_count = settings.show_nearest_events_count if settings else 3
    clubs_count = settings.show_clubs_count if settings else 6

    context = {
        "home_settings": settings,
        "main_news": _published_news().filter(is_main=True)[:news_count] or _published_news()[:news_count],
        "main_events": _published_events().filter(start_datetime__gte=timezone.now()).order_by("start_datetime")[:events_count],
        "main_clubs": _active_clubs().filter(is_main=True)[:clubs_count] or _active_clubs()[:clubs_count],
        "locations": Location.objects.filter(is_active=True)[:6],
    }
    return render(request, "site/home.html", context)


def news_list(request):
    queryset = _published_news()
    q = request.GET.get("q", "").strip()
    direction = request.GET.get("direction", "").strip()
    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(short_description__icontains=q) | Q(content__icontains=q))
    if direction:
        queryset = queryset.filter(direction__slug=direction)
    context = {
        "page_obj": _paginate(request, queryset, 9),
        "directions": Direction.objects.filter(is_active=True),
        "selected_direction": direction,
        "q": q,
    }
    return render(request, "site/news_list.html", context)


def news_detail(request, slug):
    news = get_object_or_404(_published_news(), slug=slug)
    return render(request, "site/news_detail.html", {"news": news})


def events_list(request):
    queryset = _published_events().order_by("start_datetime")
    q = request.GET.get("q", "").strip()
    direction = request.GET.get("direction", "").strip()
    fmt = request.GET.get("format", "").strip()
    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(short_description__icontains=q) | Q(description__icontains=q))
    if direction:
        queryset = queryset.filter(direction__slug=direction)
    if fmt:
        queryset = queryset.filter(format=fmt)
    context = {
        "page_obj": _paginate(request, queryset, 9),
        "directions": Direction.objects.filter(is_active=True),
        "selected_direction": direction,
        "selected_format": fmt,
        "formats": Event.Format.choices,
        "q": q,
    }
    return render(request, "site/events_list.html", context)


def event_detail(request, slug):
    event = get_object_or_404(_published_events(), slug=slug)
    form = BaseApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.application_type = Application.Type.EVENT
        application.event = event
        application.save()
        messages.success(request, "Заявка на мероприятие отправлена. Сотрудник центра свяжется с вами.")
        return redirect("pages:event_detail", slug=event.slug)
    return render(request, "site/event_detail.html", {"event": event, "form": form})


def clubs_list(request):
    queryset = _active_clubs()
    q = request.GET.get("q", "").strip()
    direction = request.GET.get("direction", "").strip()
    fmt = request.GET.get("format", "").strip()
    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(short_description__icontains=q) | Q(description__icontains=q) | Q(leader_name__icontains=q))
    if direction:
        queryset = queryset.filter(direction__slug=direction)
    if fmt:
        queryset = queryset.filter(format=fmt)
    context = {
        "page_obj": _paginate(request, queryset, 9),
        "directions": Direction.objects.filter(is_active=True),
        "selected_direction": direction,
        "selected_format": fmt,
        "formats": Club.Format.choices,
        "q": q,
    }
    return render(request, "site/clubs_list.html", context)


def club_detail(request, slug):
    club = get_object_or_404(_active_clubs(), slug=slug)
    form = BaseApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.application_type = Application.Type.CLUB
        application.club = club
        application.save()
        messages.success(request, "Заявка в клуб или студию отправлена. Сотрудник центра свяжется с вами.")
        return redirect("pages:club_detail", slug=club.slug)
    return render(request, "site/club_detail.html", {"club": club, "form": form})


def documents(request):
    docs = Document.objects.filter(status=PublishStatus.PUBLISHED).select_related("category")
    return render(request, "site/documents.html", {"documents": docs})


def dobrocenter(request):
    page = DobroCenterPage.objects.filter(is_published=True).order_by("-updated_at").first()
    return render(request, "site/dobrocenter.html", {"page": page})


def contacts(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.application_type = Application.Type.FEEDBACK
        application.save()
        messages.success(request, "Сообщение отправлено. Спасибо за обращение!")
        return redirect("pages:contacts")
    return render(request, "site/contacts.html", {"locations": Location.objects.filter(is_active=True), "form": form})


def about(request):
    return render(request, "site/about.html")


def anticorruption(request):
    return render(request, "site/anticorruption.html")
