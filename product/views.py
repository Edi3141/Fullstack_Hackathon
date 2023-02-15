from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics

from rating.serializers import ReviewActionSerializer, ReviewSerializer
# from rating.serializers import ReviewSerializer, ReviewActionSerializer
from .models import Product, Like, Favorites
from . import serializers
from .permissions import IsAuthor


class ProductPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category', 'title', 'price',)

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

    # api/v1/products/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        else:
            if product.reviews.filter(owner=request.user).exists():
                return response.Response('You already reviewed this product', status=400)
            data = request.data
            serializer = ReviewActionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user, product=product)
            return response.Response(serializer.data, status=201)


    @action(['DELETE'], detail=True)
    def review_delete(self, request, pk):
        product = self.get_object()
        user = request.user
        if not product.reviews.filter(owner=user).exists():
            return response.Response('You didn\'t reviewed this product', status=400)
        review = product.reviews.get(owner=user)
        review.delete()
        return response.Response('Successfully deleted', status=204)


    @action(['GET'], detail=True)
    def get_like(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_product.filter(product=product).exists():
                return Response('This product is already liked', status=400)
            Like.objects.create(owner=user, product=product)
            return Response('You liked this product', status=201)
        else:
            if not user.liked_product.filter(product=product).exists():
                return Response('You didn\'t liked this product', status=400)
            user.liked_product.filter(product=product).delete()
            return Response('You like is deleted', status=204)

    @action(['GET'], detail=True)
    def get_favorite(self, request, pk):
        product = self.get_object()
        favorites = product.favorites.all()
        serializer = serializers.FavoriteSerializerSerializer(instance=favorites, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorite_product.filter(product=product).exists():
                return Response('This product is already added to favorites', status=400)
            Favorites.objects.create(owner=user, product=product)
            return Response('You added to favorites this product', status=201)
        else:
            if not user.favorite_product.filter(product=product).exists():
                return Response('You didn\'t added to favorites this product', status=400)
            user.favorite_product.filter(product=product).delete()
            return Response('You favorites is deleted', status=204)


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class FavoritesCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FavoritesDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)
