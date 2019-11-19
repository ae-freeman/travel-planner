import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(destination):
    """Look up quote for symbol."""
    # url = "https://api.unsplash.com/search/photos"
    # params =

    response = requests.get(f"https://api.unsplash.com/search/photos", params={"query": {destination}}, headers={"Authorization": "Client-ID api key"})
    print(response)
    # response = requests.get(f"https://api.unsplash.com/search/photos?query={destination}&&client_id=api_key")
    # print(response)

    # Contact API
    # try:
    #     # api_key = os.environ.get("API_KEY")

    #     response.raise_for_status()
    # except requests.RequestException:
    #     return None


        #try pre-defining url params and headers then passing into get request

    # # Parse response
    # try:
    #     quote = response.json()
    #     return {
    #         "name": quote["companyName"],
    #         "price": float(quote["latestPrice"]),
    #         "symbol": quote["symbol"]
    #     }
    # except (KeyError, TypeError, ValueError):
    #     return None


# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"





#Exchange Rates API

def exchange_rate():

    try:
        response = requests.get("https://api.exchangeratesapi.io/latest")
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None

    # test_response = requests.get("https://api.exchangeratesapi.io/latest")
    # return test_response

