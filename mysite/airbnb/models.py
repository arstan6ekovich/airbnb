from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import DateField
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile (AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Гость'),
        ('host', 'Хозяин'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(choices=ROLE_CHOICES, default='guest')
    phone_number = PhoneNumberField()
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class City (models.Model):
    city_name = models.CharField(max_length=64, unique=True)
    city_image = models.ImageField(upload_to='city_image/')

    def __str__(self):
        return f'{self.city_name}'


class Property (models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price_per_night = models.PositiveIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=44)
    PROPERTY_CHOICES = (
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('studio', 'Студия'),
    )
    property_type = models.CharField(choices=PROPERTY_CHOICES, default='apartment')
    RULES_CHOICES = (
        ('no_smoking', 'Запрещено курить'),
        ('pets_allowed', 'Можно с питомцами'),
    )
    rules = models.CharField(choices=RULES_CHOICES)
    max_guests = models.PositiveIntegerField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f'{self.title} - {self.city} - {self.is_active}'


    def sum_price_night (self):
        return int(self.price_per_night * 2)


    def avg_number_review (self):
        ratings = self.property_review.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return 0





class PropertyImages (models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    image = models.ImageField(upload_to='property_image/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property.title}'



class Booking (models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = DateField()
    check_out = DateField()
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    )
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.guest.username} - {self.property.title}'



class Review (models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_review')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.guest.username} - {self.property.title} - {self.rating}'


class Favorite(models.Model):
    guest = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return f'{self.guest.username}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='items')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('favorite', 'property')

    def __str__(self):
        return f'{self.property.title}'

