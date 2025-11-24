from rest_framework import serializers
from .models import UserProfile, City, Property, PropertyImages, Booking, Review, FavoriteItem, Favorite
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'username', 'email', 'password',
                  'phone_number', 'role', 'avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'email': instance.email,
                'phone_number': instance.phone_number
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'role')


class UserProfileNamesSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'avatar')


class UserProfileDetailSerializer (serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    last_login = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name',
                  'is_superuser', 'email', 'last_login', 'is_staff',
                  'is_active', 'date_joined', 'role', 'phone_number',
                  'avatar', 'groups', 'user_permissions')


class CitySerializer (serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('city_name', 'city_image')


class PropertyImagesSerializer (serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ('image', 'created_date')


class PropertyListSerializer (serializers.ModelSerializer):
    property_images = PropertyImagesSerializer(many=True, read_only=True)
    sum_price_night = serializers.ModelSerializer()
    avg_number_review = serializers.ModelSerializer()

    class Meta:
        model = Property
        fields = ('id', 'property_images', 'title', 'sum_price_night', 'avg_number_review')

    def sum_price_night (self, obj):
        return self.sum_price_night.obj()

    def avg_number_review (self, obj):
        return self.avg_number_review.obj()


class PropertyReviewSerializer (serializers.ModelSerializer):
    property_images = PropertyImagesSerializer(many=True, read_only=True)
    sum_price_night = serializers.ModelSerializer()
    avg_number_review = serializers.ModelSerializer()

    class Meta:
        model = Property
        fields = ('property_images', 'title', 'sum_price_night', 'avg_number_review')

    def sum_price_night (self, obj):
        return self.sum_price_night.obj()

    def avg_number_review (self, obj):
        return self.avg_number_review.obj()



class ReviewPropertySerializer (serializers.ModelSerializer):
    guest = UserProfileNamesSerializer()

    class Meta:
        model = Review
        fields = ('guest', 'rating',
                  'comment', 'created_at')


class PropertyDetailSerializer (serializers.ModelSerializer):
    property_images = PropertyImagesSerializer(many=True, read_only=True)
    avg_number_review = serializers.ModelSerializer()
    city = CitySerializer()
    owner = UserProfileNamesSerializer()
    property_review = ReviewPropertySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'title', 'description', 'property_images', 'city', 'price_per_night',
                  'address', 'property_type', 'rules', 'max_guests', 'is_active',
                  'avg_number_review', 'owner', 'property_review')


    def avg_number_review (self, obj):
        return self.avg_number_review.obj()



class BookingSerializer (serializers.ModelSerializer):
    property = PropertyReviewSerializer()
    guest = UserProfileNamesSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = Booking
        fields = ('id', 'property', 'guest', 'check_in',
                  'check_out', 'status', 'created_at')


class ReviewListSerializer (serializers.ModelSerializer):
    property = PropertyReviewSerializer()

    class Meta:
        model = Review
        fields = ('property', 'rating',
                  'comment')


class ReviewDetailSerializer (serializers.ModelSerializer):
    property = PropertyReviewSerializer()
    guest = UserProfileNamesSerializer()

    class Meta:
        model = Review
        fields = ('id', 'property', 'guest', 'rating',
                  'comment', 'created_at')


class ReviewCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class FavoriteSerializer (serializers.ModelSerializer):
    guest = UserProfileNamesSerializer()

    class Meta:
        model = Favorite
        fields = ('id', 'guest')


class FavoriteItemSerializer (serializers.ModelSerializer):
    favorite = FavoriteSerializer()
    property = PropertyListSerializer()

    class Meta:
        model = FavoriteItem
        fields = ('id', 'favorite', 'property')