import logging
from django.core.mail import send_mail
from celery import shared_task
import smtplib
from decouple import config
from recipe.models import Recipe

# Configure logger
logger = logging.getLogger(__name__)

@shared_task
def example_task(arg1, arg2):
    result = arg1 + arg2  
    print(result)
    return result


# @shared_task
# def send_daily_likes_notification(author_email, likes_count):
#     logger.info('send_daily_likes_notification task started')
#     logger.info(f'Preparing to send email to {author_email} with {likes_count} likes')

#     try:
#         subject = 'Daily Notification: Likes Received on Your Recipes'
#         message = f'Hello,\n\nYou have received {likes_count} new likes on your recipes today!\n\nBest regards,\nRecipe App Team'
        
#         # Send the email
#         # send_mail(subject, message, 'roy.coc733@gmail.com', [author_email])
#         server = smtplib.SMTP('smtp.gmail.com',587)
#         server.starttls()
#         server.login(config('EMAIL_USER'),config('EMAIL_PASSWORD'))
#         text = f"Subject: {subject}\n\n{message}"
#         server.sendmail(config('EMAIL_USER'),author_email,text)
        
#         logger.info(f'Email successfully sent to {author_email}')
#     except Exception as e:
#         logger.error(f'Error sending email to {author_email}: {str(e)}')
#         raise e  # Optional: re-raise if you want the task to fail

@shared_task
def send_daily_likes_notification():
    author_email='roy.ankit5008@gmail.com'
    likes_count=10
    logger.info('send_daily_likes_notification task started')
    logger.info(f'Preparing to send email to {author_email} with {likes_count} likes')

    try:
        subject = 'Daily Notification: Likes Received on Your Recipes'
        message = f'Hello,\n\nYou have received {likes_count} new likes on your recipes today!\n\nBest regards,\nRecipe App Team'
        
        # Send the email
        # send_mail(subject, message, 'roy.coc733@gmail.com', [author_email])
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(config('EMAIL_USER'),config('EMAIL_PASSWORD'))
        text = f"Subject: {subject}\n\n{message}"
        server.sendmail(config('EMAIL_USER'),author_email,text)
        
        logger.info(f'Email successfully sent to {author_email}')
    except Exception as e:
        logger.error(f'Error sending email to {author_email}: {str(e)}')
        raise e  # Optional: re-raise if you want the task to fail
    
@shared_task
def notify_authors_of_likes():
    """
    Notify all authors of the number of likes their recipes received today.
    """
    recipes = Recipe.objects.all()
    for recipe in recipes:
        likes_count = recipe.get_total_number_of_likes()
        author_email = recipe.author.email
        send_daily_likes_notification.delay(author_email, likes_count)