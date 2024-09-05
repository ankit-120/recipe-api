from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import RecipeCategory, Recipe, RecipeLike

User = get_user_model()

#t
class RecipeCategoryModelTest(TestCase):

    def test_string_representation(self):
        category = RecipeCategory(name="Dessert")
        self.assertEqual(str(category), category.name)


class RecipeModelTest(TestCase):

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

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Chocolate Cake")
        self.assertEqual(self.recipe.author.username, "testuser")
        self.assertEqual(str(self.recipe), "Chocolate Cake")

    def test_get_total_number_of_likes(self):
        self.assertEqual(self.recipe.get_total_number_of_likes(), 0)
        
    def test_get_total_number_of_bookmarks(self):
        self.assertEqual(self.recipe.get_total_number_of_bookmarks(), 0)


class RecipeLikeModelTest(TestCase):

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

    def test_recipe_like_creation(self):
        self.assertEqual(str(self.recipe_like), self.user.username)
