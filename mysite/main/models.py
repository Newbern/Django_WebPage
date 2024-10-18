from django.db import models
from django.contrib.auth.models import User


# The Account holding there image
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='AccountImages/', default="AccountImages/Guest")
    cart = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.username

    # Changing Image Name
    def save(self, *args, **kwargs):
        # Setting image as default if no image was selected
        if self.image == "AccountImages/Guest":
            pass

        # Checking to see if the Image is already named
        elif not self.image.name.count(self.user.username):
            self.image.name = self.user.username

        # Saving data
        super().save()

    # Deleting Image
    def delete(self, using=None, keep_parents=False):
        if not self.image == "Guest" or not self.image == "AccountImages/Guest":
            super().delete()
            import os
            os.remove(self.image.path)


# The ImageSlide container
class ImageSlide(models.Model):
    name = models.CharField(max_length=200, null=True)

    # Getting all the Images inside this container
    def get_images(self):
        return self.image_set.all()

    def __str__(self):
        return str(self.name)


# The Image contained in the container
class Image(models.Model):
    file = models.ForeignKey(ImageSlide, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='ImageSlides/')

    # Slightly changing the Image name for better appearance
    def __str__(self):
        return f"{self.file.name}/{str(self.image).split('/')[1].split('.')[0]}"

    # Deleting Image
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete()


# The Items
class Part(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Parts/', default='Parts/_NotFound.png')
    stock = models.IntegerField(default=0)
    summary = models.TextField(blank=True)

    # Changing how price is captured
    def save(self, *args, **kwargs):
        # Checking for Dolor Sign
        if not self.price.startswith("$"):
            self.price.replace("$", "")
            self.price = f"${self.price}"

        # Checking for cents
        if not self.price.count("."):
            self.price = f"{self.price}.00"

        # Changing Image Name
        if not self.image.name == f"Parts/{self.name}" and not self.image.name.count("_"):
            self.image.name = self.name
        super().save()

    # Deleting Image
    def delete(self, using=None, keep_parents=False):
        if not self.image.name == "Parts/_NotFound.png":
            self.image.delete()
        super().delete()

    def __str__(self):
        return str(self.name)
