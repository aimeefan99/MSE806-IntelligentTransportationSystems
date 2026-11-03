import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median


ROOT = Path("Assessment/GTFS_All")
WEEKDAY = "20260923"
WEEKEND = "20260926"


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8-sig") as handle:
        yield from csv.DictReader(handle)


def gtfs_seconds(value):
    hour, minute, second = map(int, value.split(":"))
    return hour * 3600 + minute * 60 + second


def active_services(date_text):
    date = datetime.strptime(date_text, "%Y%m%d")
    weekday = date.strftime("%A").lower()
    active = set()
    for row in rows("calendar.txt"):
        if row["start_date"] <= date_text <= row["end_date"] and row[weekday] == "1":
            active.add(row["service_id"])
    for row in rows("calendar_dates.txt"):
        if row["date"] != date_text:
            continue
        if row["exception_type"] == "1":
            active.add(row["service_id"])
        elif row["exception_type"] == "2":
            active.discard(row["service_id"])
    return active


def haversine(a, b):
    radius = 6371.0088
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(value))


routes = {row["route_id"]: row for row in rows("routes.txt") if row["agency_id"] == "1"}
trips = {row["trip_id"]: row for row in rows("trips.txt") if row["route_id"] in routes}

active_weekday = active_services(WEEKDAY)
active_weekend = active_services(WEEKEND)
weekday_trips = {trip_id for trip_id, row in trips.items() if row["service_id"] in active_weekday}
weekend_trips = {trip_id for trip_id, row in trips.items() if row["service_id"] in active_weekend}

first_time = {}
last_time = {}
stop_counts = Counter()
used_stops = set()
for row in rows("stop_times.txt"):
    trip_id = row["trip_id"]
    if trip_id not in trips:
        continue
    used_stops.add(row["stop_id"])
    stop_counts[trip_id] += 1
    arr = gtfs_seconds(row["arrival_time"])
    dep = gtfs_seconds(row["departure_time"])
    first_time[trip_id] = min(first_time.get(trip_id, dep), dep)
    last_time[trip_id] = max(last_time.get(trip_id, arr), arr)

shape_points = defaultdict(list)
used_shapes = {row["shape_id"] for row in trips.values() if row["shape_id"]}
for row in rows("shapes.txt"):
    shape_id = row["shape_id"]
    if shape_id in used_shapes:
        shape_points[shape_id].append((int(row["shape_pt_sequence"]), float(row["shape_pt_lat"]), float(row["shape_pt_lon"])))

shape_lengths = {}
for shape_id, points in shape_points.items():
    ordered = [(lat, lon) for _, lat, lon in sorted(points)]
    shape_lengths[shape_id] = sum(haversine(a, b) for a, b in zip(ordered, ordered[1:]))


def service_summary(selected):
    hourly = Counter()
    route_trip_counts = Counter()
    route_durations = defaultdict(list)
    route_stops = defaultdict(list)
    route_lengths = defaultdict(list)
    for trip_id in selected:
        trip = trips[trip_id]
        route_id = trip["route_id"]
        route_trip_counts[route_id] += 1
        if trip_id in first_time:
            hourly[first_time[trip_id] // 3600] += 1
        if trip_id in first_time and trip_id in last_time:
            route_durations[route_id].append((last_time[trip_id] - first_time[trip_id]) / 60)
        route_stops[route_id].append(stop_counts[trip_id])
        if trip["shape_id"] in shape_lengths:
            route_lengths[route_id].append(shape_lengths[trip["shape_id"]])
    route_rows = []
    for route_id, count in route_trip_counts.items():
        route = routes[route_id]
        route_rows.append({
            "route": route["route_short_name"] or route["route_long_name"] or route_id,
            "trips": count,
            "median_duration_min": round(median(route_durations[route_id]), 1) if route_durations[route_id] else None,
            "median_stops": round(median(route_stops[route_id]), 1) if route_stops[route_id] else None,
            "max_shape_km": round(max(route_lengths[route_id]), 1) if route_lengths[route_id] else None,
        })
    return {
        "trips": len(selected),
        "routes_operated": len(route_trip_counts),
        "first_departure_hour": min(hourly) if hourly else None,
        "last_departure_hour": max(hourly) if hourly else None,
        "peak_hour": max(hourly, key=hourly.get) if hourly else None,
        "peak_hour_trips": max(hourly.values()) if hourly else None,
        "hourly": {str(hour): hourly[hour] for hour in sorted(hourly)},
        "top_routes_by_trips": sorted(route_rows, key=lambda item: item["trips"], reverse=True)[:5],
        "longest_routes": sorted(route_rows, key=lambda item: item["max_shape_km"] or 0, reverse=True)[:5],
    }


result = {
    "feed": {
        "routes": len(routes),
        "trips": len(trips),
        "used_stops": len(used_stops),
        "shapes": len(used_shapes),
    },
    "weekday_date": WEEKDAY,
    "weekday": service_summary(weekday_trips),
    "weekend_date": WEEKEND,
    "weekend": service_summary(weekend_trips),
}

print(json.dumps(result, indent=2, ensure_ascii=False))
