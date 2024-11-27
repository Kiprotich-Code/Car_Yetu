import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def images_list(request):
    response = requests.get('http://localhost:8000/api/slider_images/')
    data = response.json()  # Fetch data from your API
    return render(request, 'images/images_list.html', {'data': data})

def image_create(request):
    if request.method == 'POST' and request.FILES['image']:
        # Handle the image upload
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']

            # Save the image to the local file system
            # fs = FileSystemStorage()
            # filename = fs.save(image.name, image)
            # uploaded_file_url = fs.url(filename)

            api_url = 'http://localhost:8000/api/slider_images/'
            response = requests.post(api_url, data={'image': image, 'title': title})

            if response.status_code == 201:
                return redirect('images_list')
            else:
                # Handle any errors from the external API
                return render(request, 'images/images_list.html', {'error': 'Error uploading to API'})

    else:
        form = ImageUploadForm()

    return render(request, 'images/image_create.html', {'form': form})