from django.db import models
import uuid
import os
# Create your models here.


def get_upload_path(instance, filename):  # Python 3: def __str__(self):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('kbase/images', filename)


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    intro = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    status = models.IntegerField(default=0)

    start_date = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    parent_id = models.IntegerField(default=0)

    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)

    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
