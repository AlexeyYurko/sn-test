from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(
        upload_to='users', verbose_name='Photo', default='', blank=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user_id)])


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=140, verbose_name='Title', default='Title text')
    text = models.TextField(verbose_name='Post text')
    image = models.ImageField(
        upload_to='images', verbose_name='Image', default='', blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Date and time of post')
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date and time of post modify')
    likes = models.IntegerField(default=0, verbose_name='Like/Dislike')
    slug = models.SlugField(editable=False, verbose_name='Slug')

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['created_at', 'by_user']

    def __str__(self):
        return f'{self.by_user.username} - {self.title} @ {self.created_at}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save()


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    number = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{origin_slug}-{number}'
        number += 1
    return unique_slug
