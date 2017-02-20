"""Contains celery tasks to post messages on various social media platforms."""
from __future__ import absolute_import, unicode_literals

import uuid


# Import secret tokens from settings.
from confluence.settings import FACEBOOK_PAGE_ACCESS_TOKEN

# Import shared tasks
from celery import shared_task

# Import GraphAPI for posting attachment to facebook page.
from facebook import GraphAPI

# Import twitter_api and requests for twitter post
import requests
from .utils import twitter_api_authentication
twitter_api = twitter_api_authentication()


def save_image_from_url(image_url):
    """Extract a image from the image_url

       Args:
           - image_url: Url of the attachment to be posted.
       Returns:
           - filename: Image saved in a file.

    """
    fextn = image_url.rsplit('.')[-1]
    filename = uuid.uuid4().hex + '.' + fextn
    request = requests.get(image_url, stream=True)
    with open(filename, 'wb') as image:
        for chunk in request:
            image.write(chunk)
    return filename


# Create your tasks here

@shared_task(name='social_media.tasks.post_to_facebook')
def post_to_facebook(message, link=None):
    """Posts a message to the Facebook page using GraphAPI authenticated via
       `FACEBOOK_PAGE_ACCESS_TOKEN`.

       Args:
           - message: str. The content of the message to be posted on Facebook.
           - link: str. (Optional) Url of the attachment to be posted along
             with message.

       Returns:
           - None

    """
    graph = GraphAPI(access_token=FACEBOOK_PAGE_ACCESS_TOKEN)
    attachment = {
        'link': link,   # link to visit on clicking on the attachment.
        'picture': link  # link of the attachment to be posted.
    }
    graph.put_wall_post(message=message, attachment=attachment)


@shared_task(name='social_media.tasks.tweet_to_twitter')
def tweet_to_twitter(message, image_url=None):
    """Posts a message to the Twitter page using twitter_api, an instance for
       twitter_api_authentication imported from utility.

       Args:
           - message: str. The content of the message to be posted on Twitter.
           - image_url: (Optional) Url of the attachment to be posted along
              with message.

       Returns:
           - None

    """
    if image_url is not None:
        filename = save_image_from_url(image_url)
        twitter_api.update_with_media(filename, status=message)
    else:
        twitter_api.update_status(message)
