import pandas as pd

def normCapital(s):
    return s.strip().title()

def normDNI(s):
    return s.strip().upper().replace("-", "").replace(" ", "")

def normEmail(s):
    return s.strip().lower()

def normPhone(s):
    return s.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

def normCardNumber(s):
    return s.strip().replace(" ", "").replace("-", "")

def normCVV(s):
    return s.strip()