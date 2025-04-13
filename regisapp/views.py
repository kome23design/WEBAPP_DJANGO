from django.shortcuts import render
from django.shortcuts import redirect
from regisapp.forms import Inscription
from django.contrib.auth import logout

# Create your views here.

def Register(request):
    if request.method=="POST":
        reg=Inscription(request.POST)
        if reg.is_valid():
            new_user=reg.save(commit=False)
            new_user.set_password(
                reg.cleaned_data.get('password')
            )
            new_user.save()
            return redirect('regisapp:login_page')
    else:
        form=Inscription()
        return render(request,'regisapp/register.html',{'form':form})
    
def logout_view(request):
    logout(request)
    return redirect("regisapp:login_page")