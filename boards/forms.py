from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Topic, Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class NewTopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Enter topic title...',
                'maxlength': 50,
                'class': 'form-control'
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError("Title is required.")
        if len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title.strip()

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'placeholder': 'Write your post content here...',
                'rows': 4,
                'class': 'form-control'
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError("Content is required.")
        if len(content.strip()) < 5:
            raise forms.ValidationError("Content must be at least 5 characters long.")
        return content.strip()
