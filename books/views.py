from .models import Book, Publisher, BookComment, BookLike
from django.db.models import Count
from .serializers import BookSerializer, PublisherSerializer, BookCommentSerializer
from rest_framework import viewsets, response, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import filters
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_deleted=False)

        return qs

    @action(methods=['GET'], detail=False)
    def likes(self, request):
        books = Book.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
        serializer = BookSerializer(instance=books, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.is_deleted = True
        book.save(update_fields=['is_deleted'])
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class BookCommentViewSet(viewsets.ModelViewSet):
    queryset = BookComment.objects.all()
    serializer_class = BookCommentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(book_id=self.kwargs['book_pk'])


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


"""
1) Добавьте возможность фильтрации книг по автору с помощью параметра запроса. Например, /api/books/?author=Иван Тургенев.
2) Добавьте возможность фильтрации издателей по стране с помощью параметра запроса. Например, /api/publishers/?country=США.
3) Сортировка жанров по названию
4) Фильтрация издателей по количеству опубликованных книг
5) Сортировка книг по дате создания
"""