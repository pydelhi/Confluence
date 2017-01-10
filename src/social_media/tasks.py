"""Contains celery tasks to post messages on various social media platforms."""
from __future__ import absolute_import, unicode_literals

# Import secret tokens from settings.
from confluence.settings import FACEBOOK_PAGE_ACCESS_TOKEN
from celery import shared_task

# Import GraphAPI for posting attachment to facebook page.
from facebook import GraphAPI


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
