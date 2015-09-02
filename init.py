import schedule  # https://github.com/dbader/schedule
import googlemaps  # https://github.com/googlemaps/google-maps-services-python

from datetime import datetime
import csv
from tools import catch_exceptions

FIVE_MINUTES_IN_SECS = 300
FIFTEEN_MINUTES_IN_SECS = 900
ONE_HOUR_IN_SECS = 3600
ONE_DAY_IN_SECS = 86400

INTERVAL_IN_SECS = FIVE_MINUTES_IN_SECS

# direction flags
TO_WORK = 0
FROM_WORK = 1
CSV_BY_DIRECTION = {TO_WORK: '/Users/manoj/workspace/gmaps_fun/to_work.csv',
                    FROM_WORK: '/Users/manoj/workspace/gmaps_fun/from_work.csv'}

# maps init
gmaps_client = googlemaps.Client(key='AIzaSyA6cCE6kBvS8CmM1-fPm4hPZbArcijMSJE')


def dump_results(req_time, result, direction):
    formatted_time = req_time.strftime("%Y%m%d %H:%M")

    # if we do alternatives=true, we need to figure out a way to differentiate various routes
    # route_0 = result["routes"][0]

    assert len(result["legs"]) == 1, "Why are there more legs?"

    duration_in_mins = result["legs"][0]["duration"]["value"] / 60
    summary = result["summary"]
    with open(CSV_BY_DIRECTION[direction], 'a') as f:
        writer = csv.writer(f)
        writer.writerow([formatted_time, summary, duration_in_mins])


@catch_exceptions
def maps_request():

    now = datetime.now()

    home = "1334 Prevost Street, San Jose"
    work = "899 W Evelyn Ave, Mountain View, CA 94041"

    # only make request if times are interesting
    make_request, direction = False, 0
    if 6 <= now.hour <= 10:
        # morning hours
        src, dest, make_request, direction = home, work, True, 0
    elif 15 <= now.hour <= 19:
        # evening hours
        src, dest, make_request, direction = work, home, True, 1
    else:
        print "Ignoring time {0}".format(now.strftime("%H:%M"))

    if make_request:
        print "Making request at {0}, direction = {1}".format(now.strftime("%H:%M"), direction)
        directions_result = gmaps_client.directions(src, dest, departure_time=now)
        dump_results(now, directions_result[0], direction)


schedule.every(INTERVAL_IN_SECS).seconds.do(maps_request)
while True:
    schedule.run_pending()
