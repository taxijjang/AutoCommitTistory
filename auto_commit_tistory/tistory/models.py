from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1000)
    postUrl = models.CharField(max_length=2000)
    content = models.TextField(default='')
    visibility = models.IntegerField(default=0)
    categoryId = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    trackbacks = models.IntegerField(default=0)
    date = models.DateTimeField()
    auto_commit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.title}'