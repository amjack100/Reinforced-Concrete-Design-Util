from math import pi, pow, ceil, sqrt
from enum import Enum

from .const import *

global verbose
verbose = True

    


def radius_gyration(length: float, section: str) -> float:
    """Evaluate the radius of gyration given a diameter"""

    # Based on page 743

    if section == SQUARE:
        return 0.3 * length

    if section == CIRCLE:
        return 0.25 * length

    raise ValueError("Section must be square or circle")


def area(length: int, section: str) -> float:
    """
    Evaluate area given a diameter
    """

    if section == SQUARE:
        return pow(length, 2)

    if section == CIRCLE:
        return pi * pow((length / 2), 2)

    raise ValueError("Section must be square or circle")


def strength_reduction_factor(col_type: str) -> float:
    """ Evaluate strength reduction factor based on column type """

    if col_type == SPIRAL:
        return 0.70

    if col_type == TIED:
        return 0.65

    raise ValueError("Column type must by tied or spiral")


def eccentricity_factor(col_type: str) -> float:

    if col_type == SPIRAL:
        return 0.80

    if col_type == TIED:
        return 0.85

    raise ValueError("Column type must by tied or spiral")


def design_load(LL: int, DL: int) -> float:
    """ Evaluate the design load given live load and dead load """

    result = (1.6 * LL) + (1.2 * DL)

    print(f"[DESIGN LOAD](1.6 * {LL}) + (1.2 * {DL}) = {result}")

    return result


def area_of_concrete(gross_area: float, area_of_steel: float) -> float:
    """
    Evaluate Ac, the area of concrete
    """

    return gross_area - area_of_steel


def slenderness_reduction_factor(length: float, height: float, section: str) -> float:
    """
    Evaluate R, slenderness reduction factor
    """

    r = radius_gyration(length, section)
    result = 1.07 - (0.008 * (height * 12 / r))

    print(f"[SLENDERNESS R FACTOR]1.07 - (0.008 * ({height} * 12 / {r})) = {result}")

    return result


def area_of_steel(percent_steel: float, gross_area: float) -> float:
    """
    Evaluate As, the area of steel
    """

    return percent_steel * gross_area


def percent_steel(
    Pmax,
    R: float,
    sr: float,
    e: float,
    gross_area: float,
    fc: float,
    Fy: float,
):
    """
    Evaluate Pg, the percentage of steel
    """
    # Pmax  R(0.65)(0.80)Ag[0.85 fc(1  pg)  Fypg
    # Note must fall within the range of 0.01 < pg < 0.08

    # R = slenderness_reduction_factor
    # sr = strength_reduction_factor
    # e = eccentricity_factor
    # fc = concrete_strength
    # Fy = yield_stress_of_steel
    print(
        f"(({Pmax} / ({R} * {sr} * 0.8 * {gross_area})) - ({e} * {fc})) / ({Fy} - {fc})"
    )

    return ((Pmax / (R * sr * 0.8 * gross_area)) - (e * fc)) / (Fy - fc)


def area_from_design(Pmax, R, sr, e, pg, fc, Fy, section: str):

    area = Pmax / (R * sr * 0.8 * (e * fc * (1 - pg) + (Fy * pg)))

    if section == SQUARE:
        area = ceil(sqrt(area))
        area = pow(area, 2)

    return area
