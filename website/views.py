from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Contact, Feedback, GalleryImage, Quote

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and phone and message:
            Quote.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            return redirect("home")

    return render(request, "index.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            return redirect("contact")
    return render(request, "contact.html")


def projects(request):
    if request.method == "POST":
        name = request.POST.get("feedback_name")
        location = request.POST.get("feedback_location")
        message = request.POST.get("feedback_message")
        rating = request.POST.get("feedback_rating", "5")

        if name and location and message:
            try:
                rating_value = int(rating)
            except (TypeError, ValueError):
                rating_value = 5

            rating_value = max(1, min(5, rating_value))
            Feedback.objects.create(
                name=name,
                location=location,
                rating=rating_value,
                message=message
            )
            
            return redirect("projects")
    feedbacks = list(Feedback.objects.all()[:8])
    return render(request, "projects.html", {"feedbacks": feedbacks})
def about(request):
    return render(request, 'about.html')

def gallery(request):
    gallery_images = GalleryImage.objects.filter(is_active=True)
    return render(request, 'gallery.html', {"gallery_images": gallery_images})

#Our Solar Products


def tata(request):
    return render(request, 'tata.html')

def waaree(request):
    return render(request, 'waaree.html')

def adani(request):
    return render(request, 'adani.html')

def premier(request):
    return render(request, 'premier.html')

def utl(request):
    return render(request, 'utl.html')

#Our Services
def residential(request):
    return render(request, 'residential.html')

def commercial(request):
    return render(request, 'commercial_solar.html')

def industrial(request):
    return render(request, 'industrial_solar.html')

def solar_maintenance(request):
    return render(request, 'solar_maintenance.html')


def project_documentation(request):
    documentation_path = Path(settings.BASE_DIR) / "PROJECT_DOCUMENTATION.md"
    if not documentation_path.exists():
        raise Http404("Project documentation not found.")

    return HttpResponse(
        documentation_path.read_text(encoding="utf-8"),
        content_type="text/markdown; charset=utf-8",
    )
