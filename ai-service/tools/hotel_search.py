import json
import os
import requests

from dotenv import load_dotenv

from schemas.hotel import (
    HotelRecommendation,
    HotelRecommendations,
)

from schemas.planner import TripRequirements
from .currency import get_currency
from .date_utils import calculate_trip_dates
load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")

BASE_URL = "https://serpapi.com/search"

def convert_property(property_data: dict) -> HotelRecommendation:

    nearby_places = property_data.get("nearby_places", [])

    if nearby_places:
        location = nearby_places[0].get("name", "Unknown")
    else:
        location = "Unknown"

    rate = property_data.get("rate_per_night", {})

    price = rate.get(
        "extracted_lowest",
        0,
    )

    price_text = rate.get(
        "lowest",
        "",
    )

    # ------------------------------------
    # Detect Currency Symbol
    # ------------------------------------

    if price_text.startswith("$"):
        currency = "USD"

    elif price_text.startswith("₹"):
        currency = "INR"

    elif price_text.startswith("€"):
        currency = "EUR"

    elif price_text.startswith("£"):
        currency = "GBP"

    elif price_text.startswith("AED"):
        currency = "AED"

    else:
        currency = "Unknown"

    return HotelRecommendation(

        name=property_data.get(
            "name",
            "Unknown",
        ),

        location=location,

        price_per_night=float(price),

        currency=currency,

        booking_url=property_data.get(
            "link",
        ),

        rating=float(
            property_data.get(
                "overall_rating",
                0,
            )
        ),

        hotel_class=property_data.get(
            "hotel_class",
        ),

        image_url=property_data.get(
            "images",
            [{}],
        )[0].get(
            "thumbnail"
        )
        if property_data.get("images")
        else None,

        amenities=property_data.get(
            "amenities",
            [],
        ),
    )

def parse_hotels(raw_response: dict) -> HotelRecommendations:

    properties = raw_response.get("properties", [])

    hotels = []

    for property_data in properties[:3]:

        hotels.append(
            convert_property(property_data)
        )

    return HotelRecommendations(
        hotels=hotels
    )

def search_hotels(
    trip_requirements: TripRequirements,
):

    check_in, check_out = calculate_trip_dates(
        trip_requirements.start_date,
        trip_requirements.end_date,
        trip_requirements.duration_days,
    )

    currency = get_currency(
        trip_requirements.destination
    )

    params = {

        "engine": "google_hotels",

        "q": trip_requirements.destination,

        "check_in_date": check_in,

        "check_out_date": check_out,

        "adults": trip_requirements.travelers or 1,

        "currency": currency,

        "hl": "en",

        "gl": "in",

        "api_key": SERP_API_KEY,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    raw_response = response.json()
    print("\n================ RAW HOTEL ================\n")

    print(
            json.dumps(
            raw_response["properties"][0],
            indent=4,
        )
    )

    print("\n===========================================\n")

    return parse_hotels(raw_response)
