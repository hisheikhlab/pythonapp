from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=600)
    Content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='static/')
    print(blog)

    def __str__(self):
        return self.blog.title
