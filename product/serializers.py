from django.db.models import Avg
from rest_framework import serializers
from category.models import Category
from rating.serializers import ReviewSerializer
from .models import Product, Like, Favorites


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email', 'title', 'price', 'image', 'stock', 'reviews', 'category', 'description')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        # repr['text'] = instance.reviews('text')
        return repr


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_stars(instance):
        stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
                 '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
                 '1': instance.reviews.filter(rating=1).count()}
        return stars


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['rating_count'] = instance.reviews.count()
        repr['stars'] = self.get_stars(instance)
        return repr


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.liked_product.filter(product=product).exists():
            raise serializers.ValidationError('You already liked this product')
        return attrs


class LikedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.product.title
        image = instance.post.image
        repr['product_image'] = image.url
        return repr


class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Favorites
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.favorite_product.filter(product=product).exists():
            raise serializers.ValidationError('You already added to favorites this product')
        return attrs


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.product.title
        image = instance.post.image
        repr['product_image'] = image.url
        return repr
