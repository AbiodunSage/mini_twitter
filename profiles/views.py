from django.contrib.auth.models import User
from django.views.generic import DetailView, View,UpdateView
from feed.models import Post
from django.http import JsonResponse,HttpResponseBadRequest
from django.shortcuts import render
from .models import Profile
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy


from followers.models import Followers
# Create your views here.


class ProfileDetailView(DetailView):
    http_method_names = ['get']
    model= User
    template_name='profiles/detail.html'
    context_object_name="user"
    slug_field="username"
    slug_url_kwarg="username"

    def dispatch(self,request,*args,**kwargs):
        self.request=request

        return super().dispatch(request,*args,**kwargs)
    

    def get_context_data(self,**kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Followers.objects.filter(followed_by=user).count()

        if self.request.user.is_authenticated:
             context['you_follow']= Followers.objects.filter(following=user,followed_by=self.request.user).exists()
        return context
    

class ProfileUpdateView(UpdateView):
     model = Profile
     form_class = ProfileUpdateForm
     template_name='profiles/update.html'


     def get_success_url(self):
        return reverse_lazy('profile:detail', kwargs={'username': self.object.user.username})


     def get_form_kwargs(self):
          kwargs = super().get_form_kwargs()
          kwargs['user'] = self.request.user
          return kwargs

     def get_object(self, queryset=None):
          content =Profile.objects.get(user__username=self.kwargs['username'])
          return content

class FollowView(View):
        http_method_names = ['post']
        

       
        def post(self, request, *args, **kwargs):
            data = request.POST.dict()
            
            if "action" not in data or "username" not in data:
                return HttpResponseBadRequest("Missing Data")
            
            try:
                 other_user = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                 return HttpResponseBadRequest("Missing Username")
            
            if data['action'] == 'follow':
                 #Follow
                 follower,created = Followers.objects.get_or_create(
                      followed_by=request.user,
                      following=other_user
                 )
            else:
                 #Unfollow
                try:
                    follower = Followers.objects.get(
                        followed_by=request.user,
                        following=other_user
                 )
                except Followers.DoesNotExist:
                     follower=None
                if follower:
                     follower.delete()
                

            return JsonResponse({
                  'success': True,
                  'wording': "Unfollow" if data['action']=="follow" else "Follow"
             })
