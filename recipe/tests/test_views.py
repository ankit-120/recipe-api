from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory, RecipeLike
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


User = get_user_model()

class RecipeListAPIViewTest(APITestCase):

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

    def test_get_recipe_list(self):
        url = reverse('recipe:recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Create a simple image for testing
def create_test_image():
    # Create an image in memory
    image = Image.new('RGB', (100, 100), color = (73, 109, 137))
    image_file = io.BytesIO()
    image.save(image_file, format='JPEG')
    image_file.seek(0)  # Go to the beginning of the file

    return SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")

class RecipeCreateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.login(email='test@example.com', password='testpassword')
        
        # Create a recipe category
        self.category = RecipeCategory.objects.create(name='Test Category')
        
        # Prepare URL and data
        self.url = reverse('recipe:recipe-create')  # Ensure this is the correct URL name
        self.data = {
            'title': 'Test Recipe',
            'desc': 'Test description',
            'cook_time': '01:30:00',  # TimeField needs time in HH:MM:SS format
            'ingredients': 'Test ingredients',
            'procedure': 'Test procedure',
            'category': self.category.id,
            'picture': create_test_image()
            # 'picture': SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')
        }

    def test_create_recipe(self):
        # Ensure the client is authenticated
        self.client.force_authenticate(user=self.user)

        # Define the payload for creating a recipe
        response = self.client.post(self.url, self.data, format='multipart')

        # Print response for debugging
        print('create recipe response',response.data)

        # Check for a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Additional assertions can be added here
        # For example, verify that the recipe was created in the database
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Test Recipe')

class RecipeLikeAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)
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

    def test_like_recipe(self):
        url = reverse('recipe:recipe-like', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecipeLike.objects.count(), 1)

    def test_unlike_recipe(self):
        like = RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe:recipe-like', kwargs={'pk': self.recipe.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecipeLike.objects.count(), 0)
