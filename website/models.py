from django.db import models


class Quote(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"], name="contact_created_desc_idx"),
        ]


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"], name="feedback_created_desc_idx"),
        ]

    def __str__(self):
        return f"{self.name} - {self.location}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="gallery/")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        indexes = [
            models.Index(
                fields=["is_active", "display_order", "-created_at"],
                name="gallery_active_order_idx",
            ),
        ]

    def __str__(self):
        return self.title
