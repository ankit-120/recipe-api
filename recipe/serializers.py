from rest_framework import serializers
from .models import Recipe, RecipeCategory, RecipeLike

class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('id', 'name')

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=RecipeCategory.objects.all())
    total_number_of_likes = serializers.SerializerMethodField()
    total_number_of_bookmarks = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'category', 'category_name', 'picture', 'title', 'desc',
                  'cook_time', 'ingredients', 'procedure', 'author', 'username',
                  'total_number_of_likes', 'total_number_of_bookmarks')

    def get_username(self, obj):
        return obj.author.username

    def get_category_name(self, obj):
        return obj.category.name

    def get_total_number_of_likes(self, obj):
        return obj.get_total_number_of_likes()

    def get_total_number_of_bookmarks(self, obj):
        return obj.get_total_number_of_bookmarks()

    def create(self, validated_data):
        category = validated_data.pop('category')
        # Fetch or create the category instance based on primary key
        category_instance = RecipeCategory.objects.get(pk=category.id)
        recipe_instance = Recipe.objects.create(
            **validated_data, category=category_instance)
        return recipe_instance

    def update(self, instance, validated_data):
        # Update the category instance if provided
        if 'category' in validated_data:
            category = validated_data.pop('category')
            category_instance = RecipeCategory.objects.get(pk=category.id)
            instance.category = category_instance

        return super().update(instance, validated_data)

class RecipeLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ('id', 'user', 'recipe')
