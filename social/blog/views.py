from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from .models import Upload
from users.models import Friend 
from django.contrib.auth.models import User
 
def home(request):
    if request.user.is_authenticated:
        f1 = []
        f1 = list(Upload.objects.filter(author=request.user)) 
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            for f in friends:
                k = Upload.objects.filter(author=f)
                for u in k:
                    f1.append(u)
        except Friend.DoesNotExist:
            friends = None 
        f1.sort(key=lambda x: x.date_posted, reverse=True)
        return render(request, 'blog/home.html', {'posts': f1})
    return render(request,'blog/welcome.html')

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

@login_required
def search(request):
    u=request.GET.get('u')
    susers=User.objects.filter(username__icontains=u)
    current_user = request.user
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = None
    return render(request,'blog/search.html',{'susers':susers,'friends':friends,'cuser':current_user})

@login_required
def timeline(request,pk):
    q2 = Upload.objects.filter(author__pk=pk).order_by('-date_posted')
    u = User.objects.filter(id=pk).first()
    current_user=request.user
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = None
    return render(request, 'blog/timeline.html', {'uploads': q2, 'user': u, 'friends': friends,'cuser':current_user})
'''
@login_required
def uploadlist(request):
    f1=[]
    f1= list(Upload.objects.filter(author=request.user))
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        for f in friends:
            k = Upload.objects.filter(author=f)
            for u in k:
                f1.append(u)
    except Friend.DoesNotExist:
        friends = None
    f1.sort(key= lambda x:x.date_posted,reverse=True)
    return render(request,'blog/upload_home.html',{'posts':f1})

'''
class UploadDetailView(LoginRequiredMixin,DetailView):
    model = Upload


class UploadCreateView(LoginRequiredMixin, CreateView):
    model = Upload
    fields = ['title','caption','image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UploadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Upload
    fields = ['title','caption','image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UploadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Upload
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
