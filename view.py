#imports
import streamlit as st
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit.components.v1 import html
from streamlit_autorefresh import st_autorefresh

from weather import get_weather, get_deltas
from gCalendar import get_calendar_progress
from lava_Bar import lava_progress


# page setup
st.set_page_config(layout="wide")

#bye byedefoult header
st.markdown("""
<style>
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

ICS_URL = "https://calendar.google.com/calendar/ical/c_188aajppcq1b4i4lgds6ba7qukqm4%40resource.calendar.google.com/private-c27724efc70b4459ac548b36a743653a/basic.ics"

# auto refresh 
st_autorefresh(interval=60000, key="auto_refresh")


# force columns to stay side-by-side
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    align-items: flex-start !important;
}

[data-testid="column"] {
    min-width: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# state sameness
if "hovered_event" not in st.session_state:
    st.session_state.hovered_event = None

if "selected_event" not in st.session_state:
    st.session_state.selected_event = None


# weather data
temperature, wind_speed, humidity = get_weather()

if temperature is None:
    temperature, wind_speed, humidity = 0, 0, 0

temp_delta, wind_delta, humidity_delta = get_deltas(
    temperature, wind_speed, humidity
)


# calendar data
events, progress_list, active_count = get_calendar_progress(ICS_URL)


# top bar
col1, col2, col3, col4, col5 = st.columns(5)

now = datetime.now(ZoneInfo("America/Los_Angeles"))
today_string = now.strftime("%Y-%m-%d")
current_time_string = now.strftime("%H:%M:%S")

col1.metric("Time", now.strftime("%I:%M %p"))

with col2:
    st.metric("Date", now.strftime("%m/%d/%Y"))
    st.caption(now.strftime("%A, %B %d, %Y"))

col3.metric("Temperature", f"{temperature:.1f} °F", f"{temp_delta:+.1f} °F")
col4.metric("Wind", f"{wind_speed:.1f} mph", f"{wind_delta:+.1f} mph")
col5.metric("Humidity", f"{humidity}%", f"{humidity_delta:+}%")


st.markdown("---")


# layout
left, right = st.columns([1.35, 1.65], gap="medium")


# calendar view
with left:

    calendar_events = json.dumps(events)

    calendar_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.19/index.global.min.js"></script>

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: white;
                font-family: Arial;
                overflow: hidden;
            }}

            #calendar {{
                width: 100%;
                height: 700px;
            }}

            .fc {{
                background: white;
                border-radius: 12px;
                padding: 10px;
                height: 700px;
            }}

            .fc-toolbar {{
                display: none;
            }}

            .fc-event {{
                pointer-events: none;
            }}
        </style>
    </head>

    <body>
        <div id="calendar"></div>

        <script>
            var calendarEl = document.getElementById('calendar');

            var calendar = new FullCalendar.Calendar(calendarEl, {{
                initialView: 'timeGridTwoDay',
                timeZone: "America/Los_Angeles",

                headerToolbar: false,

                views: {{
                    timeGridTwoDay: {{
                        type: 'timeGrid',
                        duration: {{ days: 2 }}
                    }}
                }},

                initialDate: "{today_string}",

                height: 700,
                expandRows: true,
                nowIndicator: true,
                allDaySlot: false,

                editable: false,
                selectable: false,
                navLinks: false,

                slotMinTime: "06:00:00",
                slotMaxTime: "22:00:00",
                scrollTime: "{current_time_string}",

                events: {calendar_events}
            }});

            calendar.render();
        </script>
    </body>
    </html>
    """

    html(calendar_html, height=700)


# lava display
with right:
    lava_progress(
        progress_list,
        active_count
    )
