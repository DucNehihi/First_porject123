from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Thêm trường email, có thể bỏ ràng buộc nếu không cần
    first_name = forms.CharField(max_length=30, required=False)  # Thêm trường first_name
    last_name = forms.CharField(max_length=30, required=False)   # Thêm trường last_name

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']  # Cập nhật fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  # Lưu first_name
        user.last_name = self.cleaned_data['last_name']    # Lưu last_name
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'continent']
