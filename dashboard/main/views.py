import requests
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def index(request):
    return render(request, 'index.html', {})

def images_list(request):
    # Get the current page number (default to 1 if not provided)
    page_number = int(request.GET.get('page', 1))
    per_page = 9  # Number of items per page

    # Calculate the offset for LimitOffsetPagination
    offset = (page_number - 1) * per_page

    # Fetch data from the API with limit and offset
    api_url = f'https://test.api.bellyone.co.ke/api/slider_images/?limit={per_page}&offset={offset}'
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

# DETAIL VIEW IMAGE 
def image_detail(request, image_id):
    api_url = f'https://test.api.bellyone.co.ke/api/slider_images/{image_id}/'
    response = requests.get(api_url)

    if response.status_code == 200:
        image_data = response.json()
        return render(request, 'images/image_detail.html', {'image': image_data})
    else:
        # Handle error if the API fails
        return render(
            request,
            'images/image_detail.html',
            {'error': 'Unable to fetch image details.'},
        )


# CREATE IMAGE 
@login_required()
def image_create(request):
    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']

            # Save the image to the local file system
            api_url = 'https://test.api.bellyone.co.ke/api/slider_images/'
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

# UPDATE IMAGE
@login_required()
def image_update(request, image_id):
    api_url = f'https://test.api.bellyone.co.ke/api/slider_images/{image_id}/'
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            image = request.FILES.get('image')  # Handle image only if updated

            # Prepare the data for the API
            data = {'title': title}
            files = {'image': image} if image else None

            response = requests.put(api_url, data=data, files=files)

            if response.status_code == 200:
                return redirect('images_list')  # Redirect to list view after successful update
            else:
                return render(
                    request,
                    'images/image_update.html',
                    {
                        'form': form,
                        'error': 'Failed to update the image.',
                    },
                )
    else:
        # Fetch current data to populate the form
        response = requests.get(api_url)
        if response.status_code == 200:
            current_data = response.json()
            form = ImageUploadForm(initial={'title': current_data.get('title')})
        else:
            return redirect('images_list')  # Redirect if unable to fetch data

    return render(request, 'images/image_update.html', {'form': form})


# DELETE IMAGE
@login_required()
def image_delete(request, image_id):
    api_url = f'https://test.api.bellyone.co.ke/api/slider_images/{image_id}/'
    if request.method == 'POST':
        response = requests.delete(api_url)

        if response.status_code == 204:  # Successful deletion
            return redirect('images_list')
        else:
            return render(
                request,
                'images/image_delete.html',
                {'error': 'Failed to delete the image.'},
            )

    # Render confirmation page
    return render(request, 'images/image_delete.html', {'image_id': image_id})
