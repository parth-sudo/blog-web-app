from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)

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