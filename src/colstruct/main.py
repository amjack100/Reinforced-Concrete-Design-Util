from dataclasses import dataclass
import click

from .ops import *
from .eval import *


@dataclass
class Column:
    """Class for holding data about a column"""

    P: float
    R: float
    Pg: float
    As: float

    def __init__(self, P: float, R: float, Pg: float, As: float):

        self.P = P
        self.R = R
        self.Pg = Pg
        self.As = As


@click.command()
@click.argument("section", type=click.STRING)
@click.argument("col_type", type=click.STRING)
@click.argument("length", type=click.INT)
@click.argument("live-load", type=click.INT)
@click.argument("dead-load", type=click.INT)
@click.argument("height", type=click.INT)
@click.argument("strength-concrete", type=click.FLOAT)
@click.argument("strength-steel", type=click.FLOAT)
def calc_column(
    section: str,
    col_type: str,
    length: int,
    live_load: int,
    dead_load: int,
    height: int,
    strength_concrete: float,
    strength_steel: float,
):

    P = design_load(live_load, dead_load)

    print(f"P (design load) = {P}")

    R = slenderness_reduction_factor(length, height, section)

    print(f"R (slenderness reduction factor) = {R}")

    str_redux = strength_reduction_factor(col_type)

    print(f"Strength reduction factor = {str_redux}")

    ecc_redux = eccentricity_factor(col_type)

    a = area(length, section=section)
    print(f"Column gross area = {a}")

    print(f"Eccentricity factor = {ecc_redux}")

    Pg = percent_steel(Pmax=P,R=R,sr=str_redux,e=ecc_redux,gross_area=a,fc=strength_concrete,Fy=strength_steel)

    As = area_of_steel(Pg,a)

    print(f"Area of steel = {As}")

    col = Column(P, R, Pg, As)

    if not verify_Pg(col.Pg):
        print(f"Percent steel {col.Pg} should be 0.01 < x < 0.08")
        return

    print(col)