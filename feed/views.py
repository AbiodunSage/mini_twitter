
from django.views.generic import TemplateView,DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from followers.models import Followers

from .models import Post


class HomePage(TemplateView):
    http_method_names = ['get']
    template_name = "feed/homepage.html"
    # model = Post
    # context_object_name = 'posts'
    # queryset = Post.objects.all().order_by('-id')[0:30]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.request.user.is_authenticated:
            following = list(
                Followers.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
            )
            if not following:
                posts = Post.objects.all().order_by('-id')[0:30]
            else:
                posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]
        else:
            posts = Post.objects.all().order_by('-id')[0:30]
        context['posts'] = posts

        return context
    


class PostDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "feed/new_post.html"
    fields = ['text']
    success_url = "/"

    
    def post (self, request, *args, **kwargs):

        post = Post.objects.create(
          text=request.POST.get("text"),
          author=request.user,
       )
        return render (
            request,
            "includes/post.html",
            {
                "post":post,
                "show_detail_Link":True,
            },
            content_type="application/html"
        )
      