from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     message= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email


class Feedback(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     message= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "feedback from " + self.name + ' - ' + self.email


class IpModel(models.Model):
    ip=models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Blog(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=20)
    sub_head=models.CharField(max_length=100)
    image=models.ImageField(upload_to='blog/img',default="")
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    views=models.ManyToManyField(IpModel,related_name='post_views',blank=True)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()


    def __str__(self):
        return self.name

    def total_views(self):
        return self.views.count()


class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username





class Python(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()

    def __str__(self):
        return self.name




class Projects(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=20)
    image=models.ImageField(upload_to='projects/img',default="")
    views=models.ManyToManyField(IpModel,related_name='project_views',blank=True)
    likes = models.ManyToManyField(User,related_name='projectlike', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()


    def __str__(self):
        return self.name

    def total_views(self):
        return self.views.count()
