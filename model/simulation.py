"""
    Coordinator of the model.
    Contains the Simulation class.
"""
from PyQt5.QtCore import QMutex

from model.particle import Particle
from model.simulationParameter import SimulationParameter
from model.statistics import Statistics

particles = []
mutex_particles = QMutex()
mutex_statistics = QMutex()


# noinspection PyUnresolvedReferences
def add_particle(particle: Particle) -> None:
    """Adds a particle to the particles list

    Parameters
    ----------
    particle: Particle
        particle to add

    """
    particles.append(particle)


# noinspection PyUnresolvedReferences
class Simulation:
    """The simulation, the heart of the model

    Attributes
    ----------
    simulation_parameter : SimulationParameter
        the general simulation parameter object
    statistics: Statistics
            the general statistics object
    fps_counter : int
        contains the number of fps for the next day
    day : int
        contains the current day
    thread_manager : ThreadManager
        manager for the simulation threads
    """

    def __init__(self, data: dict, size_world: dict, preset_data: dict) -> None:
        """Inits the simulation

        Parameters
        ----------
        data: dict
            dict of the simulation parameter
        size_world: dict
            dict of the size of the world which contains the width and height
        preset_data: dict
            dict of the data of the preset
        """
        self.simulation_parameter = SimulationParameter(data)
        simulation_parameters = self.simulation_parameter.get_parameters()
        self.statistics = Statistics(int(simulation_parameters['humans']))
        self.fps_counter = 0
        self.day = 0
        particles.clear()
        for i in range(int(simulation_parameters['humans'])):
            add_particle(Particle(size_world, self.simulation_parameter))
        if preset_data is not None:
            for i in range(int(preset_data['infectious'])):
                self.init_infectious(particles[i])
            for i in range(int(preset_data['infectious']), int(preset_data['infectious']) + int(preset_data['immune'])):
                self.init_immune(particles[i])
            for i in range(int(preset_data['infectious']) + int(preset_data['immune']),
                           int(preset_data['infectious']) + int(preset_data['immune']) + int(preset_data['deceased'])):
                self.init_deceased(particles[i])
        else:
            for i in range(int(simulation_parameters['infected'])):
                self.init_infected(particles[i])
        self.statistics.write_csv(self.day)

        from model.thread_manager import ThreadManager
        self.thread_manager = ThreadManager(None, self.simulation_parameter, self.statistics, len(particles))

    def get_data(self) -> dict:
        """Returns the simulation data for the view

        Returns
        -------
        dict:
            contains the simulation data for the view
        """
        simulation_parameters = self.simulation_parameter.get_parameters()
        self.fps_counter += 1
        if self.fps_counter >= int(simulation_parameters['ticks_per_day']):
            self.fps_counter = 0
            self.day = self.day + 1
            self.statistics.write_csv(self.day)

        return {
            'particles': particles,
            'healthy': self.statistics.get_data_healthy(),
            'immune': self.statistics.get_data_immune(),
            'infected': self.statistics.get_data_infected(),
            'infectious': self.statistics.get_data_infectious(),
            'deceased': self.statistics.get_data_deceased(),
            'days': self.statistics.get_data_days(),
            'show_infection_radius': simulation_parameters['show_infection_radius'],
            'infection_radius': simulation_parameters['infection_radius'],
            'show_home': simulation_parameters['show_home'],
            'show_humans': simulation_parameters['show_humans'],
            'lockdown': simulation_parameters['lockdown'],
            'lockdown_state': simulation_parameters['lockdown_state'],
            'show_social_distance': simulation_parameters['show_social_distance'],
            'social_distance': simulation_parameters['social_distancing_distance']
        }

    def set_world_size(self, old_size: dict, new_size: dict) -> None:
        """Tells every particle that the size of the world changed

        Parameters
        ----------
        old_size: dict
            contains the old width and height of the world
        new_size: dict
            contains the new width and height of the world
        """
        for particle in particles:
            particle.set_world_size(old_size, new_size)

    def simulate(self) -> None:
        """Simulates a step"""
        self.thread_manager.simulate(self.day)

    def reset(self) -> None:
        """Resets the thread manager"""
        self.thread_manager.stop()

    def init_infected(self, particle: Particle) -> None:
        """Inits the particle as infected.
        Tells the statistic that a particle became infected.

        Parameters
        ----------
        particle: Particle
            particle to be infected
        """
        particle.becomes_infected(self.day)
        self.statistics.becomes_infected()

    def init_infectious(self, particle: Particle) -> None:
        """Inits the particle as infectious.
        Tells the statistic that a particle became infectious.

        Parameters
        ----------
        particle: Particle
            particle to be infected
        """
        particle.init_infectious(self.day)
        self.statistics.init_infectious()

    # noinspection PyUnresolvedReferences
    def init_immune(self, particle: Particle):
        """Inits the particle as immune. Tells the statistic that a particle became immune.

        Parameters
        ----------
        particle: Particle
            particle to be infected
        """
        particle.set_immune_state()
        self.statistics.init_immune()

    # noinspection PyUnresolvedReferences
    def init_deceased(self, particle: Particle):
        """Inits the particle as deceased. Tells the statistic that a particle became deceased.

        Parameters
        ----------
        particle: Particle
            particle to be infected
        """
        particle.set_deceased_state()
        self.statistics.init_deceased()

    def export_data(self, location: str, parameters: dict) -> bool:
        """Tells the statistic to export the data
        
        Parameters
        ----------
        location: String
            location where the file will be saved
        parameters: dict
            dict of the export parameters
        Returns
        -------
        bool:
            was the export successful
        """
        if parameters["include_parameters"]:
            return self.statistics.export_data(location, parameters, self.simulation_parameter.get_parameters())
        else:
            return self.statistics.export_data(location, parameters, None)

    def show_infection_radius_changed(self, radius: float) -> None:
        """Is called when the parameter show infection radius from the extended view section is toggled.
        Saves the change to the simulation parameters

        Parameters
        ----------
        radius: float
            show infection radius in view
        """
        if self.simulation_parameter is not None:
            self.simulation_parameter.show_infection_radius = radius

    def show_home_changed(self, show_home: bool) -> None:
        """Is called when the parameter show homes from the extended view section is toggled.
                Saves the change to the simulation parameters

        Parameters
        ----------
        show_home: bool
            show home in view
        """
        if self.simulation_parameter is not None:
            self.simulation_parameter.show_home = show_home

    def show_humans_changed(self, show_humans: bool) -> None:
        """Is called when the parameter show humans from the extended view section is toggled.
                Saves the change to the simulation parameters

        Parameters
        ----------
        show_humans: bool
            show humans in view
        """
        if self.simulation_parameter is not None:
            self.simulation_parameter.show_humans = show_humans

    def show_social_distance_changed(self, distance: float) -> None:
        """Is called when the parameter show social distance from the extended view section is toggled.
                Saves the change to the simulation parameters

        Parameters
        ----------
        distance: float
            show social distance in view
        """
        if self.simulation_parameter is not None:
            self.simulation_parameter.show_social_distance = distance

    def speed_changed(self, speed: int) -> None:
        """Is called, when the simulation speed is changed. Corrects the speed in the simulation_parameter object.

    Parameters
    ----------
    speed : int
        The value of the simulation speed slider
    """
        if self.simulation_parameter is not None:
            self.simulation_parameter.ticks_per_day = 100 - (10 * (speed / 1.2))
            self.simulation_parameter.simulation_speed = speed
