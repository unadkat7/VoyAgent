# ============================================================
# Destination -> Currency Mapping
# ============================================================

DESTINATION_CURRENCY = {

    # UAE
    "dubai": "AED",
    "abu dhabi": "AED",

    # India
    "mumbai": "INR",
    "delhi": "INR",
    "dwarka": "INR",
    "goa": "INR",
    "jaipur": "INR",

    # Japan
    "tokyo": "JPY",
    "osaka": "JPY",

    # France
    "paris": "EUR",

    # Italy
    "rome": "EUR",
    "venice": "EUR",

    # Germany
    "berlin": "EUR",

    # UK
    "london": "GBP",

    # USA
    "new york": "USD",
    "los angeles": "USD",
    "las vegas": "USD",

    # Singapore
    "singapore": "SGD",

    # Thailand
    "bangkok": "THB",

    # Indonesia
    "bali": "IDR",

    # Turkey
    "istanbul": "TRY",

    # Russia
    "moscow": "RUB",

    # Switzerland
    "zurich": "CHF",

    # Australia
    "sydney": "AUD",

    # Canada
    "toronto": "CAD",
}


# ============================================================
# Helper Function
# ============================================================

def get_currency(destination: str | None) -> str:
    """
    Returns the currency code for a destination.

    Defaults to USD if the destination
    is unknown.
    """

    if not destination:
        return "USD"

    return DESTINATION_CURRENCY.get(
        destination.lower(),
        "USD",
    )