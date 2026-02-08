import pytest
import os
import sys
from argon2 import PasswordHasher

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from normalizers import *

# normCapital test cases
def testNormCapitalStripAndCapitals():
    assert normCapital("  john doe  ") == "John Doe"

def testNormCapitalEmptyString():
    assert normCapital("   ") == ""

# normDNI test cases
def testNormDNIFormatAndAnonymize():
    assert normDNI(" 12345678A ") == "******78A"

def testNormDNIDifferentFormat():
    assert normDNI("12-345678-A") == "******78A"

# normEmail test cases
def testNormEmailValid():
    assert normEmail("example@example.com ") == "example@example.com"

def testNormEmailInvalid():
    assert normEmail("invalid@emailcom") == "n/a"

def testNormEmailInvalid():
    assert normEmail("invalid-email.com") == "n/a"

# normPhone test cases
def testNormPhoneFormat():
    assert normPhone(" (123) 456-7890 ") == "1234567890"

# normCardNumber test cases
def testNormCardNumberHash():
    raw = "1234567890123456"
    hashed = normCardNumber(" 1234 5678 9012 3456 ")
    assert PasswordHasher().verify(hashed, raw)

# normCVV test cases
def testNormCVVAnonymize():
    assert normCVV(" 123 ") == "**3"

if __name__ == "__main__":
    pytest.main()
