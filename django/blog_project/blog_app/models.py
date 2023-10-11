import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete

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
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    pic = models.ImageField(upload_to='images/')
 
    def __str__(self):
        return self.blog.title

@receiver(pre_delete, sender=BlogImage)
def delete_images(sender, instance, **kwargs):
    try:
        print(instance.pic.path)
        os.remove(instance.pic.path)
    except:
        pass