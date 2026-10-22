"""Daily Lubbock weather post from the free National Weather Service API."""
import re
import random
import datetime
import requests

from config import UA

LAT, LON = 33.5779, -101.8552  # Lubbock, TX
SOURCE = "https://forecast.weather.gov/MapClick.php?lat=33.5779&lon=-101.8552"

# ---- Edit these pools to change the voice. Keep jokes about weather only. ----
WIND_HIGH = [
    "Secure your trash cans, your hat, and your sense of optimism.",
    "The wind is not a suggestion today. It is a lifestyle.",
    "If your patio furniture is not in Oklahoma by noon, consider yourself lucky.",
    "Hold onto anything you plan to see again.",
]
WIND_MID = [
    "Breezy, by Lubbock standards, which means normal people would call it windy.",
    "The wind is back. It never really left, but it is back.",
    "Great day to remember why hair products are a gamble here.",
]
WIND_LOW = [
    "Light wind today. Take a picture, it is rare.",
    "The wind is taking a break. Enjoy it while it lasts.",
    "Barely any wind. Suspicious, honestly.",
]
RAIN_HIGH = [
    "Rain is in the forecast, which around here counts as a local holiday.",
    "Actual rain expected. Drivers will forget how roads work, so leave early.",
    "Rain chances are real today. Dust gets the day off.",
]
RAIN_MID = [
    "A chance of rain. Lubbock has heard that story before.",
    "Some rain chances, so keep the umbrella handy but your expectations low.",
]
HOT = [
    "It is hot out. The sun is simply showing off.",
    "Triple digits. Your car's steering wheel is now a cooking surface.",
]
WARM = ["Hot enough to complain, not hot enough to get a day off for it."]
COLD = [
    "Freezing temperatures. Cover your plants and warm up the car.",
    "Cold enough that the wind has real leverage today.",
]
CHILLY = ["Chilly out there. Layers will do you well, the weather may change by lunch."]
# -----------------------------------------------------------------------------


def _get_json(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()


def _max_wind(text):
    nums = [int(n) for n in re.findall(r"\d+", text or "")]
    return max(nums) if nums else 0


def _pop(p):
    return (p.get("probabilityOfPrecipitation") or {}).get("value") or 0


def _period_line(p):
    label = "High" if p.get("isDaytime") else "Low"
    return (
        f"{p['name']}: {p['shortForecast']}. {label} {p['temperature']}F, "
        f"wind {p['windDirection']} {p['windSpeed']}, rain chance {_pop(p)}%."
    )


def build_post(periods, alerts, today=None):
    """Returns (text, straight). straight=True means no jokes (active alerts)."""
    if alerts:
        lines = ["Weather alert for Lubbock:"]
        for event, headline in alerts:
            lines.append(f"- {event}. {headline}".strip())
        lines.append("Check weather.gov for the latest and stay safe.")
        return "\n".join(lines), True

    today = today or datetime.date.today()
    rng = random.Random(today.toordinal())  # same pick all day, varies by day
    p = periods[0]
    wind, temp, pop = _max_wind(p["windSpeed"]), p["temperature"], _pop(p)

    jokes = [rng.choice(WIND_HIGH if wind >= 30 else WIND_MID if wind >= 20 else WIND_LOW)]
    if pop >= 50:
        jokes.append(rng.choice(RAIN_HIGH))
    elif pop >= 20:
        jokes.append(rng.choice(RAIN_MID))
    elif p.get("isDaytime") and temp >= 100:
        jokes.append(rng.choice(HOT))
    elif p.get("isDaytime") and temp >= 90:
        jokes.append(rng.choice(WARM))
    elif temp <= 32:
        jokes.append(rng.choice(COLD))
    elif temp <= 49:
        jokes.append(rng.choice(CHILLY))

    facts = "\n".join(_period_line(x) for x in periods)
    return " ".join(jokes) + "\n\n" + facts, False


def get_posts():
    point = _get_json(f"https://api.weather.gov/points/{LAT},{LON}")
    periods = _get_json(point["properties"]["forecast"])["properties"]["periods"][:2]
    alerts = _get_json(f"https://api.weather.gov/alerts/active?point={LAT},{LON}")
    alert_list = [
        (a["properties"]["event"], a["properties"].get("headline") or "")
        for a in alerts.get("features", [])
    ]
    text, straight = build_post(periods, alert_list)
    note = "Active alerts present, so this draft has no jokes. Review carefully." if straight else ""
    return [{"title": "Weather", "text": text, "source": SOURCE, "note": note}]
