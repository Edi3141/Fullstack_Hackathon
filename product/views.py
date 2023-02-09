from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action

# from rating.serializers import ReviewSerializer, ReviewActionSerializer
from .models import Product
from . import serializers
from .permissions import IsAuthor


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    #
    # # api/v1/products/<id>/reviews/
    # @action(['GET', 'POST'], detail=True)
    # def reviews(self, request, pk):
    #     product = self.get_object()
    #     if request.method == 'GET':
    #         reviews = product.reviews.all()
    #         serializer = ReviewSerializer(reviews, many=True).data
    #         return response.Response(serializer, status=200)
    #     else:
    #         if product.reviews.filter(owner=request.user).exists():
    #             return response.Response('You already reviewed this product', status=400)
    #         data = request.data
    #         serializer = ReviewActionSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(owner=request.user, product=product)
    #         return response.Response(serializer.data, status=201)
    #
    #
    # @action(['DELETE'], detail=True)
    # def review_delete(self, request, pk):
    #     product = self.get_object()
    #     user = request.user
    #     if not product.reviews.filter(owner=user).exists():
    #         return response.Response('You didn\'t reviewed this product', status=400)
    #     review = product.reviews.get(owner=user)
    #     review.delete()
    #     return response.Response('Successfully deleted', status=204)
