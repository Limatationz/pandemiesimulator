"""
    Element of the model.
    Contains the SimulationThread class.
"""

from PyQt5.QtCore import QThread

from constants import BETTER_MOVEMENT_SPEED, BETTER_SIMULATION_SPEED
from model.particle import Particle
from model.simulation import mutex_particles, mutex_statistics, particles
from model.simulationParameter import SimulationParameter
from model.statistics import Statistics
from util import get_infected_state, get_infectious_state


class SimulationThread(QThread):
    """A thread which is managed by the SimulationManager and simulates an specific number of particles.

    Attributes
    ----------
    simulation_parameter: SimulationParameter
        the general simulation parameter object
    min: int
        contains the min index of the particle which will be simulated
    max: int
        contains the max index of the particle which will be simulated
    """

    def __init__(self, cur_thread_id: int, number_of_threads: int, simulation_parameter: SimulationParameter, statistics: Statistics) -> None:
        """Inits the SimulationThread

        Parameters
        ----------
        cur_thread_id: int
            id of the thread
        number_of_threads:
            total number of threads
        simulation_parameter: SimulationParameter
            the general simulation parameter object
        statistics: Statistics
            the general statistics object
        """
        super(SimulationThread, self).__init__()
        self.simulation_parameter = simulation_parameter
        self.statistics = statistics
        self.min = int(len(particles) / number_of_threads * cur_thread_id)
        if cur_thread_id == number_of_threads:
            self.max = int(len(particles))
        else:
            self.max = int(len(particles) / number_of_threads * (cur_thread_id + 1))

    def simulate(self, day: int) -> None:
        """Simulates a step for all assigned particles
        
        Parameters
        ----------
        day: int
            current day
        """

        simulation_parameters = self.simulation_parameter.get_parameters()
        speed = (int(simulation_parameters['simulation_speed']) / BETTER_SIMULATION_SPEED) * (
                int(simulation_parameters['movement_speed']) / BETTER_MOVEMENT_SPEED)
        social_distancing_or_all_collision = simulation_parameters['social_distancing'] \
                                             or simulation_parameters['all_collision']
        social_distancing_and_all_collision = simulation_parameters['social_distancing'] \
                                              and simulation_parameters['all_collision']

        infected_state = get_infected_state()
        infectious_state = get_infectious_state()

        for i in range(self.min, self.max, 1):
            if i < len(particles):
                mutex_particles.lock()
                p1 = particles[i]
                mutex_particles.unlock()

                for p2 in particles:
                    if p2 is not p1:
                        if social_distancing_or_all_collision:
                            if p1.collision_test(p2, simulation_parameters['social_distancing']):
                                p1.collision(p2)
                                p2.collision(p1)
                        if (p2.state == infectious_state or p2.state == infected_state) \
                                and not social_distancing_and_all_collision:
                            if p1.collision_test(p2, simulation_parameters['social_distancing']):
                                p1.collision(p2)
                                p2.collision(p1)
                        if p2.state == infectious_state:
                            if p1.test_infection(p2):
                                self.becomes_infected(p1, day)
                res = p1.simulate(speed, day)
                self.inspect_res(res, p1)

    def inspect_res(self, res: list, particle: Particle) -> None:
        """Inspects the result of a simulation step of a particle and changes the statistic if necessary

        Parameters
        ----------
        res: list
            a list of results what changed this step for the particle
        particle: Particle
            effected particle
        """
        if res[0]:
            mutex_statistics.lock()
            self.statistics.becomes_infectious()
            mutex_statistics.unlock()
        if res[1]:
            mutex_statistics.lock()
            self.statistics.becomes_deceased(res[3])
            mutex_statistics.unlock()
            mutex_particles.lock()
            particles.remove(particle)
            mutex_particles.unlock()
        else:
            if int(res[2]) == 1:
                mutex_statistics.lock()
                self.statistics.becomes_immune(res[3])
                mutex_statistics.unlock()
            if int(res[2]) == 2:
                mutex_statistics.lock()
                self.statistics.becomes_healthy(res[3])
                mutex_statistics.unlock()

    def becomes_infected(self, particle: Particle, day: int) -> None:
        """Infects the particle

        Parameters
        ----------
        particle: Particle
            effected particle
        day: int
            current day
        """
        particle.becomes_infected(day)
        mutex_statistics.lock()
        self.statistics.becomes_infected()
        mutex_statistics.unlock()
