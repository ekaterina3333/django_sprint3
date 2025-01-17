from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from datetime import datetime


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.filter(is_published=True,
                                    category__is_published=True,
                                    pub_date__lt=datetime.now())[0:5]
    context = {'post_list': post_list}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=post_id,
                             is_published=True,
                             pub_date__lte=datetime.now(),
                             category__is_published=True)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = Post.objects.filter(category=category, is_published=True,
                                    pub_date__lte=datetime.now())
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
