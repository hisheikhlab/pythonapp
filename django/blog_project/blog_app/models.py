from django.db import models

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=600)
    Content = models.TextField()
    pic = models.ImageField(upload_to='static')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




