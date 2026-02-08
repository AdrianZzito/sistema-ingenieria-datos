import pandas as pd
import re
from argon2 import PasswordHasher

def normCapital(s):
    return s.strip().title()

def normDNI(s):
    s = s.strip().upper().replace("-", "").replace(" ", "")
    anon = "******" + s[6:9]
    return anon

def normEmail(s):
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    s = s.strip().lower()

    if re.fullmatch(regex, s):
        return s
    else:
        return "n/a"

def normPhone(s):
    return s.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

def normCardNumberRaw(s):
    return s.strip().upper().replace(" ", "")

def normCardNumber(s):
    s = normCardNumberRaw(s)
    ph = PasswordHasher()
    res = ph.hash(s)
    return res

def normCVV(s):
    s = s.strip().upper().replace(" ", "")
    anon = "**" + s[2]
    return anon
