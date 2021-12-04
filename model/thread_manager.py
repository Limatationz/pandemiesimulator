"""
    Element of the model.
    Contains the ThreadManager class.
"""

from PyQt5.QtCore import QObject, QThreadPool

from model.simulation_thread import SimulationThread


class ThreadManager(QObject):
    """A ThreadManager which is manages the SimulationThreads.

        Attributes
        ----------
        simulation_parameter: SimulationParameter
            the general simulation parameter object
        number_of_particles: int
            contains the number of total particles
        threads: list
            contains a list of all SimulationThreads
        """

    def __init__(self, parent=None, simulation_parameter=None, statistics=None, number_of_particles=0):
        """Inits the ThreadManager.

        Parameters
        ----------
        parent: QObject
            parent Object
        simulation_parameter: SimulationParameter
            the general simulation parameter object
        statistics: Statistics
            the general statistics object
        number_of_particles: int
            number of total particles
        """
        super(ThreadManager, self).__init__(parent)
        self.simulation_parameter = simulation_parameter
        self.statistics = statistics
        self.number_of_particles = number_of_particles
        self.threads = []
        self.create_threads()

    def create_threads(self) -> None:
        """Creates SimulationThreads and append them to the thread list"""
        number_of_threads = QThreadPool.globalInstance().maxThreadCount()
        if self.number_of_particles < (5 * number_of_threads):
            number_of_threads = 1
        for cur_thread_id in range(number_of_threads):
            backend_thread = SimulationThread(cur_thread_id, number_of_threads, self.simulation_parameter,
                                              self.statistics)
            self.threads.append(backend_thread)

    def simulate(self, day: int) -> None:
        """Simulates all managed threads"""
        for thread in self.threads:
            thread.simulate(day)

    def stop(self) -> None:
        """Closes all SimulationThreads"""
        for thread in self.threads:
            thread.quit()
