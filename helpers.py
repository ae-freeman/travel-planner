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
#Get photo of destination


     # Contact API
    # try:
    #     # api_key = os.environ.get("API_KEY")

    #     response.raise_for_status()
    # except requests.RequestException:
    #     return None


    response = requests.get(f"https://api.unsplash.com/search/photos", params={"query": {destination}}, headers={"Authorization": "Client-ID api-key"})

    #Parse Response
    try:
        test = response.json()
        return test["results"][0]

    except (KeyError, TypeError, ValueError):
        return None


#Exchange Rates API

def exchange_rate(start_currency, end_currency):

    try:
        response = requests.get(f"https://api.exchangeratesapi.io/latest?base={start_currency}&&symbols={end_currency}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    #Parse Response
    try:
        result = response.json()
        return result
    except (KeyError, TypeError, ValueError):
        return None





def format(value):
    """Format value as USD."""
    return f"{value:,.2f}"