import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def images_list(request):
    response = requests.get('http://localhost:8000/api/slider_images/')
    data = response.json()  # Fetch data from your API
    return render(request, 'images/images_list.html', {'data': data})