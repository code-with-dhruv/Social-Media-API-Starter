# authentication/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import NoPasswordConfirmationUserCreationForm

class SignUpView(View):
    def get(self, request):
        form = NoPasswordConfirmationUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = NoPasswordConfirmationUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the password manually since password2 is removed
            user.set_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']  # Save the email
            user.save()
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('api')  # Replace 'api' with your desired URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

def logout_view(request):
    logout(request)
    return redirect('login')
