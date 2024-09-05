from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory, RecipeLike
from recipe.serializers import RecipeSerializer, RecipeCategorySerializer, RecipeLikeSerializer

User = get_user_model()

class RecipeCategorySerializerTest(TestCase):

    def setUp(self):
        self.category = RecipeCategory.objects.create(name="Dessert")
        self.serializer = RecipeCategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.category.name)


class RecipeSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.category = RecipeCategory.objects.create(name="Dessert")
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            title="Chocolate Cake",
            desc="Delicious chocolate cake recipe",
            cook_time="00:30:00",
            ingredients="Chocolate, Flour, Sugar, Eggs",
            procedure="Mix ingredients and bake"
        )
        self.serializer = RecipeSerializer(instance=self.recipe)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), [
            'id', 'category', 'category_name', 'picture', 'title', 'desc', 
            'cook_time', 'ingredients', 'procedure', 'author', 'username', 
            'total_number_of_likes', 'total_number_of_bookmarks'
        ])

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)


class RecipeLikeSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.category = RecipeCategory.objects.create(name="Dessert")
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            title="Chocolate Cake",
            desc="Delicious chocolate cake recipe",
            cook_time="00:30:00",
            ingredients="Chocolate, Flour, Sugar, Eggs",
            procedure="Mix ingredients and bake"
        )
        self.recipe_like = RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        self.serializer = RecipeLikeSerializer(instance=self.recipe_like)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'user', 'recipe'])
