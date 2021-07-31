from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse 
# Create your views here.

def home(request):
    user = request.user
    context = {
        'posts': Post.objects.all(),
        'user' : user,
    }
    return render(request,'blog/home.html',context)

# def likeHandler(request):
def like_post(request, pk):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    

    return redirect('post-detail', pk)


class PostListView(ListView):    #class based view.
  
      model = Post
      template_name = 'blog/home.html' # <app>/<model>_<view_type>.html
      context_object_name = 'posts'
      ordering=['-date_posted']
      paginate_by = 4


class UserPostListView(ListView):  # class based view.
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self): #limit post to specific user.
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):  # class based view.
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)

        post_obj = get_object_or_404(Post, id = self.kwargs['pk'])
        total_likes = post_obj.total_likes()

        liked = False
        if post_obj.likes.filter(id = self.request.user.id).exists():
            liked = True 
        
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context 

class PostCreateView(LoginRequiredMixin, CreateView):  # class based view.
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #to form a post.
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # class based view.
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #to form a post.
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # class based view to delete post.
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})