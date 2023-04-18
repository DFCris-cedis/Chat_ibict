from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from paginas.models import MyUser

@receiver(post_save, sender=User)
def create_myuser(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)