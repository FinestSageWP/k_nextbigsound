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

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"{value:,.2f}"
    
    
def num(value):
    """Format value as comma separated."""
    if isinstance(value, int):
        return f"{value:,}"
    else:
        return value
    
    
def form(value):
    return round(value*100, 2)
    

def sort_nbs(value):
    arr = "DESC"
    if value == "else": 
        return f"SELECT artist, smi, cmb, ind FROM nbs"
    else:
        if value == "artist":
            arr = "ASC"
        return f"SELECT artist, smi, cmb, ind FROM nbs ORDER BY { value } { arr }"
    
    
def sort_smi(value):
    arr = "DESC"
    if value == "else": 
        return f"SELECT nbs.artist, smi.jan, smi.feb, smi.mar, smi.apr, smi.may, smi.jun, smi.jul, smi.aug, smi.sep, smi.oct, smi.nov_dec, smi.jan + smi.feb + smi.mar + smi.apr + smi.may + smi.jun + smi.jul + smi.aug + smi.sep + smi.oct + smi.nov_dec AS total FROM nbs INNER JOIN smi ON nbs.id=smi.artist_id ORDER BY total DESC"
    else:
        if value == "artist":
            arr = "ASC"
        return f"SELECT nbs.artist, smi.jan, smi.feb, smi.mar, smi.apr, smi.may, smi.jun, smi.jul, smi.aug, smi.sep, smi.oct, smi.nov_dec, smi.jan + smi.feb + smi.mar + smi.apr + smi.may + smi.jun + smi.jul + smi.aug + smi.sep + smi.oct + smi.nov_dec AS total FROM nbs INNER JOIN smi ON nbs.id=smi.artist_id ORDER BY { value } { arr }"


def sort_cmb(value):
    arr = "DESC"
    if value == "else": 
        return f"SELECT nbs.artist, cmb.jan, cmb.feb, cmb.mar, cmb.apr, cmb.may, cmb.jun, cmb.jul, cmb.aug, cmb.sep, cmb.oct, cmb.nov_dec, cmb.jan + cmb.feb + cmb.mar + cmb.apr + cmb.may + cmb.jun + cmb.jul + cmb.aug + cmb.sep + cmb.oct + cmb.nov_dec AS total FROM nbs INNER JOIN cmb ON nbs.id=cmb.artist_id ORDER BY total DESC"
    else:
        if value == "artist":
            arr = "ASC"
        return f"SELECT nbs.artist, cmb.jan, cmb.feb, cmb.mar, cmb.apr, cmb.may, cmb.jun, cmb.jul, cmb.aug, cmb.sep, cmb.oct, cmb.nov_dec, cmb.jan + cmb.feb + cmb.mar + cmb.apr + cmb.may + cmb.jun + cmb.jul + cmb.aug + cmb.sep + cmb.oct + cmb.nov_dec AS total FROM nbs INNER JOIN cmb ON nbs.id=cmb.artist_id ORDER BY { value } { arr }"


def get(artist, chart, month):
    if month == "total" or chart == "ind":
        return f'SELECT { chart } FROM nbs WHERE artist = "{ artist }"'
    else:
        return f'SELECT { chart }.{ month } FROM { chart } INNER JOIN nbs ON { chart }.artist_id = nbs.id WHERE nbs.artist = "{ artist }"'