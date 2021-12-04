"""
    Element of the model.
    Contains the SimulationParameter class.
"""

from constants import BETTER_TICKS_PER_DAY, BETTER_SIMULATION_SPEED, DRAW_PARTICLE_RADIUS


class SimulationParameter:
    """A Presenter which controls the model and the view.

        Attributes
        ----------
        humans : int
            contains the total number of particles
        infected : int
            contains the number of infected particles
        ticks_per_day : float
            contains how long one day is
        movement_speed : int
            contains the speed ot the particles
        all_collision : bool
            do all particles collide (True) or only if a infected/infectious particle is involved (False)?
        infection_rate : int
            contains the percentage of infection when a healthy particle is in infection range of an infectious
        infection_radius : int
            contains the infection radius
        death_rate : int
            contains the percentage that a infected particle dies
        risk_group : bool
            is there a risk group?
        risk_group_age : dict
            contains the min and max age of the risk group
        risk_group_death_rate : int
            contains the percentage that a infected particle which is in the risk group dies
        incubation_time : int
            contains the average time between the infection and the time where the particle can infect others
        average_death_time : int
            contains the average time between the infection and the death
        average_recover_time : int
            contains the average time between the infection and the recovery
        reinfection_after_recovery : bool
            is there the possibility that a recovered particle can be infected again?
        reinfection_rate : int
            contains the percentage that a recovered particle can become infected again
        social_distancing : bool
            do particles keep a distance from one another?
        social_distancing_distance : int
            contains the social distance
        lockdown : bool
            is there a lockdown so that the particles can only move in an specific radius around their home?
        lockdown_state : int
            contains the state of the lockdown which influence the lockdown radius
        quarantine : bool
            do infected particles have to be quarantined?
        quarantine_breakout : int
            contains the percentage that a particle breaks out of the quarantine
        simulation_speed : int
            contains the speed of the simulation which influence the length of the days
        extended_view : bool
            is an extended presentation preferred?
        show_infection_radius : bool
            shows the infection radius of infectious particles if he can be displayed in the world
        show_home : bool
            shows the homes of the particles
        show_humans : bool
            shows people instead of particles
        show_social_distance : bool
            shows the social distance of particles if it can be displayed in the world
        """

    def __init__(self, data: dict) -> None:
        """ inits the parameters.

        Parameters
        ----------
        data : dict
            contains the simulation data from the view
        """
        self.humans = data['humans']
        self.infected = data['infected']
        self.ticks_per_day = 100 - (BETTER_TICKS_PER_DAY * (int(data['simulation_speed']) / BETTER_SIMULATION_SPEED))
        self.movement_speed = data['movement_speed']
        self.all_collision = data['all_collision']
        self.infection_rate = data['infection_rate']
        self.infection_radius = DRAW_PARTICLE_RADIUS * ((data['infection_radius'] * 2) + 1)
        self.death_rate = data['death_rate']
        self.risk_group = data['risk_group']
        self.risk_group_age = data['risk_group_age']
        self.risk_group_death_rate = data['risk_group_death_rate']
        self.incubation_time = data['incubation_time']
        self.average_death_time = data['average_death_time']
        self.average_recover_time = data['average_recover_time']
        self.reinfection_after_recovery = data['reinfection_after_recovery']
        self.reinfection_rate = data['reinfection_rate']
        self.social_distancing = data['social_distancing']
        self.social_distancing_distance = DRAW_PARTICLE_RADIUS * 2 * data['social_distancing_distance']
        self.lockdown = data['lockdown']
        self.lockdown_state = data['lockdown_state']
        self.quarantine = data['quarantine']
        self.quarantine_breakout = data['quarantine_breakout']
        self.simulation_speed = data['simulation_speed']
        self.extended_view = data['extended_view']
        self.show_infection_radius = data['show_infection_radius']
        self.show_home = data['show_home']
        self.show_humans = data['show_humans']
        self.show_social_distance = data['show_social_distance']

    def get_parameters(self) -> dict:
        """Returns the simulation parameters.

         Returns:
            dict:
                parameters of the simulation
        """
        return {
            'humans': self.humans,
            'infected': self.infected,
            'ticks_per_day': self.ticks_per_day,
            'movement_speed': self.movement_speed,
            'all_collision': self.all_collision,
            'infection_rate': self.infection_rate,
            'infection_radius': self.infection_radius,
            'death_rate': self.death_rate,
            'risk_group': self.risk_group,
            'risk_group_age': self.risk_group_age,
            'risk_group_death_rate': self.risk_group_death_rate,
            'incubation_time': self.incubation_time,
            'average_death_time': self.average_death_time,
            'average_recover_time': self.average_recover_time,
            'reinfection_after_recovery': self.reinfection_after_recovery,
            'reinfection_rate': self.reinfection_rate,
            'social_distancing': self.social_distancing,
            'social_distancing_distance': self.social_distancing_distance,
            'lockdown': self.lockdown,
            'lockdown_state': self.lockdown_state,
            'quarantine': self.quarantine,
            'quarantine_breakout': self.quarantine_breakout,
            'simulation_speed': self.simulation_speed,
            'extended_view': self.extended_view,
            'show_infection_radius': self.show_infection_radius,
            'show_home': self.show_home,
            'show_humans': self.show_humans,
            'show_social_distance': self.show_social_distance,
        }
