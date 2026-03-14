import requests

def search_neurologists(city):
    try:
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": f"neurologist in {city}",
            "format": "json",
            "limit": 5
        }

        headers = {
            "User-Agent": "BrainHemorrhageAI/1.0"
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        doctors = []

        for place in data:
            doctors.append({
                "name": place.get("display_name", "Unknown"),
                "address": place.get("display_name", "")
            })

        return doctors

    except Exception as e:
        print("OpenStreetMap Error:", e)
        return []