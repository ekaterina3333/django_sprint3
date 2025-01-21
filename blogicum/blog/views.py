from django.db.models.functions import Now
from django.shortcuts import render, get_object_or_404

from blog.constants import POST_COUNT
from blog.models import Post, Category


def posts(manager):
    return manager.filter(is_published=True,
                          pub_date__lte=Now(),
                          category__is_published=True,
                          ).select_related('category')


def index(request):
    template_name = 'blog/index.html'
    post_list = posts(Post.objects).order_by('-pub_date')[:POST_COUNT]
    context = {'post_list': post_list}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=post_id,
                             is_published=True,
                             pub_date__lte=Now(),
                             category__is_published=True)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = posts(Post.objects).filter(category=category)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
