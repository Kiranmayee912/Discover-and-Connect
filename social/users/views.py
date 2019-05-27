from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,InterestUpdateForm
from blog.models import Upload
from .models import Friend,Interest
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage 


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Acrivate your account'
            message = render_to_string('users/acc_active_email.html', {
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete your registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def myposts(request):
    q2 = Upload.objects.filter(author=request.user).order_by('date_posted')
    return render(request,'users/myposts.html',{'uploads':q2})

@login_required
def profile(request):
    inter = Interest.objects.get_or_create(user_id=request.user.id)
    inter=inter[0]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        i_form = InterestUpdateForm(request.POST,instance=inter)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        if i_form.is_valid():
            m = i_form.save(commit=False)
            m.user = request.user
            m.save()
            messages.success(request, f'Your Intersets has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        i_form = InterestUpdateForm(instance=inter)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'i_form':i_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def change_friends(request,pk, operation):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.addfriend(request.user, friend)
    elif operation == 'remove':
        Friend.removefriend(request.user, friend)
    return redirect('timeline',pk=pk)

@login_required
def friendlist(request):
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = None
    return render(request, 'users/friendlist.html', {'friends': friends})
