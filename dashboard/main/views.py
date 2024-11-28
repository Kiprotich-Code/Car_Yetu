import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def images_list(request):
    # Get the current page number (default to 1 if not provided)
    page_number = int(request.GET.get('page', 1))
    per_page = 9  # Number of items per page

    # Calculate the offset for LimitOffsetPagination
    offset = (page_number - 1) * per_page

    # Fetch data from the API with limit and offset
    api_url = f'http://localhost:8000/api/slider_images/?limit={per_page}&offset={offset}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # Extract required data
        results = data.get('results', [])
        count = data.get('count', 0)
        next_url = data.get('next')
        previous_url = data.get('previous')

        # Calculate total pages
        total_pages = (count + per_page - 1) // per_page  # Ceiling division

        # Prepare context for the template
        context = {
            'results': results,  # Items for the current page
            'count': count,  # Total number of items
            'page_number': page_number,  # Current page number
            'total_pages': total_pages,  # Total number of pages
            'has_next': next_url is not None,
            'has_previous': previous_url is not None,
            'next_page': page_number + 1 if next_url else None,
            'previous_page': page_number - 1 if previous_url else None,
        }

        return render(request, 'images/images_list.html', context)
    else:
        return render(
            request,
            'images/images_list.html',
            {'error': 'Failed to fetch images from the API.'},
        )


def image_create(request):
    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']

            # Save the image to the local file system
            api_url = 'http://localhost:8000/api/slider_images/'
            files = {'image': image}  # Send the file directly
            data = {'title': title}  # Other fields
            response = requests.post(api_url, files=files, data=data)

            if response.status_code == 201:
                return redirect('images_list')
            else:
                # Log API response for debugging
                print("API Error:", response.text)
                return redirect('images_list', {'error': response.text})

    else:
        form = ImageUploadForm()

    return render(request, 'images/image_create.html', {'form': form})
