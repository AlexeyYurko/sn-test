from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, DetailView

from .forms import SignUpForm, UserInformationUpdateForm
from .models import Post
from .models import UserProfile as User


class BoardListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'home.html'


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user_detail.html'


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users_list.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
