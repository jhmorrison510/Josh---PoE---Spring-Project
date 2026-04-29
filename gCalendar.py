#imports
import requests
import icalendar
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import streamlit as st


# make all dates  same
def normalize(dt):
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime.combine(dt, datetime.min.time())

    if isinstance(dt, datetime) and dt.tzinfo is not None:
        return dt.astimezone(ZoneInfo("America/Los_Angeles")).replace(tzinfo=None)

    return dt


# main calendar 
@st.cache_data(ttl=60)
def get_calendar_progress(ics_url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; CalendarBot/1.0)"
        }

        r = requests.get(ics_url, headers=headers, timeout=30)

        #too many requests check if google get mad
        if r.status_code == 429:
            print("Rate limited by Google (429)")
            return [], [], 0

        if "BEGIN:VCALENDAR" not in r.text:
            print("Invalid ICS feed (not calendar data)")
            return [], [], 0

        r.raise_for_status()

        cal = icalendar.Calendar.from_ical(r.text)

        now = datetime.now(ZoneInfo("America/Los_Angeles")).replace(tzinfo=None)
        start_window = datetime.combine(now.date(), datetime.min.time())
        end_window = start_window + timedelta(days=2)

        events = []
        progress_list = []
        active_count = 0


        #loop for events
        for c in cal.walk():

            if c.name != "VEVENT":
                continue

            try:
                dtstart = c.get("dtstart")
                dtend = c.get("dtend")

                if not dtstart:
                    continue

                start_raw = dtstart.dt
                end_raw = dtend.dt if dtend else start_raw

                title = str(c.get("summary", "Event"))


               #get rid of all day events
                is_all_day = (
                    hasattr(dtstart, "params")
                    and dtstart.params.get("VALUE") == "DATE"
                )

                if is_all_day:
                    continue


                #make times same
                start = normalize(start_raw)
                end = normalize(end_raw)


                # safety check
                if not isinstance(start, datetime) or not isinstance(end, datetime):
                    continue


                #two day calendar
                if start < end_window and end > start_window:
                    events.append({
                        "title": title,
                        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
                    })


                #lava go
                if start <= now <= end:

                    duration = (end - start).total_seconds()

                    if duration > 0:

                        progress = (now - start).total_seconds() / duration

                        progress_list.append({
                            "title": title,
                            "progress": max(0, min(progress, 1)) * 100
                        })

                        active_count += 1


            except:
                continue


        #sort events
        events.sort(key=lambda x: x["start"])
        progress_list.sort(key=lambda x: x["progress"], reverse=True)


        return events, progress_list, active_count


    except Exception as e:
        print("Calendar Error:", e)
        return [], [], 0
