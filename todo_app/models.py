from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='userDPs', default='default.jpg')
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')), blank=False)
    country = models.CharField(max_length=20, blank=False)
    phone_no = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name_plural = 'Users Profiles'

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 400 and img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
    

class Tasks(models.Model):
    rel = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField(blank=False, help_text='Enter the task you want to do, you can include place/school or campus/city/country.')
    task_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    date_due = models.DateTimeField(help_text='Date-time format: YYYY-MM-DD HH:MM:SS. Time is optional.')

    class Meta:
        ordering = ['date_due']
        verbose_name_plural = 'Scheduled Tasks'

    def __str__(self):
        return f'{self.task}'
