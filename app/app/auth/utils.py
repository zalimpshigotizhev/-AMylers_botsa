import re
from constants.common import (
    AGE, SEX,
    CANCEL
)


def is_valid_name(name):
    pattern = r"^[А-ЯЁA-ZİıŞşÇçĞğÜüÖö][а-яёa-zİıŞşÇçĞğÜüÖö'-]{1,49}( [А-ЯЁA-ZİıŞşÇçĞğÜüÖö][а-яёa-zİıŞşÇçĞğÜüÖö'-]{1,49})*$"
    return re.match(pattern, name) is not None


def is_valid_age(age):
    return age in AGE or age == CANCEL


def is_valid_sex(sex):
    return sex in SEX or sex == CANCEL


def is_valid_description(description):
    return len(description) <= 255
