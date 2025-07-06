from rest_framework import serializers
from app.models import * 
from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User(username=validated_data['username'], role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        
        return user
            
    

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = '__all__'

class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = '__all__'
    
        
class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.user == request.user