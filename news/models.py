from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=600, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    # IMPORTANT: drafts by default (professional approach)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.slug = f"{base_slug}-{timestamp}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def __str__(self):
        return self.title


class JournalistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='journalists/', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_journalist_profile(sender, instance, created, **kwargs):
    if created:
        JournalistProfile.objects.create(user=instance)
