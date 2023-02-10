from rest_framework import serializers
from .models import Review


class ReviewActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')


    class Meta:
        model = Review
        fields = '__all__'


    def validate(self, attrs):
        request = self.context['request']
        product = attrs['product']
        user = request.user
        if user.reviews.filter(product=product).exists():
            raise serializers.ValidationError('You already reviewed this product')
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'
