from django.db import models

class Gesture(models.Model):
    name= models.CharField(max_length=200)
    gestureNum= models.IntegerField()
    moveX= models.IntegerField()
    moveY= models.IntegerField()
    
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    date= models.DateTimeField('date published')
    image= models.ImageField(upload_to='images/',blank=True, null= True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)