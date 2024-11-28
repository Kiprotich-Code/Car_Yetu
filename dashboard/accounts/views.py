from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomerRegisterForm
from django.contrib import messages

# Create your views here.
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'customer'
            user.save()
            messages.success(request, ('Successfully registered!'))
            return redirect('login')

        else:
            messages.error(request, 'Enter Valid Details and Try Again!')
        
    else:
        form = CustomerRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register_customer.html', context)

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            
            # redirect users based on role            
            if user.is_staff:
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            
            else:
                messages.success(request, 'Login successful!')
                return redirect('user_dashboard')
        
        else:
            messages.error(request, 'User Does Not Exist!')
            return redirect('login')

    else:
        form = LoginForm()
    context = {
        'form': form
    }
        
    return render(request, 'login.html', context)


def signout(request):
    logout(request)
    return redirect('home')