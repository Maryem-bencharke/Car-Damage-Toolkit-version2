from django.db import models

class Car(models.Model):
    image = models.ImageField(blank = True, null = True)
    iscar = models.BooleanField(default=True)
    isdamaged = models.BooleanField(default=True)
    location = models.CharField(max_length=16,default="Front")
    severity = models.CharField(max_length=16,default="Severe")


    def __str__(self):
        return self.image.name

    def get_image(self):
        if self.image :
            return 'http://127.0.0.1:8000' + self.image.url 
        else:
            return ''

    def get_absolute_url(self):
        return f'/{self.id}/'

