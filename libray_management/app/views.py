from django.shortcuts import render
from django.utils import timezone
from app.models import * 
from app.serializer import *
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

# Create your views here.

class Registerview(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filterset_fields = ['author_name', 'genres_name', 'title']
    search_fields = ['title', 'ISBN']
    ordering_fields = ['title']
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BookCreateSerializer    
        return BookSerializer
    
    
    def get_permission(self):
        if self.request.methof in ['POST', 'PUT', "DELETe", 'PATCH']:
            return [IsAuthenticated(), IsLibrarian()]
        return [AllowAny()]
    
    
class AuthorListAndCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        return [IsAuthenticated(), IsLibrarian()] if self.request.method == 'POST' else [AllowAny()]
    
        
class GenericLisrView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsLibrarian()] if self.request.method == 'POST' else [AllowAny()]

class BorrowRequestCreateView(generics.CreateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class UserBorrowRequestLsitView(generics.CreateAPIView):
    serializer_class = BorrowRequestSerializer
    
    def get_queryset(self):
        return BorrowRequest.objects.filter(user=self.request.user)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsLibrarian])
def approve_borrow(request,pk):
    borrow = BorrowRequest.objects.get(pk=pk)
    if borrow.status != 'pending':
        return Response({"details": "ALready process done"})
    
    borrow.status = 'approved'
    borrow.approved_at = timezone.now()
    
    borrow.book.available_copies -= 1
    borrow.book.save()
    borrow.save()
    
    return Response({"status": 'approved'})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsLibrarian])
def reject_borrow(request, pk):
    borrow = BorrowRequest.objects.get(pk=pk)
    borrow.status = 'REJECTED'
    borrow.save()
    return Response({"status": "rejected"})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def return_borrow(request, pk):
    borrow = BorrowRequest.objects.get(pk=pk)
    borrow.status = 'RETURNED'
    borrow.returned_at = timezone.now()
    borrow.book.available_copies += 1
    borrow.book.save()
    borrow.save()
    return Response({"status": "returned"})


class BookReviewCreateView(generics.CreateAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_Create(self,serializer):
        book_id = self.kwargs['pk']
        serializer.save(user=self.request.user, book_id=book_id)
        
        
class BookReviewListView(generics.ListAPIView):
    serializer_class = BookReviewSerializer
    
    
    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs['pk'])
    
    
    
        
        
        