from django.db import models

# Create your models here.
class Box(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # can you still add papers?
    open = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Paper(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    # text on paper
    content = models.TextField()
    # who currently has the paper open
    holder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.content
