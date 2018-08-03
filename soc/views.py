from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, DetailView

from .forms import SignUpForm, UserInformationUpdateForm, CreatePostForm
from .models import Post
from .models import User


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


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'


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


@login_required
def new_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.by_user = request.user
            post.save()
            return redirect('home')
    else:
        form = CreatePostForm()
    return render(request, 'create_post.html', {'form': form})


def handle_uploaded_file(f):
    destination = open('root', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
