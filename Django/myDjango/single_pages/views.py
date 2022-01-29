from django.shortcuts import render
from blog.models import Post, Category

# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    catagories = Category.name
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
            'categories': categories,
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )