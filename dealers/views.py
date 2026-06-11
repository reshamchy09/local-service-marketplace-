from django.shortcuts import render

def dealer_dashboard(request):
    return render(request, "dealer_dashboard.html")