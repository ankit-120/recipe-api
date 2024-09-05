from django.core.management.base import BaseCommand
from django.utils.timezone import now
from recipe.tasks import send_daily_likes_notification
from recipe.models import Author

class Command(BaseCommand):
    help = 'Send daily email notifications to authors about likes on their recipes.'

    def handle(self, *args, **kwargs):
        # Fetch authors and their likes count (assuming you have a method for this)
        authors = Author.objects.all()
        for author in authors:
            likes_count = author.get_likes_count_for_today()  # Implement this method in Author model
            send_daily_likes_notification.delay(author.email, likes_count)
        self.stdout.write(self.style.SUCCESS('Successfully sent daily notifications.'))
