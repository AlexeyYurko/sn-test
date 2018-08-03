from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify
from markdown import markdown


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # a superuser
    username = models.CharField(max_length=30, blank=True, default='')
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    photo = models.ImageField(
        upload_to='users', verbose_name='Photo', default='', blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their first and last name
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.staff

    @property
    def is_admin(self):
        """
        Is the user a admin member?
        """
        return self.admin


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
    rating = models.IntegerField(default=0, verbose_name='Like/Dislike')
    slug = models.SlugField(editable=False, verbose_name='Slug')
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['created_at', 'by_user']

    def __str__(self):
        return f'{self.by_user.username} - {self.title} @ {self.created_at}'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save()

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    number = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{origin_slug}-{number}'
        number += 1
    return unique_slug
