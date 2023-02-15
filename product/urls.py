from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
# .../posts/  -> GET(list), POST(create)
# .../posts/<id>/  -> GET(retrieve), PUT/PATCH(update),
#                                               DELETE(destroy)

urlpatterns = [
    path('', include(router.urls))
    # path('likes/', views.LikeCreateView.as_view()),
    # path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
    # path('api/v1/favorites/', views.FavoritesCreateView.as_view()),
]
