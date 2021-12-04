"""
    Element of the model.
    Contains the particle class.
"""

import math
from random import *

from constants import *
from model.particleState import ParticleState
from model.simulationParameter import SimulationParameter
from util import get_percentage, get_percentage_infectious


class Particle:
    """A particle which represents a human in the simulation.

    Attributes
    ----------
    simulation_parameter : SimulationParameter
        the general simulation parameter object
    state : ParticleState
        contains the current health status
    pos_x : float
        contains the current x position in the world
    pos_y : float
        contains the current y position in the world
    home_pos_x : float
        contains the home y position in the world
    home_pos_y : float
        contains the home y position in the world
    counter_lock_change_direction : int
        contains the number of fps where the particle cannot change the direction randomly
    direction : int
        contains the direction in degree where the particle moves next
    last_collision_with: Particle
        contains the particle that had the last collision with the current particle
    day_of_infection: int
        contains the day of the infection
    will_die : bool
        contains if the particle will die after an infection
    day_death_test : int
        contains the last day where was tested if the particle would die
    day_heal_test : int
        contains the last day where was tested if the particle would recover
    day_infectious_test : int
        contains the last day where was tested if the particle would become infectious
    quarantine : bool
        contains if the particle is in quarantine
    is_immune : bool
        contains if the particle is immune
    age : int
        contains the age of the particle
    in_risk_group : bool
        contains if the particle is in the risk group
    world_width : float
        contains the width of the world
    world_height : float
        contains the height of the world
    """

    def __init__(self, size_world: dict, simulation_parameter: SimulationParameter) -> None:
        """Inits the particle

        Parameters
        ----------
        size_world: dict
            dict of the size of the world which contains the width and height
        simulation_parameter: SimulationParameter
            the general simulation parameter object
        """
        self.simulation_parameter = simulation_parameter
        self.state = ParticleState.HEALTHY
        self.pos_x = randint(DRAW_PARTICLE_RADIUS, int(size_world['width'] - HOUSE_PIXMAP_SIZE * 2)) - int(
            size_world['width'] - HOUSE_PIXMAP_SIZE * 2) / 2
        self.pos_y = randint(5, int(size_world['height'] - HOUSE_PIXMAP_SIZE * 2)) - int(
            size_world['height'] - HOUSE_PIXMAP_SIZE * 2) / 2
        self.home_pos_x = self.pos_x
        self.home_pos_y = self.pos_y
        self.counter_lock_change_direction = 0

        self.direction = self.compute_direction(0, 360)

        self.last_collision_with = None

        self.day_of_infection = 0
        self.will_die = False
        self.day_death_test = 0
        self.day_heal_test = 0
        self.day_infectious_test = 0
        self.quarantine = False
        self.is_immune = False

        self.age = randint(1, 100)
        self.in_risk_group = self.test_risk_group()

        self.world_width = int(size_world['width']) / 2
        self.world_height = int(size_world['height']) / 2

    """
    Getter
    """

    def get_pos(self) -> list:
        """Returns the current position

        Returns
        -------
        list:
            list which contains the current x and y position
        """
        return [self.pos_x, self.pos_y]

    def get_home_pos(self) -> list:
        """Returns the home position

        Returns
        -------
        list:
            list which contains the home x and y position
        """
        return [self.home_pos_x, self.home_pos_y]

    def get_last_collision(self):
        """Returns the particle from the last collision

        Returns
        -------
        Particle:
            particle of the last collision
        """
        return self.last_collision_with

    def get_state(self) -> ParticleState:
        """Returns the current state of the particle

        Returns
        -------
        ParticleState:
            the current state of the particle
        """
        return self.state

    def get_in_risk_group(self) -> bool:
        """Returns if the particle is in the risk group

        Returns
        -------
        bool:
            is the particle in the risk group?
        """
        return self.in_risk_group

    def get_quarantine(self) -> bool:
        """Returns if the particle is in quarantine

        Returns
        -------
        bool:
            is the particle quarantined?
        """
        return self.quarantine

    """
    Setter
    """

    def set_state(self, status: ParticleState) -> None:
        """Sets the current status

        Parameters
        ----------
        status: ParticleState
            new state of the particle
        """
        self.state = status

    def set_immune_state(self) -> None:
        """Sets the current status to immune"""
        self.state = ParticleState.IMMUNE

    def set_deceased_state(self) -> None:
        """Sets the current status to deceased"""
        self.state = ParticleState.DECEASED

    def set_world_size(self, old_size: dict, new_size: dict) -> None:
        """Sets the world size of the particle to the new size and
        corrects the x and y position relative to the new size

        Parameters
        ----------
        old_size: dict
            contains the old width and height of the world
        new_size: dict
            contains the new width and height of the world
        """

        if old_size['width'] != new_size['width'] and old_size['width'] > 0:
            self.pos_x *= new_size['width'] / old_size['width']
            self.home_pos_x *= new_size['width'] / old_size['width']
        if old_size['height'] != new_size['height'] and old_size['height'] > 0:
            self.pos_y *= new_size['height'] / old_size['height']
            self.home_pos_y *= new_size['height'] / old_size['height']

    def set_quarantine(self, quarantine: bool) -> None:
        """Calculates and sets if the particle will be quarantined

        Parameters
        ----------
        quarantine: bool
            will the particle be quarantined

        """
        if quarantine:
            if randint(0, 99) > int(self.simulation_parameter.get_parameters()['quarantine_breakout']):
                self.quarantine = True
        else:
            self.quarantine = False

    def set_will_die(self, day: int) -> None:
        """Calculates and sets if the particle will die

        Parameters
        ----------
        day: int
            current day

        """
        simulation_parameter = self.simulation_parameter.get_parameters()
        if self.in_risk_group:
            if randint(0, 99) < int(simulation_parameter['risk_group_death_rate']):
                self.will_die = True
        else:
            if randint(0, 99) < int(simulation_parameter['death_rate']):
                self.will_die = True
        self.day_of_infection = day

    def set_immune(self) -> None:
        """Calculates and sets if the particle is immune
        """
        if self.simulation_parameter.get_parameters()['reinfection_after_recovery']:
            if randint(0, 99) > int(self.simulation_parameter.get_parameters()['reinfection_rate']):
                self.is_immune = True
        else:
            self.is_immune = True

    def becomes_infected(self, day: int) -> None:
        """Inits the particle as infected and calculates if he dies, becomes immune or becomes quarantined.

        Parameters
        ----------
        day: int
            day of infection
        """
        self.set_state(ParticleState.INFECTED)
        self.set_will_die(day)
        self.set_immune()
        if self.simulation_parameter.get_parameters()['quarantine']:
            self.set_quarantine(True)

    def init_infectious(self, day: int) -> None:
        """Inits the particle as infectious and calculates if he dies, becomes immune or becomes quarantined.

        Parameters
        ----------
        day: int
            day of infection
        """
        self.set_state(ParticleState.INFECTIOUS)
        self.set_will_die(day)
        self.set_immune()
        if self.simulation_parameter.get_parameters()['quarantine']:
            self.set_quarantine(True)

    def simulate(self, speed: float, day: int) -> list:
        """Simulates a step

        Parameters
        ----------
        speed: float
            speed of the particle
        day: int
            current day

        Returns
        -------
        list:
            contains the effects that count happened in this step
        """
        previous_status = self.state
        self.move(speed)
        if self.state == ParticleState.INFECTED or self.state == ParticleState.INFECTIOUS:
            infectious = self.becomes_infectious(day)
            deceased = self.dies(day)
            immune = self.recovers(day)
            return [infectious, deceased, immune, previous_status]
        return [False, False, 0, previous_status]

    def move(self, speed: float) -> None:
        """Moves the particle if he is not quarantined. Checks also if the particle has to be pushed off

        Parameters
        ----------
        speed: float
            speed of the particle
        """
        if not self.quarantine:
            self.push_off_wall(speed)
            if self.simulation_parameter.get_parameters()['lockdown']:
                self.push_off_movement_radius()
            self.pos_x += math.cos(self.direction * math.pi / 180) * speed
            self.pos_y -= math.sin(self.direction * math.pi / 180) * speed

        if self.counter_lock_change_direction > 0:
            self.counter_lock_change_direction -= 1
        elif self.counter_lock_change_direction <= 0:
            self.last_collision_with = None

    def push_off_wall(self, speed: float) -> None:
        """Calculates of the particle is near a wall and pushes it off otherwise the particle can change its
        direction randomly

        Parameters
        ----------
        speed: float
            speed of the particle

        """
        dif = 50 + speed * 3
        if self.pos_y > (self.world_height - DRAW_PARTICLE_RADIUS - speed * 2 - BETTER_WALL_DETECTION):  # bottom wall
            self.direction = self.compute_direction(20, 160)
        elif self.pos_y < -(self.world_height - DRAW_PARTICLE_RADIUS - speed * 2 - BETTER_WALL_DETECTION):  # top wall
            self.direction = self.compute_direction(200, 340)
        if self.pos_x > (self.world_width - DRAW_PARTICLE_RADIUS - speed * 2 - BETTER_WALL_DETECTION):  # right wall
            self.direction = self.compute_direction(110, 250)
        elif self.pos_x < -(self.world_width - DRAW_PARTICLE_RADIUS - speed * 2 - BETTER_WALL_DETECTION):  # left wall
            self.direction = self.compute_direction(290, 70)
        if self.counter_lock_change_direction <= 0 \
                and not self.pos_y > (self.world_height - dif) \
                and not self.pos_y < -(self.world_height - dif) \
                and not self.pos_x > (self.world_width - dif) \
                and not self.pos_x < -(self.world_width - dif):
            if randint(0, 99) < PARTICLE_PROBABILITY_CHANGE_OF_DIRECTION:
                self.direction = self.compute_direction(0, 360)

    def push_off_movement_radius(self) -> None:
        """ Calculates of the particle is near the limit of the movement radius and pushes it off"""
        lockdown_state = self.simulation_parameter.get_parameters()['lockdown_state']
        delta_x = int(abs(self.pos_x - self.home_pos_x))
        delta_y = int(abs(self.pos_y - self.home_pos_y))
        radius = self.world_height / lockdown_state
        if self.world_height > self.world_width:
            radius = self.world_width / lockdown_state
        if math.sqrt(delta_x * delta_x + delta_y * delta_y) > radius and self.counter_lock_change_direction <= 0:
            self.turn_movement_radius(radius, (self.pos_x - self.home_pos_x), (self.pos_y - self.home_pos_y))

    def turn_movement_radius(self, radius: float, delta_x: float, delta_y: float) -> None:
        """Sets the direction if the particle collides with the movement radius

        Parameters
        ----------
        radius: float
            movement radius
        delta_x: float
            difference between the current and the home position in the x dimension
        delta_y: float
            difference between the current and the home position in the y dimension
        """
        if delta_y < -radius + 15:  # top wall
            self.direction = self.compute_direction(220, 320)
        elif delta_y > radius - 15:  # bottom wall
            self.direction = self.compute_direction(40, 140)
        elif delta_x > radius - 15:  # right wall
            self.direction = self.compute_direction(140, 220)
        elif delta_x < -radius + 15:  # left wall
            self.direction = self.compute_direction(310, 50)
        self.counter_lock_change_direction = \
            PARTICLE_TIME_DISABLE_CHANGE_OF_DIRECTION / self.simulation_parameter.get_parameters()['simulation_speed']

    def collision_distance(self, test_particle) -> float:
        """Calculates the distance between two particles

        Parameters
        ----------
        test_particle: Particle
            particle to test the collision

        Returns
        -------
        float:
            distance between the current and the test particle
        """
        pos_test_particle = test_particle.get_pos()
        delta_x = int(abs(self.pos_x - pos_test_particle[0]))
        delta_y = int(abs(self.pos_y - pos_test_particle[1]))
        return math.sqrt(delta_x * delta_x + delta_y * delta_y)

    def collision_test(self, test_particle, social_distancing: bool) -> bool:
        """Tests if the current and the test particle collides

        Parameters
        ----------
        test_particle: Particle
            particle to test the collision
        social_distancing: bool
            social distancing

        Returns
        -------
        bool:
            do the two particle collide?
        """
        if self.get_last_collision() == test_particle and test_particle.get_last_collision() == self:
            return False
        distance = self.collision_distance(test_particle)
        if social_distancing:
            return distance < int(self.simulation_parameter.get_parameters()['social_distancing_distance'])
        else:
            return distance < DRAW_PARTICLE_RADIUS * 2

    def collision(self, collided_particle) -> None:
        """Calculates and sets the new direction after a collision

        Parameters
        ----------
        collided_particle:
            particle which collides with the current
        """
        self.last_collision_with = collided_particle
        if self.direction <= 180:
            self.direction = self.direction + 180
        else:
            self.direction = self.direction - 180
        self.counter_lock_change_direction = \
            PARTICLE_TIME_DISABLE_CHANGE_OF_DIRECTION / self.simulation_parameter.get_parameters()['simulation_speed']

    def compute_direction(self, lower: int, upper: int) -> int:
        """Computes the new direction between two degrees

        Parameters
        ----------
        lower:
            minimum
        upper:
            maximum

        Returns
        -------
        int:
            new direction
        """
        self.counter_lock_change_direction = PARTICLE_TIME_DISABLE_CHANGE_OF_DIRECTION
        if lower > upper:
            return (randint(0, lower - upper) + 180) % 360
        else:
            return randint(lower, upper)

    def becomes_infectious(self, day: int) -> bool:
        """Calculates if the particle becomes infectious

        Parameters
        ----------
        day: int
            current day

        Returns
        -------
        bool:
            is the particle now infectious?
        """
        if self.state == ParticleState.INFECTED and self.day_infectious_test != day:
            self.day_infectious_test += 1
            dif = abs(
                int(self.day_of_infection) + int(self.simulation_parameter.get_parameters()['incubation_time']) - int(
                    day))
            percentage = get_percentage_infectious(dif)
            if (int(self.day_of_infection) + int(
                    self.simulation_parameter.get_parameters()['incubation_time'])) + 3 < int(day):
                self.set_state(ParticleState.INFECTIOUS)
                return True
            else:
                if randint(0, 99) < percentage and dif < 4:
                    self.set_state(ParticleState.INFECTIOUS)
                    return True
        return False

    def dies(self, day: int) -> bool:
        """Calculates if the particle dies

        Parameters
        ----------
        day: int
            current day

        Returns
        -------
        bool:
            does the particle die?
        """
        if self.will_die and self.day_death_test != day:
            self.day_death_test += 1
            day_of_death = int(
                int(self.day_of_infection) + int(self.simulation_parameter.get_parameters()['average_death_time']))
            dif = abs(int(day_of_death) - int(day))
            percentage = get_percentage(dif)
            if int(day_of_death) + 3 < int(day):
                self.set_state(ParticleState.DECEASED)
                return True
            else:
                if randint(0, 99) < percentage and dif < 4:
                    self.set_state(ParticleState.DECEASED)
                    return True
        return False

    def test_recovered(self, day_of_recovery: int, day: int) -> bool:
        """ Tests if the particle recovers

        Parameters
        ----------
        day_of_recovery: int
            day when the particle will recover average
        day: int
            current day

        Returns
        -------
        bool:
            does the particle recover today
        """
        dif = abs(int(day_of_recovery) - int(day))
        percentage = get_percentage(dif)
        if randint(0, 99) < percentage and dif < 4:
            return True
        elif int(day_of_recovery) + 3 < int(day):
            return True
        else:
            return False

    def recovers(self, day: int) -> int:
        """Calculates if the particle recovers

        Parameters
        ----------
        day: int
            current day

        Returns
        -------
        bool:
            does the particle recover?
        """
        if not self.will_die \
                and (self.state == ParticleState.INFECTED or self.state == ParticleState.INFECTIOUS) \
                and self.day_heal_test != day:
            self.day_heal_test += 1
            simulation_parameters = self.simulation_parameter.get_parameters()
            genesungstag = int(int(self.day_of_infection) + int(simulation_parameters['average_recover_time']))
            if simulation_parameters['reinfection_after_recovery'] and self.test_recovered(genesungstag, day):
                self.set_quarantine(False)
                if self.is_immune:
                    self.set_state(ParticleState.IMMUNE)
                    return 1
                else:
                    self.set_state(ParticleState.HEALTHY)
                    return 2
            elif self.test_recovered(genesungstag, day):
                self.set_state(ParticleState.IMMUNE)
                self.set_quarantine(False)
                return 1
        return 0

    def test_infection(self, test_particle) -> bool:
        """Calculates if the test particle infects the current particle

        Parameters
        ----------
        test_particle: Particle
            particle to test the infection

        Returns
        -------
        bool:
            does the test particle infects the current particle?
        """
        if self.state == ParticleState.HEALTHY \
                and test_particle.get_state() == ParticleState.INFECTIOUS \
                and not test_particle.quarantine:
            distance = self.collision_distance(test_particle)
            if distance < int(self.simulation_parameter.get_parameters()['infection_radius']):
                if randint(0, 99) < int(self.simulation_parameter.get_parameters()['infection_rate']):
                    return True
        return False

    def test_risk_group(self) -> bool:
        """Calculates if the particle is in the risk group

        Returns
        -------
        bool:
            is the particle in the risk group?
        """
        simulation_parameters = self.simulation_parameter.get_parameters()
        if simulation_parameters['risk_group'] \
                and int(simulation_parameters['risk_group_age']['min']) <= self.age <= \
                int(simulation_parameters['risk_group_age']['max']):
            return True
        return False
