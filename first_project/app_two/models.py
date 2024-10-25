from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)

    def __str__(self):
        return self.top_name

class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Thêm on_delete
    name = models.CharField(max_length=264)
    url = models.URLField()

    def __str__(self):
        return self.name
class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage,on_delete=models.CASCADE,)
    date = models.DateField()
    def __str__(self):
        return self.date

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.id}/"



from ckeditor.fields import RichTextField
class Post(models.Model):
    CONTINENT_CHOICES = [
        ("Asia", "Asia"),
        ("Europe", "Europe"),
        ("Africa", "Africa"),
        ("North America", "North America"),
        ("South America", "South America"),
        ("Oceania", "Oceania"),
    ]
    title = models.CharField(max_length=255)  # Đảm bảo rằng bạn có trường này
    content = RichTextField() 
    continent = models.CharField(max_length=20, choices=CONTINENT_CHOICES, default="Asia")  # Chọn châu lục
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Tự động tạo thời gian khi tạo bài viết
    is_draft = models.BooleanField(default=True)  # Đánh dấu bài nháp
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

def __str__(self):
        return self.content[:50] 




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)  
    liked_users = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
    


class PostAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(max_length=10)  # "like" hoặc "dislike"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')    
from django import forms
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'continent', 'content', 'image']