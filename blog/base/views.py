from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm

# Create your views here.


def home(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'home.html', context)


def blog(request, pk):
    blogs = Blog.objects.get(id=pk)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)


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
