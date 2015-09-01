import schedule  # https://github.com/dbader/schedule
import googlemaps  # https://github.com/googlemaps/google-maps-services-python

from datetime import datetime
import csv
from tools import catch_exceptions


INTERVAL_IN_SECS = 5
CSV_FILE = '/Users/manoj/workspace/gmaps_fun/results.csv'


def dump_results(req_time, result):
    formatted_time = req_time.strftime("%Y%m%d %H:%M")

    # if we do alternatives=true, we need to figure out a way to differentiate various routes
    # route_0 = result["routes"][0]

    assert len(result["legs"]) == 1, "Why are there more legs?"

    duration_in_mins = result["legs"][0]["duration"]["value"] / 60
    summary = result["summary"]
    with open(CSV_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([formatted_time, summary, duration_in_mins])


@catch_exceptions
def maps_request():
    gmaps_client = googlemaps.Client(key='AIzaSyA6cCE6kBvS8CmM1-fPm4hPZbArcijMSJE')

    now = datetime.now()
    directions_result = gmaps_client.directions("1334 Prevost Street, San Jose",
                                                "899 W Evelyn Ave, Mountain View, CA 94041",
                                                departure_time=now)
    print directions_result
    dump_results(now, directions_result[0])


schedule.every(INTERVAL_IN_SECS).seconds.do(maps_request)

while True:
    schedule.run_pending()


