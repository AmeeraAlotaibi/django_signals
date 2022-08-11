from django.db.models.signals  import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CafeOwner, CoffeeShop, CoffeeShopAddress, Drink
from utils import create_slug

@receiver(post_save, sender=CafeOwner)
def send_new_owner_email(sender, instance, created, **kwargs):
    if created == True:
        send_mail(
            subject="New Cafe Owner", 
            message= f"A new cafe owner has joined named {instance.first_name} {instance.last_name}",
            from_email=f"{sender.first_name}@test.com",
            recipient_list=["reciever@test.com"],
        ),


### reason why we use pre_save for creating slugs ##
# you have to create slugs after the instance gets created 
# because the create_slug function cannot sluggify empty strings.
@receiver(pre_save, sender=CoffeeShop)
def slugify_coffee_shop(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# create default address
@receiver(post_save, sender= CoffeeShop)
def add_default_address(sender, instance, created, **kwargs):
    if created and instance.location is None:
        location= CoffeeShopAddress.objects.create()
        instance.location = location
        instance.save()


# restore default address
@receiver(post_delete, sender=CoffeeShopAddress)
def restore_default_address(sender, instance, **kwargs):
    coffee_shop = instance.coffee_shop
    default= CoffeeShopAddress.objects.create()
    coffee_shop.location = default
    coffee_shop.save()


# drink
@receiver(pre_save, sender=Drink)
def slugify_coffee_shop(sender, instance, **kwargs):
    if instance.stock_count > 0:
        instance.is_out_of_stock = False
    elif instance.stock_count < 0:
        instance.is_out_of_stock = True
