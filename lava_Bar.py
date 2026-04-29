#imports
import streamlit as st
from streamlit.components.v1 import html


def lava_progress(progress_list, active_count):

    if not isinstance(progress_list, list):
        progress_list = []

    tubes_html = ""

    # idle state
    if active_count == 0:
        tubes_html = """
        <div class="tube idle-tube">
            <div class="idle"></div>
            <div class="idle-text">no current events</div>
        </div>
        """

    # single event
    elif active_count == 1:
        item = progress_list[0] if progress_list else {"title": "current event", "progress": 0}

        if isinstance(item, dict):
            title = item.get("title", "current event")
            p = item.get("progress", 0)
        else:
            title = "current event"
            p = item

        tubes_html = f"""
        <div class="tube">
            <div class="lava" style="height: {p}%;"></div>
            <div class="event-label">
                <div class="event-title">{title}</div>
                <div class="event-progress">{round(p)}% complete</div>
            </div>
        </div>
        """

    # overlapping events
    else:
        for item in progress_list[:4]:

            if isinstance(item, dict):
                title = item.get("title", "current event")
                p = item.get("progress", 0)
            else:
                title = "current event"
                p = item

            tubes_html += f"""
            <div class="tube split-tube">
                <div class="lava" style="height: {p}%;"></div>
                <div class="event-label small-label">
                    <div class="event-title">{title}</div>
                    <div class="event-progress">{round(p)}%</div>
                </div>
            </div>
            """

    lava_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
                width: 100%;
                height: 100%;
            }}

            .container {{
                display: flex;
                justify-content: center;
                align-items: stretch;
                width: 100%;
                height: 700px;
                gap: clamp(12px, 2vw, 28px);
                box-sizing: border-box;
                padding: clamp(4px, 1vw, 12px);
            }}

            .tube {{
                flex: 1;
                width: 100%;
                height: 100%;
                max-width: 680px;
                min-width: 0;
                background: rgba(15, 15, 15, 0.86);
                border-radius: clamp(36px, 5vw, 70px);
                overflow: hidden;
                position: relative;
                box-shadow: inset 0 0 45px #000;
                border: 2px solid rgba(255, 140, 0, 0.4);
            }}

            .split-tube {{
                max-width: 260px;
            }}

            .lava {{
                position: absolute;
                bottom: 0;
                width: 100%;
                min-height: 2%;
                background: linear-gradient(
                    180deg,
                    #fff200,
                    #ff8c00,
                    #ff3c00,
                    #5a0000
                );
                background-size: 100% 300%;
                animation: lavaFlow 6s linear infinite, lavaPulse 3s ease-in-out infinite, smoothFill 1.8s ease-out;
                filter: blur(1px);
                box-shadow: 0 0 45px #ff4500;
                border-radius: 45% 45% 0 0;
                transition: height 1.8s ease-in-out;
            }}

            .lava::before {{
                content: "";
                position: absolute;
                top: -38px;
                left: -15%;
                width: 130%;
                height: 76px;
                background: rgba(255, 242, 0, 0.8);
                border-radius: 48%;
                animation: wave 4s ease-in-out infinite;
                filter: blur(8px);
            }}

            .lava::after {{
                content: "";
                position: absolute;
                top: -52px;
                left: -25%;
                width: 150%;
                height: 95px;
                background: rgba(255, 100, 0, 0.45);
                border-radius: 50%;
                animation: wave 6s ease-in-out infinite reverse;
                filter: blur(12px);
            }}

            .event-label {{
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                width: 82%;
                z-index: 10;
                text-align: center;
                color: white;
                font-family: Arial, sans-serif;
                text-shadow: 0 2px 12px rgba(0, 0, 0, 0.9);
                pointer-events: none;
            }}

            .event-title {{
                font-size: clamp(20px, 3vw, 46px);
                font-weight: 700;
                line-height: 1.05;
                margin-bottom: 10px;
            }}

            .event-progress {{
                font-size: clamp(13px, 1.3vw, 20px);
                color: rgba(255, 255, 255, 0.78);
                letter-spacing: 1px;
                text-transform: uppercase;
            }}

            .small-label .event-title {{
                font-size: clamp(13px, 1.5vw, 22px);
            }}

            .small-label .event-progress {{
                font-size: clamp(10px, 1vw, 14px);
            }}

            .idle {{
                position: absolute;
                top: 45%;
                left: 50%;
                width: clamp(120px, 18vw, 210px);
                height: clamp(120px, 18vw, 210px);
                transform: translate(-50%, -50%);
                border-radius: 50%;
                border: 4px solid rgba(255, 140, 0, 0.3);
                border-top: 4px solid #ff3c00;
                animation: spin 2s linear infinite;
                box-shadow: 0 0 35px #ff4500;
            }}

            .idle-text {{
                position: absolute;
                bottom: clamp(24px, 4vw, 48px);
                width: 100%;
                text-align: center;
                font-size: clamp(13px, 1.5vw, 22px);
                color: rgba(255, 255, 255, 0.72);
                font-family: Arial, sans-serif;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}

            @keyframes lavaFlow {{
                0% {{ background-position: 0% 0%; }}
                100% {{ background-position: 0% 100%; }}
            }}

            @keyframes lavaPulse {{
                0% {{ filter: blur(1px) brightness(1); }}
                50% {{ filter: blur(2px) brightness(1.25); }}
                100% {{ filter: blur(1px) brightness(1); }}
            }}

            @keyframes smoothFill {{
                0% {{ transform: translateY(18px); opacity: 0.65; }}
                100% {{ transform: translateY(0); opacity: 1; }}
            }}

            @keyframes wave {{
                0% {{ transform: translateX(0) scaleY(1); }}
                50% {{ transform: translateX(30px) scaleY(1.25); }}
                100% {{ transform: translateX(0) scaleY(1); }}
            }}

            @keyframes spin {{
                0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
                100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}

            @media (max-width: 900px) {{
                .container {{
                    height: 620px;
                    gap: 10px;
                }}

                .tube {{
                    border-radius: 42px;
                }}
            }}
        </style>
    </head>

    <body>
        <div class="container">
            {tubes_html}
        </div>
    </body>
    </html>
    """

    html(lava_html, height=700)