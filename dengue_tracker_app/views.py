from django.shortcuts import render

def home_page(request):
    return render(request, 'home_page.html')

def list_cases(request):
    return render (request, 'cases_registered.html')