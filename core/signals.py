from django.dispatch import receiver
from django.db.models.signals import post_save
from account.models import User
from core.models import Tutor, Pet, Tag


@receiver(post_save, sender=User)
def create_tutor(sender, instance, created, **kwargs):
    if created:
        Tutor.objects.create(user=instance, name=instance.name)


@receiver(post_save, sender=Tag)
def update_allotment(sender, instance, created, **kwargs):
    if created:
        print("PET ALLOTMENT UPDATED")
        # tag = instance
        allotment = instance.allotment
        if allotment.quantity > 0 and allotment.active:
            allotment.quantity -= 1
            if allotment.quantity == 0:
                allotment.active = False
            allotment.save()


@receiver(post_save, sender=Pet)
def update_tag(sender, instance, created, *args, **kwargs):
    if created:
        print("PET TAG UPDATED")
        tag = instance.tag
        tag.registered = True
        tag.save()
