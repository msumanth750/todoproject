from django.db import models
from django.urls import reverse

# Create your models here.

class Todo(models.Model):
    STATUS=(
        ("in progress" , "In Progress"),
        ("completed","Completed"),
        ("pending","Pending")
    )
    Title = models.CharField(max_length=50)
    Description = models.TextField()
    Datetime = models.DateTimeField()
    Status = models.CharField(max_length=20,choices=STATUS)
    CreatedAt = models.DateField(auto_now_add=True)
    ModifiedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Title;

    def get_absolute_url(self):
        return reverse('todo-detail',kwargs={'pk':self.pk})
