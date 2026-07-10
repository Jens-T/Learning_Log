from django import forms

from .models import Topic
from .models import Entry

from django.contrib.auth.models import User
from .models import TopicMember, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class TopicMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all()
    )

    class Meta:
        model = TopicMember
        fields = ['user', 'permission']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a reaction...'
            }),
        }