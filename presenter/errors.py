"""
    Element of the presenter.
    Contains the error classes.
"""


class InfectionError(LookupError):
    """InfectionError is raised when the number of infected people is higher then the total number"""
