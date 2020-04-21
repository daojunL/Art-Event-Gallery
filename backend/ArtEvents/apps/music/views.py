from django.shortcuts import render

# Create your views here.
def ShowEvents(request):
    """the music search page"""
    return render(request, 'MusicList.html')
