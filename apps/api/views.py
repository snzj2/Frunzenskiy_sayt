from django.http import JsonResponse
from django.utils import timezone

from apps.clubs.models import Club
from apps.core.models import Location, PublishStatus
from apps.events.models import Event
from apps.news.models import News


def health(request):
    return JsonResponse({"status": "ok"})


def _absolute_media_url(request, field):
    if not field:
        return None
    try:
        return request.build_absolute_uri(field.url)
    except ValueError:
        return None


def news_list(request):
    queryset = News.objects.filter(status=PublishStatus.PUBLISHED).select_related("direction", "author")
    search = request.GET.get("q")
    if search:
        queryset = queryset.filter(title__icontains=search)
    data = [
        {
            "id": item.id,
            "title": item.title,
            "slug": item.slug,
            "short_description": item.short_description,
            "direction": item.direction.title if item.direction else None,
            "published_at": item.published_at.isoformat() if item.published_at else None,
            "preview_image": _absolute_media_url(request, item.preview_image),
        }
        for item in queryset[:50]
    ]
    return JsonResponse({"results": data})


def event_list(request):
    queryset = Event.objects.filter(status=Event.Status.PUBLISHED).select_related("direction", "location")
    date_from = request.GET.get("date_from")
    direction = request.GET.get("direction")
    if date_from:
        queryset = queryset.filter(start_datetime__date__gte=date_from)
    if direction:
        queryset = queryset.filter(direction__slug=direction)
    data = [
        {
            "id": item.id,
            "title": item.title,
            "slug": item.slug,
            "short_description": item.short_description,
            "start_datetime": item.start_datetime.isoformat(),
            "end_datetime": item.end_datetime.isoformat() if item.end_datetime else None,
            "format": item.format,
            "direction": item.direction.title if item.direction else None,
            "location": item.location.title if item.location else None,
            "address": item.location.address if item.location else None,
            "age_min": item.age_min,
            "age_max": item.age_max,
            "registration_available": item.is_registration_available,
            "preview_image": _absolute_media_url(request, item.preview_image),
        }
        for item in queryset.order_by("start_datetime")[:100]
    ]
    return JsonResponse({"now": timezone.now().isoformat(), "results": data})


def club_list(request):
    queryset = Club.objects.exclude(status=Club.Status.ARCHIVED).select_related("direction", "location")
    direction = request.GET.get("direction")
    fmt = request.GET.get("format")
    if direction:
        queryset = queryset.filter(direction__slug=direction)
    if fmt:
        queryset = queryset.filter(format=fmt)
    data = [
        {
            "id": item.id,
            "title": item.title,
            "slug": item.slug,
            "short_description": item.short_description,
            "direction": item.direction.title if item.direction else None,
            "location": item.location.title if item.location else None,
            "address": item.location.address if item.location else None,
            "format": item.format,
            "schedule": item.schedule,
            "age_min": item.age_min,
            "age_max": item.age_max,
            "leader_name": item.leader_name,
            "status": item.status,
            "preview_image": _absolute_media_url(request, item.preview_image),
        }
        for item in queryset[:100]
    ]
    return JsonResponse({"results": data})


def location_list(request):
    queryset = Location.objects.filter(is_active=True)
    data = [
        {
            "id": item.id,
            "title": item.title,
            "address": item.address,
            "latitude": str(item.latitude) if item.latitude is not None else None,
            "longitude": str(item.longitude) if item.longitude is not None else None,
            "working_hours": item.working_hours,
            "phone": item.phone,
            "email": item.email,
            "yandex_map_url": item.yandex_map_url,
        }
        for item in queryset
    ]
    return JsonResponse({"results": data})
