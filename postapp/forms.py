from django import forms 
from postapp.models import Ticket, Comment, UserFollows, profilemodel


class Ticketform(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=("title", "description", "image")
        widgets={'description':forms.Textarea(attrs={'id':'text_id'}),
                 'title':forms.TextInput(attrs={'id':'title_id'}),
                 'image':forms.FileInput(attrs={'required':False})}

class Reviewform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        
        widgets={'body':forms.Textarea(attrs={'required':True,
                                              'placeholder':"Write a comment"})}
           
                 


class Userfollowsform(forms.ModelForm):
    class Meta:
        model=UserFollows
        fields=["followed_user"]

class profilform(forms.ModelForm):
    class Meta:
        model=profilemodel
        fields=("image","description","gender")      