from django.urls import path, include
from .views import BookViewSet, PublisherViewSet, BookCommentViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('publishers', PublisherViewSet, basename='publishers')

books_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
books_router.register('comments', BookCommentViewSet, basename='books-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
]

