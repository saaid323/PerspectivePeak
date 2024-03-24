from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'home.html', context)


def blog(request, pk):
    blogs = Blog.objects.get(id=pk)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)


@login_required(login_url='login')
def create_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
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