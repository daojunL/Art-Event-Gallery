from django.shortcuts import render

# Create your views here.
def home(request):
    """the homepage view"""
    return render(request, 'HomePage.html')

