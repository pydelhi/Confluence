"""Contains celery tasks to migrate conference attendees from different
ticketing platforms."""

from __future__ import absolute_import, unicode_literals

import logging

from django.db.models import Max
from celery import shared_task

from .models import User
from .utils import call_explara_and_fetch_data, process_explara_data_and_populate_db

logger = logging.getLogger(__name__)


@shared_task(name='registration.tasks.sync_database_with_explara')
def sync_database_with_explara(EXPLARA_EVENT_ID):
    """Syncs all new conference attendees from explara with the
    application's database.

    Args:
      - EXPLARA_EVENT_ID: str. Event ID for the explara event.

    Returns:
      - None
    """

    # For having multiple paginated calls to Explara till all the data is
    # synced with the database
    while True:
        max_ticket_id = User.objects.all().aggregate(Max('ticket_id'))["ticket_id__max"]

        if not max_ticket_id:
            max_ticket_id = 0

        data = call_explara_and_fetch_data(EXPLARA_EVENT_ID, max_ticket_id)

        if data["status"] != 'success':
            logger.error("Error from explara: ")
            logger.error(data)
            break

        if not data["attendee"]:
            logger.info("No attendees left now")
            break

        attendee_order_list = data['attendee']

        process_explara_data_and_populate_db(attendee_order_list)
