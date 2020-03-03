from django.db import models
import uuid
import os
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator, \
                                    validate_image_file_extension


def get_upload_path(instance, filename):  # Python 3: def __str__(self):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('recognition', filename)


class RecognitionElement(models.Model):
    label = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=get_upload_path,
        validators=[validate_image_file_extension]
    )
    modelo = models.TextField()
    descripcion = models.TextField()
    month = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
     )
    year = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    estimated_date = models.DateField(default='')
    note_img = models.TextField(default='')
    status = models.BooleanField(default=1)
    state = models.SmallIntegerField(
        choices=(
            (0, 'En Espera'), (1, 'Completado'), (2, 'Rechazado')
         ), default=0
    )

    @property
    def is_active(self):
        return bool(self.status)

    class Meta:
        verbose_name_plural = "Recognition Element"

    def __str__(self):
        return str(self.label) + " - Active: " + str(self.is_active)
