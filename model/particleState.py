"""
    Element of the model.
    Contains the ParticleState enum.
"""
from enum import Enum


class ParticleState(Enum):
    """
    Contains all health states
    """
    HEALTHY = 1
    INFECTED = 2
    INFECTIOUS = 3
    IMMUNE = 4
    DECEASED = 5
