from django.views.generic import TemplateView
from django.views import generic
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


class HomePageView(TemplateView):
    template_name = 'home.html'

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


"""
def RegisterPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Konto zostało utworzone dla ' + user)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html', context)

def LoginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Podano błędną nazwę użytkownika lub hasło')

    context = {}
    return render(request,'accounts/login.html', context)

def LogoutUser(request):
    return render(request,'home')

"""
