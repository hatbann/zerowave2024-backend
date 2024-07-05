from django.db import models

# Create your models here.
class BoardModel(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    views = models.IntegerField(default=0)
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('user.ZerowaveUser', on_delete=models.CASCADE, related_name='author_of')
    location = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=100, blank=True, default='')


    def increase_view_count(self):
        self.views = self.views + 1
        self.save(update_fields=['views'])