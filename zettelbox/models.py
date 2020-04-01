from django.db import models

# Create your models here.
class Box(models.Model):
    name = models.CharField(max_length=200)
    # is somebody currently looking at a paper from the box?
    open = models.BooleanField(default=False)
    # can you still add papers?
    full = models.BooleanField(default=False)
    # who has the box?
    holder = models.CharField(max_length=200)



class Paper(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    # text on paper
    content = models.TextField()
    # is it inside the box or outside?
    inside = models.BooleanField(default=True)
