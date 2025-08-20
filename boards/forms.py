from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter topic title...',
                'maxlength': 50,
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError("Title is required.")
        if len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title.strip()

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post content here...',
                'rows': 4,
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError("Content is required.")
        if len(content.strip()) < 5:
            raise forms.ValidationError("Content must be at least 5 characters long.")
        return content.strip()