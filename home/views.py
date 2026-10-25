import json
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Service, Skill, Project, Review, ContactMessage
from django.conf import settings
from django.core.mail import send_mail

def index(request, section=None):
    skills = list(Skill.objects.filter(visible=True).values("name", "cat", "icon", "desc"))
    services = list(Service.objects.filter(visible=True).values("icon", "title", "desc"))

    projects = []
    for p in Project.objects.filter(visible=True).prefetch_related("screenshots"):
        projects.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "category": p.category,
            "technologies": [t.strip() for t in p.technologies.split(",") if t.strip()],
            "frontend": p.frontend,
            "backend": p.backend,
            "integrations": p.integrations,
            "date": p.date.isoformat() if p.date else "",
            "status": p.status,
            "image": p.image.url if p.image else "",
            "screenshots": [s.image.url for s in p.screenshots.all() if s.image],
            "liveUrl": p.live_url,
            "sourceUrl": p.source_url,
        })

    reviews = [
        {"name": r.name, "comment": r.comment, "date": r.created.isoformat()}
        for r in Review.objects.filter(approved=True)[:50]
    ]

    context = {
        "name": "Muhammad Abdullah Nasir",
        "currentClass": "11th year",
        "studyStatus": "Currently studying",
        "ResponseTime": "Within 24 hours",
        "title": "Muhammad Abdullah Bajwa | Portfolio",
        "description": "Muhammad Abdullah Nasir (Abdullah Bajwa) is a web developer and designer based in Faisalabad, Punjab, Pakistan.",
        "reviewsApproval": "witin 24 hours ", #after approval  
        "skills": skills,
        "projects": projects,
        "services": services,
        "reviews": reviews,
    }
    return render(request, "index.html", context)

def notify(subject, body):
    if not getattr(settings, "NOTIFY_EMAIL", ""):
        return
    try:
        send_mail(subject, body, None, [settings.NOTIFY_EMAIL])
    except Exception:
        pass

@require_POST
def submit_review(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({"error": "Invalid request."}, status=400)

    if data.get("website"):                      # hidden trap field: only bots fill it
        return JsonResponse({"ok": True})

    name = str(data.get("name", "")).strip()[:60]
    email = str(data.get("email", "")).strip()[:120]
    comment = str(data.get("comment", "")).strip()[:500]

    if len(name) < 2 or len(comment) < 5:
        return JsonResponse({"error": "Please enter your name and a comment."}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Please enter a valid email address."}, status=400)

    sent = request.session.get("review_count", 0)
    if sent >= 3:
        return JsonResponse({"error": "Review limit reached for this browser session."}, status=429)

    Review.objects.create(name=name, email=email, comment=comment) 
    notify("New review on your portfolio", f"From: {name} <{email}>\n\n{comment}\n\nApprove it in the admin panel.")  # approved=False by default
    request.session["review_count"] = sent + 1
    return JsonResponse({"ok": True})

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: " + request.build_absolute_uri("/sitemap.xml"),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    url = request.build_absolute_uri("/")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f"<url><loc>{url}</loc></url></urlset>")
    return HttpResponse(xml, content_type="application/xml")

@require_POST
def submit_contact(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({"error": "Invalid request."}, status=400)

    if data.get("website"):
        return JsonResponse({"ok": True})

    name = str(data.get("name", "")).strip()[:60]
    email = str(data.get("email", "")).strip()[:120]
    message = str(data.get("message", "")).strip()[:1000]

    if len(name) < 2 or len(message) < 10:
        return JsonResponse({"error": "Please enter your name and a message."}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Please enter a valid email address."}, status=400)

    sent = request.session.get("contact_count", 0)
    if sent >= 5:
        return JsonResponse({"error": "Message limit reached. Please email me directly."}, status=429)

    ContactMessage.objects.create(name=name, email=email, message=message)
    request.session["contact_count"] = sent + 1
    notify("New message from your portfolio", f"From: {name} <{email}>\n\n{message}")
    return JsonResponse({"ok": True})