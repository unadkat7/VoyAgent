from pydantic import BaseModel


class HotelRecommendation(BaseModel):

    name: str

    location: str

    price_per_night: float

    currency: str

    booking_url: str | None

    rating: float

    amenities: list[str]


class HotelRecommendations(BaseModel):

    hotels: list[HotelRecommendation]
