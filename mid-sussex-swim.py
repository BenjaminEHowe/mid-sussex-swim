import config
import domain

import datetime
import flask
import logging
import os
import requests
import shutil
import time

from simplejson.errors import JSONDecodeError


logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=config.LOG_FILE,
    format='%(asctime)s (%(levelname)s): %(message)s',
    level=config.LOG_LEVEL)


def copy_static_files():
    if not os.path.exists(os.path.join(config.OUTPUT_DIR, config.STATIC_DIR)):
        os.makedirs(os.path.join(config.OUTPUT_DIR, config.STATIC_DIR))
    static_files = os.listdir(config.STATIC_DIR)
    for file_name in static_files:
        full_file_name = os.path.join(config.STATIC_DIR, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, os.path.join(config.OUTPUT_DIR, config.STATIC_DIR, file_name))


def generate_daily_pages(dates):
    for date in dates:
        rendered = flask.render_template(
            'daily-events.html',
            date=date,
            events=get_events_on_date(date),
            leisureCentres=config.LEISURE_CENTRES,
            now=datetime.datetime.now()
        )
        with open(os.path.join(config.OUTPUT_DIR, f'{format_datetime(date, "dateiso")}.html'), 'w') as f:
            f.write(rendered)


def generate_index_page():
    rendered = flask.render_template('index.html', dates=dates, now=datetime.datetime.now())
    with open(os.path.join(config.OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(rendered)


def get_events_on_date(date):
    events = []
    for centre in config.LEISURE_CENTRES:
        url = f'https://pfpleisure-pochub.org/LhWeb/en/api/Sites/{centre.siteId}/Timetables/{config.SWIM_TIMETABLE_ID}/Events'
        for location in centre.locations:
            params = {'locationGroupId': location.guid, 'date': date.strftime('%Y/%m/%d')}
            time.sleep(config.REQUEST_DELAY_SECONDS)
            for event in request_json_with_backoff(url, params):
                events.append(
                    domain.Event(
                        event['DisplayName'],
                        datetime.datetime.fromisoformat(event['StartTime']),
                        datetime.datetime.fromisoformat(event['EndTime']),
                        centre.siteId,
                        location.guid,
                        event['TotalPlaces'],
                        event['AvailablePlaces']
                    )
                )
    events.sort(key=lambda event: event.startTime)
    return events


def request_json_with_backoff(url, params):
    for i in range(config.REQUEST_RETRIES):
        if i != 0:
            sleepDuration = config.REQUEST_BACKOFF_BASE ** i
            logging.info(f'Previous HTTP request failed, sleeping for {sleepDuration} seconds.')
            time.sleep(sleepDuration)
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning(f'HTTP request to {url} failed with status code {response.status_code} (body: "{response.text}").')
        except JSONDecodeError:
            pass
    logging.critical(f'Unable to obtain JSON from {url} after {config.REQUEST_RETRIES} attempts.')
    raise RuntimeError


app = flask.Flask('Mid Sussex Swim')


@app.template_filter('datetime')
def format_datetime(value, format='datetime'):
    if format == 'datehuman':
        format_code = '%d %B %Y'
    elif format == 'dateiso':
        format_code = '%Y-%m-%d'
    elif format == 'datetime':
        format_code = '%Y-%m-%d %H:%M:%S'
    elif format == 'timeshort':
        format_code = '%H:%M'
    return value.strftime(format_code)


@app.template_filter('get_centre_display_name')
def get_centre_display_name(event):
    return next(centre.displayName for centre in config.LEISURE_CENTRES if centre.siteId == event.siteId)


@app.template_filter('get_event_booked_places')
def get_event_booked_places(event):
    return event.totalPlaces - event.availablePlaces


@app.template_filter('get_event_percent_full')
def get_event_percent_full(event):
    return (get_event_booked_places(event) / event.totalPlaces) * 100


@app.template_filter('get_event_progress_colour')
def get_event_progress_colour(event):
    percent_full = get_event_percent_full(event)
    if percent_full < 50:
        return '#198754'
    elif percent_full < 75:
        return '#ffc107'
    elif percent_full < 100:
        return '#fd7e14'
    else:
        return '#dc3545'


@app.template_filter('get_location_display_name')
def get_location_display_name(event):
    locations = next(centre for centre in config.LEISURE_CENTRES if centre.siteId == event.siteId).locations
    return next(location.displayName for location in locations if location.guid == event.locationGuid)


if __name__ == "__main__":
    dates = []
    now = datetime.datetime.now()
    logging.info('Updating...')
    for i in range(config.DAYS_ADVANCE + 1):
        dates.append(now + datetime.timedelta(days=i))
    copy_static_files()
    with app.app_context():
        generate_daily_pages(dates)
        generate_index_page()
    logging.info('Update complete!')
