from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm, UserForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


def home(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'home.html', context)


def blog(request, pk):
    read_blogs_id =  request.session.get('read_blog',[])
    if 'read_blog' not in request.session:
        request.session['read_blog'] = []
    if pk not in read_blogs_id:
        request.session['read_blog'].insert(0, pk)
        request.session.modified = True
    blogs = Blog.objects.get(id=pk)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)


def user_history(request):
    read_blog_ids = request.session.get('read_blog', [])[::-1]
    read_history = Blog.objects.filter(id__in=read_blog_ids).order_by('id')
    context = {'read_history': read_history}
    return render(request, 'history.html', context)


def delete_read_history(request, pk):
    read_blog_ids = request.session.get('read_blog', [])
    if pk in read_blog_ids:
        read_blog_ids.remove(pk)
        request.session['read_blog'] = read_blog_ids
        request.session.modified = True
    return redirect('history')


@login_required(login_url='login')
def create_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        author = request.user
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = author
            blog.save()
            return redirect('home')
    context = { 'form': form }
    return render(request, "create_blog.html", context)


def update_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST,  request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = { 'form': form }
    return render(request, "create_blog.html", context)


def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return redirect('home')


def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect Password")
    context = {'page': page}
    return render(request, 'login_register.html', context)

def Logout(request):
    logout(request)
    return redirect('home')


def register(request):
    page = 'register'
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)


def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user_profile.html', context)



def updateUser(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'update-user.html', {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
