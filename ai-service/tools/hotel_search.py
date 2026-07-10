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

def convert_property(property_data: dict, default_currency: str = "USD") -> HotelRecommendation:

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
    if not price and rate.get("extracted_before_taxes_fees"):
        price = rate.get("extracted_before_taxes_fees", 0)

    price_text = rate.get(
        "lowest",
        "",
    )

    # ------------------------------------
    # Detect Currency Symbol
    # ------------------------------------

    if price_text.startswith("$"):
        currency = "USD"

    elif price_text.startswith("₹") or "\u20b9" in price_text:
        currency = "INR"

    elif price_text.startswith("€"):
        currency = "EUR"

    elif price_text.startswith("£"):
        currency = "GBP"

    elif price_text.startswith("AED"):
        currency = "AED"

    else:
        currency = default_currency

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

def parse_hotels(raw_response: dict, trip_requirements: TripRequirements = None, default_currency: str = "USD", max_price_per_night: int = None) -> HotelRecommendations:

    properties = raw_response.get("properties", [])

    # Determine if user is explicitly asking for budget/backpacking accommodations or has a low budget limit
    is_budget = False
    if trip_requirements:
        if trip_requirements.travel_style and any(k in trip_requirements.travel_style.lower() for k in ["budget", "backpack", "hostel"]):
            is_budget = True
        if trip_requirements.preferences and trip_requirements.preferences.accommodation_type and any(k in trip_requirements.preferences.accommodation_type.lower() for k in ["hostel", "dorm"]):
            is_budget = True

    if max_price_per_night:
        if (default_currency == "INR" and max_price_per_night <= 2500) or (default_currency == "USD" and max_price_per_night <= 35):
            is_budget = True

    filtered_properties = []
    for property_data in properties:
        rate = property_data.get("rate_per_night", {})
        price = rate.get("extracted_lowest", 0)
        if not price:
            price = rate.get("extracted_before_taxes_fees", 0)

        # Skip items with no valid price
        if price <= 0:
            continue

        # If a max budget per night is defined, enforce it with a 15% grace margin for taxes/fees
        if max_price_per_night and max_price_per_night > 0 and price > max_price_per_night * 1.15:
            continue

        name = property_data.get("name", "").lower()
        prop_type = property_data.get("type", "").lower()

        # If not budget requested, filter out dorm beds and hostels to ensure accurate/realistic hotel prices
        if not is_budget:
            if "hostel" in name or "zostel" in name or "backpack" in name or prop_type == "hostel":
                continue
            # Also filter out abnormally low dorm rates (< 1500 INR or < 25 USD) when standard hotels/resorts are expected
            if default_currency == "INR" and price < 1500:
                continue
            if default_currency == "USD" and price < 25:
                continue

        filtered_properties.append(property_data)

    # Fallback if strict budget/filtering excluded everything
    if not filtered_properties and max_price_per_night:
        filtered_properties = [p for p in properties if p.get("rate_per_night", {}).get("extracted_lowest", 0) > 0]
    if not filtered_properties:
        filtered_properties = [p for p in properties if p.get("rate_per_night", {}).get("extracted_lowest", 0) > 0]
        if not filtered_properties:
            filtered_properties = properties

    hotels = []

    for property_data in filtered_properties[:3]:

        hotels.append(
            convert_property(property_data, default_currency=default_currency)
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

    # Calculate duration days accurately
    duration_days = trip_requirements.duration_days
    if not duration_days or duration_days <= 0:
        from datetime import datetime
        try:
            if check_in and check_out:
                d1 = datetime.strptime(check_in, "%Y-%m-%d")
                d2 = datetime.strptime(check_out, "%Y-%m-%d")
                duration_days = (d2 - d1).days
        except Exception:
            pass
    if not duration_days or duration_days <= 0:
        duration_days = 3

    # Calculate 50% hotel budget rule: (total_budget * 0.5) / duration_days
    max_price_per_night = None
    if trip_requirements.budget and trip_requirements.budget > 0:
        max_price_per_night = int((trip_requirements.budget * 0.5) / duration_days)
        print(f"\n[Budget Rule] Total Budget: {trip_requirements.budget} {currency} | Duration: {duration_days} days -> Max Hotel Budget: {max_price_per_night} {currency}/night")

    # Build intelligent search query so Google Hotels returns actual hotels & resorts tailored to preferences
    search_query_parts = [trip_requirements.destination or ""]

    if trip_requirements.preferences and trip_requirements.preferences.accommodation_type:
        search_query_parts.append(trip_requirements.preferences.accommodation_type)
    elif trip_requirements.travel_style:
        style = trip_requirements.travel_style.lower()
        if "luxury" in style:
            search_query_parts.append("luxury hotels resorts")
        elif "budget" in style or "backpack" in style:
            search_query_parts.append("budget hotels hostels")
        elif "resort" in style or "family" in style:
            search_query_parts.append("resorts")
        else:
            search_query_parts.append("hotels")
    else:
        search_query_parts.append("hotels resorts")

    search_query = " ".join(part for part in search_query_parts if part).strip()

    params = {

        "engine": "google_hotels",

        "q": search_query,

        "check_in_date": check_in,

        "check_out_date": check_out,

        "adults": trip_requirements.travelers or 1,

        "currency": currency,

        "hl": "en",

        "gl": "in",

        "api_key": SERP_API_KEY,
    }

    if max_price_per_night and max_price_per_night > 0:
        params["max_price"] = max_price_per_night

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    raw_response = response.json()
    print("\n================ RAW HOTEL ================\n")

    if raw_response.get("properties"):
        print(
            json.dumps(
                raw_response["properties"][0],
                indent=4,
                ensure_ascii=True,
            )
        )

    print("\n===========================================\n")

    return parse_hotels(raw_response, trip_requirements=trip_requirements, default_currency=currency, max_price_per_night=max_price_per_night)
