from __future__ import division
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict

with open('turnstile_150704.txt') as f:
    reader = csv.reader(f)
    rows = [[cell.strip() for cell in row] for row in reader]

assert rows.pop(0) == ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME',
                       'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES',
                       'EXITS']
#Challenge 1
raw_readings = {}
for row in rows:
    raw_readings.setdefault(tuple(row[:4]), []).append(tuple(row[4:]))

#Challenge 2
datetime_cumulative = {turnstile: [(datetime.strptime(date + time,
                                                      '%m/%d/%Y%X'),
                                    int(out_cumulative))
                                   for _, _, date, time,
                                       _, _, out_cumulative in rows]
                       for turnstile, rows in raw_readings.items()}

for rows in datetime_cumulative.values():
    assert rows == sorted(rows)

datetime_count_times = {turnstile: [[rows[i][0],
                                     rows[i+1][1] - rows[i][1],
                                     rows[i+1][0] - rows[i][0]]
                                    for i in range(len(rows) - 1)]
                        for turnstile, rows in datetime_cumulative.items()}



all_counts = [count for rows in datetime_count_times.values() for _, count, _ in rows]
all_counts.sort()

all_times = [duration.total_seconds() / 60 / 60
             for rows in datetime_count_times.values()
             for _, _, duration in rows]
#print Counter(all_times).most_common(10)

datetime_counts = {turnstile: [(time, count)
                               for (time, count, _) in rows
                               if 0 <= count <= 5000]
                   for turnstile, rows in datetime_count_times.items()}
#print datetime_counts.items()[0]
all_good_counts = [count for rows in datetime_counts.values() for _, count in rows]
#print len(all_good_counts) / len(all_counts)

all_good_counts.sort()
#print all_good_counts[-5:]

#print all_good_counts[:5]

#Challenge 3
day_counts = {}
for turnstile, rows in datetime_counts.items():
    by_day = {}
    for time, count in rows:
        day = time.date()
        by_day[day] = by_day.get(day, 0) + count
    day_counts[turnstile] = sorted(by_day.items())
#print day_counts.items()[0]

#Challenge 4
for turnstile, values in day_counts.items():
    dates = [date for date, count in values]
    counts = [count for date, count in values]
plt.figure(figsize = (10,3))
plt.plot(dates, counts)

#Challenge 5
#(By CA/Unit/Station)
group_all_counts = {}
keymap = {turnstile: tuple((turnstile[0], turnstile[1], turnstile[3])) for turnstile, rows in day_counts.items()}
for turnstile, rows in day_counts.items():
    group_all_counts.setdefault(tuple(keymap[turnstile]), []).append(tuple(rows))
#print station_day_counts.items()[0]

group_day_counts = {}
for station, data in group_all_counts.items():
    new_dict = {}
    for week in data:
            for day, count in week:
                new_dict[day] = new_dict.get(day, 0) + count
            group_day_counts[station] = sorted(new_dict.items())
#print group_day_counts.items()[0]

#(by just the station name)

station_all_counts = {}
station_keymap = {turnstile: turnstile[2] for turnstile, rows in group_day_counts.items()}
for turnstile, rows in group_day_counts.items():
    station_all_counts.setdefault(station_keymap[turnstile], []).append(tuple(rows))

station_day_counts = {}
for station, data in station_all_counts.items():
    station_new_dict = {}
    for week in data:
            for day, count in week:
                station_new_dict[day] = station_new_dict.get(day, 0) + count
            station_day_counts[station] = sorted(station_new_dict.items())
print station_day_counts.items()[0]

#Challenge 6
for station, total_counts in station_day_counts.items():
    station_dates = [date for date, count in total_counts]
    station_counts = [count for date, count in total_counts]

#Challenge 7
plt.figure(figsize = (10,3))
plt.title(station)
plt.plot(station_dates, station_counts)

#Challenge 9
total_ridership_counts = {}
for station, date_counts in station_day_counts.items():
    for day, count in date_counts:
        total_ridership_counts[station] = total_ridership_counts.get(station, 0) + count

top_stations = OrderedDict(sorted(total_ridership_counts.items(), key=lambda tup: tup[-1], reverse = True)[0:10])
print top_stations

plt.bar(range(len(top_stations)), top_stations.values(), align='center')
plt.title("Top 10 stations by traffic for w/e 7/4")
plt.xticks(range(len(top_stations)), top_stations.keys(), rotation=60)
plt.show()

time_top_stations = OrderedDict(sorted(station_day_counts.items(), key=lambda tup: tup[-1], reverse = True)[0:10])
print time_top_stations

total_day_counts = {}
for station, day_counts in time_top_stations.items():
    for day, count in day_counts:
        total_day_counts[day] = total_day_counts.get(day, 0) + count
total_counts = OrderedDict(sorted(total_day_counts.items(), key=lambda tup: tup[0]))

print total_counts

plt.figure(figsize = (10,3))
plt.title("All station traffic for w/e 7/4")
plt.plot(total_counts.keys(), total_counts.values())
plt.show()

time_station_all_counts = {}
time_station_keymap = {turnstile: turnstile[3] for turnstile, rows in datetime_counts.items()}
for turnstile, rows in datetime_counts.items():
    time_station_all_counts.setdefault(time_station_keymap[turnstile], []).append(tuple(rows))

time_station_day_counts = {}
for station, data in time_station_all_counts.items():
    station_new_dict = {}
    for week in data:
            for day, count in week:
                station_new_dict[day] = station_new_dict.get(day, 0) + count
            time_station_day_counts[station] = sorted(station_new_dict.items())
penn_time =  time_station_day_counts["34 ST-PENN STA"]
print penn_time

sorted_penn_time = sorted(penn_time, key=lambda tup: tup[1], reverse = True)
print "Sorted penn:", sorted_penn_time

"""
penn_time_dict = {}
for i in penn_time:
    penn_time_dict.setdefault((i)[0],[]).append(i[1])
sorted_penn_times = OrderedDict(sorted(penn_time_dict()))


plt.figure(figsize = (10,3))
plt.title("Traffic by hour at 34 ST-PENN STA")
plt.plot([time for time, count in penn_time], [count for time, count in penn_time])
"""
"""
penn_time_rate = []
for i in penn_time:
    for date, count in i:
        rate = count/(date(i+1)-date(i))
    penn_time_rate.append(date, rate)
print penn_time_rate

penn_time_dict = {}
for i in penn_time:
    penn_time_dict.setdefault((i)[0],[]).append(i[1]/((i+1)-(i)))
sorted_penn_times = OrderedDict(sorted(penn_time_dict.items()))

print sorted_penn_times
"""
