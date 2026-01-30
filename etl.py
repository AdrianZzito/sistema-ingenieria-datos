import pandas as pd
import re

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

def normCardNumber(s):
    s = s.strip().upper().replace(" ", "")
    anon = "************" + s[12:16]
    return anon

def normCVV(s):
    s = s.strip().upper().replace(" ", "")
    anon = "**" + s[2]
    return anon