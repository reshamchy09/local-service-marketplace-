from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from providers.forms import ProviderPostForm, ServiceProfileForm
from providers.models import Provider, ProviderPost, ServiceProfile
from django.contrib.auth import logout


@login_required
def provider_dashboard(request):
    user = request.user

    if not hasattr(user, "provider"):
        return redirect("login")

    provider = user.provider
    service_profile = ServiceProfile.objects.filter(user=user).first()  # fix here

    if service_profile is None:
        return redirect("provider_profile")

    trial_expired = provider.is_trial_expired()
    if trial_expired:
        return redirect("subscription")

    return render(request, "provider_dashboard.html", {
        "provider": provider,
        "service_profile": service_profile,
        "trial_expired": trial_expired,
        "is_approved": service_profile.is_approved,
    })

@login_required
def create_service_profile(request):
    profile = ServiceProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        profile_form = ServiceProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_obj = profile_form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()

            service_names = request.POST.getlist("service_name")
            service_rates = request.POST.getlist("rate")

            profile_obj.services.all().delete()

            for name, rate in zip(service_names, service_rates):
                name = name.strip()
                rate = rate.strip()
                if name and rate:
                    try:
                        profile_obj.services.create(
                            service_name=name,
                            rate=float(rate)
                        )
                    except (ValueError, TypeError):
                        pass

            return redirect("provider_dashboard")

    else:
        profile_form = ServiceProfileForm(instance=profile)

    return render(request, "create_profile.html", {"form": profile_form})





@login_required
def create_post(request):
    if request.method == "POST":
        form = ProviderPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("provider_posts")
    else:
        form = ProviderPostForm()

    return render(request, "create_post.html", {"form": form})


@login_required
def provider_posts(request):
    posts = ProviderPost.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "post_list.html", {"posts": posts})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(ProviderPost, id=pk, user=request.user)

    form = ProviderPostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect("provider_posts")

    return render(request, "create_post.html", {"form": form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(ProviderPost, id=pk, user=request.user)

    if request.method == "POST":
        post.delete()

    return redirect("provider_posts")

def logout_view(request):
    logout(request)  # properly clears auth session
    return redirect("login")