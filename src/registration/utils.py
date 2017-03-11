import datetime
import requests
import logging

from confluence.settings import EXPLARA_API_KEY, EXPLARA_ATTENDEE_LIST_URL
from .models import User, UserAttendance

logger = logging.getLogger(__name__)


def call_explara_and_fetch_data(EXPLARA_EVENT_ID, max_ticket_id):
    """Syncs all new conference attendees from Explara with the
    application's database.

    Args:
      - EXPLARA_EVENT_ID: str. Event ID for the Explara event.
      - max_ticket_id: int. ticket_id till which Explara data is already
            synced with the db.

    Returns:
      - Attendees data: dict. Response in JSON format as fetched from Explara.
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Bearer %s" % EXPLARA_API_KEY
    }

    payload = {
        'eventId': EXPLARA_EVENT_ID,
        'fromRecord': int(max_ticket_id),
        'toRecord': int(max_ticket_id) + 50
    }

    response = requests.post(
        EXPLARA_ATTENDEE_LIST_URL,
        data=payload,
        headers=headers
    )

    return response.json()


def process_explara_data_and_populate_db(attendee_order_list):
    """Syncs all new conference attendees from explara with the
    application's database.

    Args:
      - attendee_order_list: list. Attendees list as fetched from Explara's API.

    Returns:
      - None.
    """
    for order in attendee_order_list:
        tickets = order['attendee']
        for ticket in tickets:
            logger.info("Processing Ticket: " + str(ticket))
            user_data = {"ticketing_platform": "E"}
            try:
                user_data['email'] = ticket['email']
                user_data['ticket_id'] = ticket['ticketNo']
                name_list = ticket['name'].title().split()
                user_data['first_name'] = name_list[0].title()
                user_data['last_name'] = ' '.join(name_list[1:])
                # username is intentionally kept as ticket_no so there
                # aren't any chances of DB integrity error of failing UNIQUE
                # constraint on username
                user_data['username'] = 'explara_' + str(user_data['ticket_id'])
                user_data['tshirt_size'] = ticket['details']['T-shirt size']
                user_data['contact'] = ticket['details']['Contact Number']
            except KeyError as e:
                logger.warning("Error in decoding data: " + str(e))
                logger.warning("Ticket information " + str(ticket))
                continue

            create_user_in_db(**user_data)


def create_user_in_db(**kwargs):
    try:
        User.objects.create(**kwargs)
    except Exception as e:
        logger.error("Cannot create User because: " + str(e))


def get_attendance_for_user(user):
    """ Get or create the attendance object for user and return the
    respective message.
    """
    now = datetime.datetime.today()
    attendance, created = UserAttendance.objects.get_or_create(
        user=user, attended_on=now
    )
    if created:
        message = "attendance marked for today"
    else:
        message = "attendance already marked for today."
    return attendance, message
