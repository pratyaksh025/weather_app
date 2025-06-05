import streamlit as st
import requests
import time
import random

API_KEY = 'ebb6439dd205bc0046d24c13a1020b39'  # Replace with your OpenWeatherMap API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data['name'],
            "country": data['sys']['country'],
            "temp": data['main']['temp'],
            "desc": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind": data['wind']['speed'],
            "icon": data['weather'][0]['icon']
        }
    else:
        return None

st.title("Weather App")
city = st.text_input("Enter city name:")

# Weather backgrounds for different places and weathers
weather_backgrounds = {
    "clear": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80",  # Norway, clear
        "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80",  # Lake, clear
        "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1500&q=80"   # Desert, clear
    ],
    "clouds": [
        "https://images.unsplash.com/photo-1464037866556-6812c9d1c72e?auto=format&fit=crop&w=1500&q=80",  # Mountains, clouds
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1500&q=80",  # City, clouds
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1500&q=80"   # Field, clouds
    ],
    "rain": [
        "https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=1500&q=80",  # Rainy street
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1500&q=80",  # Rainy window
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1500&q=80"   # Rainy thunder
    ],
    "snow": [
        "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1500&q=80",  # Snowy forest
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1500&q=80",  # Snowy city
        "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1500&q=80"   # Snowy mountain
    ],
    "thunderstorm": [
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1500&q=80",  # Lightning
        "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80",  # Lake, storm
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1500&q=80"   # City, storm
    ],
    "mist": [
        "https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=1500&q=80",  # Misty road
        "https://images.unsplash.com/photo-1464037866556-6812c9d1c72e?auto=format&fit=crop&w=1500&q=80",  # Misty mountains
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1500&q=80"   # Misty field
    ]
}

def get_weather_type(desc):
    desc = desc.lower()
    if "clear" in desc:
        return "clear"
    elif "cloud" in desc:
        return "clouds"
    elif "rain" in desc or "drizzle" in desc:
        return "rain"
    elif "snow" in desc:
        return "snow"
    elif "thunder" in desc:
        return "thunderstorm"
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return "mist"
    else:
        return "clear"

# Initialize session state for background management
if "bg_index" not in st.session_state:
    st.session_state.bg_index = 0
if "last_weather_type" not in st.session_state:
    st.session_state.last_weather_type = random.choice(list(weather_backgrounds.keys()))
if "last_bg_update" not in st.session_state:
    st.session_state.last_bg_update = time.time()
if "bg_url" not in st.session_state:
    st.session_state.bg_url = random.choice(weather_backgrounds[st.session_state.last_weather_type])
if "bg_transition" not in st.session_state:
    st.session_state.bg_transition = "opacity 1s ease-in-out"

# Get weather data if city is entered
weather = None
weather_type = None
if city:
    weather = get_weather(city)
    if weather:
        weather_type = get_weather_type(weather["desc"])
        st.session_state.last_weather_type = weather_type
    else:
        weather_type = st.session_state.last_weather_type
else:
    # When no city is entered, rotate through all weather types randomly
    if time.time() - st.session_state.last_bg_update > 5:  # Change weather type every 5 seconds
        st.session_state.last_weather_type = random.choice(list(weather_backgrounds.keys()))
        st.session_state.last_bg_update = time.time()
    weather_type = st.session_state.last_weather_type

# Update background every 3 seconds (independent of weather type changes)
current_time = time.time()
if current_time - st.session_state.last_bg_update > 3:
    bg_list = weather_backgrounds.get(weather_type, weather_backgrounds["clear"])
    st.session_state.bg_index = (st.session_state.bg_index + 1) % len(bg_list)
    st.session_state.bg_url = bg_list[st.session_state.bg_index]
    st.session_state.last_bg_update = current_time
    st.session_state.bg_transition = "opacity 1s ease-in-out"
    st.rerun()

# Apply the background with smooth transition
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{st.session_state.bg_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        transition: {st.session_state.bg_transition};
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.3);
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display weather information if city is entered and found
if city and weather:
    # SVGs for animated graphics
    wind_svg = """
    <span class="wind-anim">
    <svg viewBox="0 0 48 48" fill="none">
        <path d="M8 24h24a6 6 0 1 0 0-12" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
        <path d="M12 32h20a4 4 0 1 1 0 8" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
    </svg>
    </span>
    """
    humidity_svg = """
    <span class="humidity-anim">
    <svg viewBox="0 0 32 32" fill="none">
        <path d="M16 4C16 4 6 16 6 22a10 10 0 0 0 20 0C26 16 16 4 16 4Z" fill="#4fc3f7" stroke="#fff" stroke-width="2"/>
    </svg>
    </span>
    """
    temp_svg = """
    <span class="temp-anim">
    <svg viewBox="0 0 32 32" fill="none">
        <rect x="13" y="6" width="6" height="16" rx="3" fill="#ff9800" stroke="#fff" stroke-width="2"/>
        <circle cx="16" cy="25" r="5" fill="#ff9800" stroke="#fff" stroke-width="2"/>
    </svg>
    </span>
    """

    icon_code = weather.get('icon', '01d')
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"

    st.markdown(
        """
        <style>
        .weather-card {
            background: rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: #fff;
            padding: 32px 24px 24px 24px;
            margin-top: 30px;
            animation: fadeIn 1.2s;
            position: relative;
            overflow: hidden;
        }
        .weather-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        .weather-temp {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 8px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.18);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .weather-desc {
            font-size: 1.4rem;
            font-weight: 500;
            margin-bottom: 12px;
            text-transform: capitalize;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .weather-details {
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .wind-anim {
            display: inline-block;
            vertical-align: middle;
            margin-right: 6px;
        }
        .wind-anim svg {
            width: 32px;
            height: 32px;
            animation: windMove 1.2s linear infinite;
        }
        @keyframes windMove {
            0% { transform: translateX(0);}
            50% { transform: translateX(10px);}
            100% { transform: translateX(0);}
        }
        .humidity-anim {
            display: inline-block;
            vertical-align: middle;
            margin-right: 6px;
        }
        .humidity-anim svg {
            width: 28px;
            height: 28px;
            animation: dropBounce 1.5s infinite;
        }
        @keyframes dropBounce {
            0%, 100% { transform: translateY(0);}
            50% { transform: translateY(-8px);}
        }
        .temp-anim {
            display: inline-block;
            vertical-align: middle;
            margin-right: 6px;
        }
        .temp-anim svg {
            width: 28px;
            height: 28px;
            animation: tempGlow 1.5s infinite alternate;
        }
        @keyframes tempGlow {
            0% { filter: drop-shadow(0 0 0px #ff9800);}
            100% { filter: drop-shadow(0 0 12px #ff9800);}
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px);}
            to { opacity: 1; transform: translateY(0);}
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(icon_url, width=120)
    with col2:
        st.markdown(
            f"""
            <div class="weather-card">
                <div class="weather-title">Weather in {weather['city']}, {weather['country']}</div>
                <div class="weather-temp">{temp_svg} {weather['temp']}°C</div>
                <div class="weather-desc">
                    <img src="{icon_url}" width="36" style="vertical-align:middle;margin-right:6px;" />
                    {weather['desc'].capitalize()}
                </div>
                <div class="weather-details">
                    <div>{humidity_svg} <b>Humidity:</b> {weather['humidity']}%</div>
                    <div>{wind_svg} <b>Wind Speed:</b> {weather['wind']} m/s</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
elif city:
    st.error("City not found. Please check the name and try again.")