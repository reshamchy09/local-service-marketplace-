from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import FAQ
from dealers.models import Dealer
from providers.models import Provider, ServiceProfile, ProviderPost
from django.db.models import Q
from .utils import get_distance_km


def login_view(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")

def faq_page(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'faq.html', {'faqs': faqs})

def about(request):
    return render(request, "about.html")

def terms(request):
    return render(request, "terms.html")

def privacy(request):
    return render(request, "privacy.html")


def home(request):
    query = request.GET.get("q", "")

    user_lat = request.GET.get("lat")
    user_lng = request.GET.get("lng")

    profiles = ServiceProfile.objects.filter(is_active=True, is_approved=True)

    # SEARCH
    if query:
        profiles = profiles.filter(
            Q(business_name__icontains=query) |
            Q(location__icontains=query) |
            Q(phone__icontains=query) |
            Q(user__username__icontains=query) |
            Q(service_type__icontains=query)
        )

    results = []

    # IF LOCATION AVAILABLE → CALCULATE DISTANCE
    if user_lat and user_lng:
        user_lat = float(user_lat)
        user_lng = float(user_lng)

        for p in profiles:
            if p.latitude and p.longitude:
                distance = get_distance_km(
                    user_lat, user_lng,
                    p.latitude, p.longitude
                )
            else:
                distance = None

            results.append({
                "profile": p,
                "distance": distance
            })

        # SORT BY DISTANCE (nearest first)
        results.sort(key=lambda x: x["distance"] if x["distance"] is not None else 999999)

    else:
        # fallback without location
        for p in profiles:
            results.append({
                "profile": p,
                "distance": None
            })

    # rating sort inside same distance mode
    if not (user_lat and user_lng):
        results.sort(key=lambda x: (x["profile"].average_rating, x["profile"].review_count), reverse=True)

    return render(request, "home.html", {
        "results": results,
        "query": query
    })

def provider_detail(request, pk):
    profile = get_object_or_404(
        ServiceProfile,
        id=pk,
        is_active=True,
        is_approved=True
    )

    services = profile.services.all()

    # 🔥 GET POSTS OF THIS PROVIDER (user linked)
    posts = ProviderPost.objects.filter(user=profile.user).order_by("-created_at")

    return render(request, "provider_detail.html", {
        "profile": profile,
        "services": services,
        "posts": posts
    })


def become_provider(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            return render(request, "provider_signup.html", {"error": "Email already registered."})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Provider.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
        )

        return redirect("login")

    return render(request, "provider_signup.html")


def become_dealer(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        business_name = request.POST.get("business_name")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            return render(request, "dealer_signup.html", {"error": "Email already registered."})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Dealer.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            business_name=business_name,
        )

        return redirect("login")

    return render(request, "dealer_signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, "provider"):
                return redirect("provider_dashboard")
            elif hasattr(user, "dealer"):
                return redirect("dealer_dashboard")
            return redirect("home")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def public_services(request):
    services = ServiceProfile.objects.filter(is_active=True, is_approved=True)

    # optional selected profile (for detail view in same page)
    profile_id = request.GET.get("profile")
    selected_profile = None

    if profile_id:
        selected_profile = get_object_or_404(
            ServiceProfile,
            id=profile_id,
            is_active=True,
            is_approved=True
        )

    return render(request, "service_list.html", {
        "services": services,
        "selected_profile": selected_profile
    })