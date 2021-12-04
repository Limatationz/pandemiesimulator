"""
    Contains constants and presets
"""
from PyQt5.QtGui import QColor

FPS = 60

BETTER_TICKS_PER_DAY = 10
BETTER_SIMULATION_SPEED = 1.4
BETTER_MOVEMENT_SPEED = 2
BETTER_WALL_DETECTION = 3

DRAW_PARTICLE_RADIUS = 5
DRAW_QUARANTINE_PARTICLE_WIDTH = 20
PARTICLE_TIME_DISABLE_CHANGE_OF_DIRECTION = 60
PARTICLE_PROBABILITY_CHANGE_OF_DIRECTION = 1

HUMAN_PIXMAP_SIZE = 10  # Unfortunately, to produce the same behavior as a particle, the image has to be so small
HOUSE_PIXMAP_SIZE = 15

# Colors
COLOR_RED = QColor('#FF645B')  # Infectious
COLOR_DARK_RED = QColor('#80322E')  # Risk group
COLOR_ORANGE = QColor('#FFA56B')
COLOR_YELLOW = QColor('#EDD974')  # Infected
COLOR_GREEN = QColor('#7AC485')  # Immune
COLOR_BLUE = QColor('#70B9DB')
COLOR_GRAY = QColor('#aaaaaa')  # Healthy
COLOR_BLACK = QColor('#000000')  # Deceased
COLOR_WHITE = QColor('#ffffff')

COLOR_TOGGLE_CHECKED = QColor('#2faeec')
COLOR_TOGGLE_NOT_CHECKED = QColor('#76797c')
COLOR_TOGGLE_CHECKED_DISABLED = QColor('#265780')
COLOR_TOGGLE_DISABLED = QColor('#626568')
COLOR_TOGGLE_HANDLE = QColor('#232629')
COLOR_TOGGLE_HANDLE_DISABLED = QColor('#464646')

POPULATION_GERMANY = 80000000
BETTER_PRESET_SIMULATION = 600

# Presets
PRESET_0_DE = "Benutzerdefiniert"
PRESET_0_EN = "Custom"
PRESET_1_NAME_DE = "COVID-19, DE, 01.03.2020"
PRESET_1_NAME_EN = "COVID-19, GER, 01.03.2020"
PRESET_1_PARAMETERS = {
    'humans': 100,
    'infectious': 1,
    'immune': 0,
    'deceased': 0,
    'infected': 0,
    'infection_rate': 70,
    'infection_radius': 5,
    'movement_speed': 3,
    'all_collision': False,
    'death_rate': 2,
    'risk_group': True,
    'risk_group_age': {'min': 65, 'max': 100},
    'risk_group_death_rate': 50,
    'incubation_time': 5,
    'average_death_time': 6,
    'average_recover_time': 12,
    'reinfection_after_recovery': False,
    'reinfection_rate': 0,
    'social_distancing': False,
    'social_distancing_distance': 1,
    'lockdown': False,
    'lockdown_state': 0,
    'quarantine': True,
    'quarantine_breakout': 40,
}
PRESET_2_NAME_DE = "COVID-19, DE, 01.11.2020"
PRESET_2_NAME_EN = "COVID-19, GER, 01.11.2020"
PRESET_2_PARAMETERS = {
    'humans': 100,
    'infectious': 2,
    'immune': 3,
    'deceased': 1,
    'infected': 0,
    'infection_rate': 70,
    'infection_radius': 5,
    'movement_speed': 2,
    'all_collision': False,
    'death_rate': 2,
    'risk_group': True,
    'risk_group_age': {'min': 65, 'max': 100},
    'risk_group_death_rate': 50,
    'incubation_time': 5,
    'average_death_time': 6,
    'average_recover_time': 12,
    'reinfection_after_recovery': False,
    'reinfection_rate': 0,
    'social_distancing': True,
    'social_distancing_distance': 4,
    'lockdown': True,
    'lockdown_state': 2,
    'quarantine': True,
    'quarantine_breakout': 20,
}
PRESET_3_NAME_DE = "COVID-19, DE, 01.01.2021"
PRESET_3_NAME_EN = "COVID-19, GER, 01.01.2021"
PRESET_3_PARAMETERS = {
    'humans': 100,
    'infectious': 3,
    'immune': 11,
    'deceased': 1,
    'infected': 0,
    'infection_rate': 70,
    'infection_radius': 5,
    'movement_speed': 2,
    'all_collision': False,
    'death_rate': 2,
    'risk_group': True,
    'risk_group_age': {'min': 65, 'max': 100},
    'risk_group_death_rate': 50,
    'incubation_time': 5,
    'average_death_time': 6,
    'average_recover_time': 12,
    'reinfection_after_recovery': False,
    'reinfection_rate': 0,
    'social_distancing': True,
    'social_distancing_distance': 4,
    'lockdown': True,
    'lockdown_state': 4,
    'quarantine': True,
    'quarantine_breakout': 20,
}
# Sources: https://github.com/CSSEGISandData/COVID-19,
# https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Steckbrief.html
PRESET_4_NAME_DE = "Cholera unbehandelt, Jemen, Mitte 2017"
PRESET_4_NAME_EN = "Cholera untreated, Yemen, Mid-2017"
PRESET_4_PARAMETERS = {
    'humans': 100,
    'infectious': 2,
    'immune': 40,
    'deceased': 0,
    'infected': 0,
    'infection_rate': 15,
    'infection_radius': 10,
    'movement_speed': 3,
    'all_collision': False,
    'death_rate': 70,
    'risk_group': False,
    'risk_group_age': {'min': 0, 'max': 100},
    'risk_group_death_rate': 0,
    'incubation_time': 3,
    'average_death_time': 7,
    'average_recover_time': 6,
    'reinfection_after_recovery': True,
    'reinfection_rate': 80,
    'social_distancing': False,
    'social_distancing_distance': 0,
    'lockdown': False,
    'lockdown_state': 0,
    'quarantine': False,
    'quarantine_breakout': 00,
}
PRESET_5_NAME_DE = "Cholera behandelt, Jemen, Mitte 2017"
PRESET_5_NAME_EN = "Cholera treats, Yemen, Mid-2017"
PRESET_5_PARAMETERS = {
    'humans': 100,
    'infectious': 2,
    'immune': 40,
    'deceased': 0,
    'infected': 0,
    'infection_rate': 15,
    'infection_radius': 10,
    'movement_speed': 3,
    'all_collision': False,
    'death_rate': 2,
    'risk_group': False,
    'risk_group_age': {'min': 0, 'max': 100},
    'risk_group_death_rate': 0,
    'incubation_time': 3,
    'average_death_time': 7,
    'average_recover_time': 6,
    'reinfection_after_recovery': True,
    'reinfection_rate': 80,
    'social_distancing': False,
    'social_distancing_distance': 0,
    'lockdown': False,
    'lockdown_state': 0,
    'quarantine': False,
    'quarantine_breakout': 0,
}
# Sources: https://de.wikipedia.org/wiki/Cholera#Die_Cholerainfektion,
# https://www.lzg.nrw.de/5aim-berichte/steckbrief/cholera.pdf,
# https://www.heilpraxisnet.de/themen/cholera-pandemie-geschichte-verlauf-und-hintergruende/,
# https://reliefweb.int/report/yemen/cholera-situation-yemen-august-2019
PRESET_6_NAME_DE = "Spanische Grippe, Weltweit, Herbst 1918"
PRESET_6_NAME_EN = "Spanish Flu, Worldwide, Fall 1918"
PRESET_6_PARAMETERS = {
    'humans': 100,
    'infectious': 20,
    'immune': 1,
    'deceased': 10,
    'infected': 0,
    'infection_rate': 10,
    'infection_radius': 5,
    'movement_speed': 3,
    'all_collision': False,
    'death_rate': 10,
    'risk_group': True,
    'risk_group_age': {'min': 70, 'max': 100},
    'risk_group_death_rate': 50,
    'incubation_time': 2,
    'average_death_time': 7,
    'average_recover_time': 7,
    'reinfection_after_recovery': True,
    'reinfection_rate': 95,
    'social_distancing': False,
    'social_distancing_distance': 0,
    'lockdown': False,
    'lockdown_state': 0,
    'quarantine': False,
    'quarantine_breakout': 0,
}
# Sources: https://de.wikipedia.org/wiki/Spanische_Grippe,
# Influenza: https://de.wikipedia.org/wiki/Influenza,
# https://www.infektionsschutz.de/erregersteckbriefe/grippe-influenza/
# many estimates

PRESETS = [[PRESET_0_DE, PRESET_0_EN], [PRESET_1_NAME_DE, PRESET_1_NAME_EN, PRESET_1_PARAMETERS],
           [PRESET_2_NAME_DE, PRESET_2_NAME_EN, PRESET_2_PARAMETERS],
           [PRESET_3_NAME_DE, PRESET_3_NAME_EN, PRESET_3_PARAMETERS], [],
           [PRESET_4_NAME_DE, PRESET_4_NAME_EN, PRESET_4_PARAMETERS],
           [PRESET_5_NAME_DE, PRESET_5_NAME_EN, PRESET_5_PARAMETERS],
           [PRESET_6_NAME_DE, PRESET_6_NAME_EN, PRESET_6_PARAMETERS], ]
