"""
    Contains static functions
"""
import csv
import datetime
import math
import os
import urllib.request
import webbrowser
from datetime import date, timedelta

from PyQt5.QtGui import QBrush, QPixmap, QPen

from constants import COLOR_GRAY, COLOR_YELLOW, COLOR_RED, COLOR_GREEN, POPULATION_GERMANY, BETTER_PRESET_SIMULATION, \
    COLOR_WHITE, COLOR_BLACK
from model.particleState import ParticleState


def get_healthy_state() -> ParticleState:
    """Returns the healthy ParticleState

    Returns
    -------
    ParticleState:
        HEALTHY
    """
    return ParticleState.HEALTHY


def get_infected_state() -> ParticleState:
    """Returns the infected ParticleState

    Returns
    -------
    ParticleState:
        INFECTED
    """
    return ParticleState.INFECTED


def get_infectious_state() -> ParticleState:
    """Returns the infectious ParticleState

    Returns
    -------
    ParticleState:
        INFECTIOUS
    """
    return ParticleState.INFECTIOUS


def get_immune_state() -> ParticleState:
    """Returns the immune ParticleState

    Returns
    -------
    ParticleState:
        IMMUNE
    """
    return ParticleState.IMMUNE


def get_deceased_state() -> ParticleState:
    """Returns the deceased ParticleState

    Returns
    -------
    ParticleState:
        DECEASED
    """
    return ParticleState.DECEASED


def get_particle_brush(state: ParticleState) -> QBrush:
    """Returns the brush of the particle

    Parameters
    ----------
    state: ParticleState
        state of the particle

    Returns
    -------
    QBrush:
        brush of the particle
    """
    if state == ParticleState.HEALTHY:
        return QBrush(COLOR_GRAY)
    elif state == ParticleState.INFECTED:
        return QBrush(COLOR_YELLOW)
    elif state == ParticleState.INFECTIOUS:
        return QBrush(COLOR_RED)
    else:
        return QBrush(COLOR_GREEN)


def get_particle_pixmap(state: ParticleState, in_risk_group: bool) -> QPixmap:
    """Returns the image of the human

    Parameters
    ----------
    state: ParticleState
        state of the particle
    in_risk_group: bool
        particle in risk group

    Returns
    -------
    QPixmap:
        image of the human
    """
    if state == ParticleState.HEALTHY:
        if in_risk_group:
            return QPixmap('resources/images/riskHuman.png')
        else:
            return QPixmap('resources/images/healthyHuman.png')
    elif state == ParticleState.INFECTED:
        return QPixmap('resources/images/infectedHuman.png')
    elif state == ParticleState.INFECTIOUS:
        return QPixmap('resources/images/infectiousHuman.png')
    elif state == ParticleState.IMMUNE:
        return QPixmap('resources/images/immuneHuman.png')


def get_color_for_chart_piece(number: int) -> list:
    """Returns the color for the piece of the pie chart

    Parameters
    ----------
    number: int
        id of the piece

    Returns
    -------
    list:
        contains the colors for the QPen and the QBrush
    """
    if number == 0:
        return [QPen(COLOR_WHITE, 2), COLOR_GRAY]
    elif number == 1:
        return [QPen(COLOR_WHITE, 2), COLOR_GREEN]
    elif number == 2:
        return [QPen(COLOR_WHITE, 2), COLOR_YELLOW]
    elif number == 3:
        return [QPen(COLOR_WHITE, 2), COLOR_RED]
    elif number == 4:
        return [QPen(COLOR_WHITE, 2), COLOR_BLACK]


def get_data_for_today_preset() -> dict:
    """Is called when the user wants to switch the language in the menubar.
            Changes the language and tells the view to translate itself.

    Source: https://github.com/CSSEGISandData/COVID-19

     Returns:
             dict: Data for the today's preset"""
    day_offset = 0
    while True:
        test_date = date.today() - timedelta(days=day_offset)
        test_date = test_date.strftime('%m-%d-%Y')
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
              "csse_covid_19_data/csse_covid_19_daily_reports/" + str(test_date) + ".csv"

        try:
            fp = urllib.request.urlopen(url)
            res = fp.read()
            text = res.decode("utf8")
            fp.close()
            lines = text.splitlines()
            data = csv.reader(lines)
            break
        except:
            day_offset += 1

    deaths, recovered, active = 0, 0, 0
    last_update = ""

    for row in data:
        if row[3] == "Germany":
            last_update = str(row[4])
            deaths += int(row[8])
            recovered += int(row[9])
            active += int(row[10])

    last_update = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
    last_update = last_update.strftime('%d.%m.%Y')
    deaths = math.ceil(deaths / POPULATION_GERMANY * BETTER_PRESET_SIMULATION)
    recovered = math.ceil(recovered / POPULATION_GERMANY * BETTER_PRESET_SIMULATION)
    active = math.ceil(active / POPULATION_GERMANY * BETTER_PRESET_SIMULATION)
    return {
        'last_update': last_update,
        'infectious': active,
        'immune': recovered,
        'deceased': deaths
    }


def open_doc_in_browser() -> None:
    """Opens the documentation in a browser."""
    webbrowser.open_new('file://' + os.path.realpath('doc/Pandemic-Simulator/index.html'))


def get_percentage(dif: int) -> int:
    """Calculate the percentage to die or recover dependent on the average time

    Parameters
    ----------
    dif: int
        contains the difference between the average and the current time

    Returns
    -------
    int:
        percentage to die or recovers
    """
    percentage = 5
    if dif == 2:
        percentage = 20
    elif dif == 1:
        percentage = 35
    elif dif == 0:
        percentage = 75
    return percentage


def get_percentage_infectious(dif: int) -> int:
    """Calculate the percentage to become infectious dependent on the average time

    Parameters
    ----------
    dif: int
        contains the difference between the average and the current time

    Returns
    -------
    int:
        percentage to become infectious
    """
    percentage = 5
    if dif == 1:
        percentage = 50
    elif dif == 0:
        percentage = 80
    return percentage
