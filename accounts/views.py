from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return render(request, 'registration.html', {'form': form})

    else:
        form = CustomUserCreationForm()
        return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"[DEBUG] Email: {email}, Password: {password}")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('lk')
            else:
                messages.error(request, 'Аккаунт неактивен.')
        else:
            messages.error(request, 'Неверные email или пароль.')

    return render(request, 'auth.html')


@login_required
def lk_view(request):
    return render(request, 'lk.html')