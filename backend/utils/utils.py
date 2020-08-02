from django.utils import timezone


root_auth = {
    'username': 'root',
    'password': 'lkasdjlkasdflaksdjf',
    'email': 'root@abc.com',
}

date_now = timezone.now()
date_timedelta_1_hour = date_now + timezone.timedelta(hours=1)
date_timedelta_1_5_hours = date_now + timezone.timedelta(hours=1.5)
date_timedelta_2_hours = date_now + timezone.timedelta(hours=2)
date_timedelta_24_hours = date_now + timezone.timedelta(hours=24)

check_data = [
    (date_timedelta_2_hours, False, False),
    (date_timedelta_2_hours, True, False),
    (date_timedelta_2_hours, False, True),
    (date_timedelta_2_hours, True, True),

    (date_now, False, False),
    (date_now, True, False),
    (date_now, False, True),
    (date_now, True, True),
]


def join_test_data(check_data, correct_value):
    for i in range(len(check_data)):
        yield (*check_data[i], *correct_value[i])


def list_events(date):
    def _list_events():
        return [(1, 'Test', '', date, 'ivan@abc.com')]
    return _list_events()


def format_as_iso8601(time):
    """Helper function to format datetime with the Z at the end"""
    # Can't use datetime.isoformat() because format is slightly different from this
    iso_format = '%Y-%m-%dT%H:%M:%S'
    formatted_time = time.strftime(iso_format)
    if time.microsecond:
        miniseconds_format = '.%f'
        formatted_time += time.strftime(miniseconds_format)[:4]
    return formatted_time + "Z"