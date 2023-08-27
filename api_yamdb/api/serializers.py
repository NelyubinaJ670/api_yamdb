from rest_framework import serializers
from reviews.models import Title, Genre, Category, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            'id', 'name', 'category', 'genre',
            'description', 'year',
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254
    )


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )
    score = serializers.IntegerField(
        min_value=1, max_value=10
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )
        read_only = ('id',)

    def validate(self, data):
        request = self.context.get('request')
        title = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=request.user, title=title).exists():
            raise serializers.ValidationError('У вас уже есть отзыв'
                                              'на это произведение')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работ с отзывами"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )
    score = serializers.IntegerField(
        min_value=1, max_value=10
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )
        read_only = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )
        read_only = ('id',)
