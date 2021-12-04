"""
    Element of the model.
    Contains the Statistics class.
"""
import csv
import os
import zipfile

from PyQt5.QtWidgets import QApplication

from model.particleState import ParticleState


class Statistics:
    """The statistic of the simulation.

    Attributes
    ----------
    healthy : int
        contains the number of healthy particles
    infected : int
        contains the number of infected particles
    infectious : int
        contains the number of infectious particles
    immune : int
        contains the number of immune particles
    deceased : int
        contains the number of deceased particles
    data_days: list
        contains a list of total days
    data_healthy: list
        contains a list of healthy particles each day
    data_healthy: list
        contains a list of healthy particles each day
    data_infected: list
        contains a list of infected particles each day
    data_infectious: list
        contains a list of infectious particles each day
    data_immune: list
        contains a list of immune particles each day
    data_deceased: list
        contains a list of deceased particles each day
    """

    def __init__(self, healthy: int) -> None:
        """Inits the statistic

        Parameters
        ----------
        healthy: int
            number of healthy particles
        """
        self.healthy = int(healthy)
        self.infected = 0
        self.infectious = 0
        self.immune = 0
        self.deceased = 0

        self.data_days = []
        self.data_healthy = []
        self.data_infected = []
        self.data_infectious = []
        self.data_immune = []
        self.data_deceased = []

    """
    Getter
    """

    def get_data_days(self) -> list:
        """Returns the list of days

        Returns
        -------
        list:
            list of days
        """
        return self.data_days

    def get_data_healthy(self) -> list:
        """Returns the list of healthy particles per day

        Returns
        -------
        list:
            list of healthy particles per day
        """
        return self.data_healthy

    def get_data_infected(self) -> list:
        """Returns the list of infected particles per day

        Returns
        -------
        list:
            list of infected particles per day
        """
        return self.data_infected

    def get_data_infectious(self) -> list:
        """Returns the list of infectious particles per day

        Returns
        -------
        list:
            list of infectious particles per day
        """
        return self.data_infectious

    def get_data_immune(self) -> list:
        """Returns the list of immune particles per day

        Returns
        -------
        list:
            list of immune particles per day
        """
        return self.data_immune

    def get_data_deceased(self) -> list:
        """Returns the list of deceased particles per day

        Returns
        -------
        list:
            list of healthy deceased per day
        """
        return self.data_deceased

    """
    Export
    """

    def export_data(self, location: str, parameters: dict, simulation_parameter: dict) -> bool:
        """Writes and saves the export file at the specified location.

        Parameters
        ----------
        location: str
            location of the file
        parameters: dict
            dict of the export parameters
        simulation_parameter: dict
            dict of the simulation parameters

        Returns
        ---------
        bool:
            success
        """
        if location == "":
            return False

        if location.find("csv") != -1:
            file_type = "csv"
            location = location[:location.rfind(file_type)]
        elif location.find("png") != -1:
            file_type = "png"
            location = location[:location.rfind(file_type)]
        else:
            file_type = "zip"
            location = location[:location.rfind(file_type)]

        if file_type == "csv" or file_type == "zip":
            file = open(location + "csv", 'w', newline='')
            with file:
                header = [QApplication.instance().translate("Export header day", "Day"),
                          QApplication.instance().translate("Export header healthy", "Healthy"),
                          QApplication.instance().translate("Export header infected", "Infected"),
                          QApplication.instance().translate("Export header infectious", "Infectious"),
                          QApplication.instance().translate("Export header immune", "Immune"),
                          QApplication.instance().translate("Export header deceased", "Deceased")]
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                write = csv.writer(file)
                for i in range(0, len(self.data_days), int(parameters["granularity"])):
                    write.writerow([self.data_days[i], self.data_infected[i], self.data_infectious[i],
                                    self.data_immune[i], self.data_deceased[i]])

                if parameters['include_parameters']:
                    write.writerow(["Parameter"])
                    write.writerow([QApplication.instance().translate("Export parameter granularity", "Granularity"),
                                    parameters["granularity"]])
                    if simulation_parameter is not None:
                        for key in simulation_parameter:
                            if key == "risk_group_age":
                                if simulation_parameter['risk_group']:
                                    write.writerow([key, "Min:" + simulation_parameter[key]['min'],
                                                    "Max:" + simulation_parameter[key]['max']])
                            elif key == "risk_group_death_rate":
                                if simulation_parameter['risk_group']:
                                    write.writerow([key, simulation_parameter[key]])
                            elif key == "social_distancing_distance":
                                if simulation_parameter['social_distancing']:
                                    write.writerow([key, simulation_parameter[key]])
                            elif key == "lockdown_state":
                                if simulation_parameter['lockdown']:
                                    write.writerow([key, simulation_parameter[key]])
                            elif key == "quarantine_breakout":
                                if simulation_parameter['quarantine']:
                                    write.writerow([key, simulation_parameter[key]])
                            else:
                                write.writerow([key, simulation_parameter[key]])
        if file_type == "png" or file_type == "zip":
            parameters['plot_image'].export(location + "png")
        if file_type == "zip":
            # creates the zip file
            zip_file = zipfile.ZipFile(location + file_type, 'w')
            # calculates the file name and folder
            folder_location = location[:location.rfind("/")]
            file_name = location[location.rfind("/") + 1:]
            # switches in the folder
            os.chdir(folder_location)
            # saves the files in the zip
            zip_file.write(file_name + "png")
            zip_file.write(file_name + "csv")
            zip_file.close()
            # remove the temporary files
            os.remove(file_name + "png")
            os.remove(file_name + "csv")
        return True

    def write_csv(self, day: int) -> None:
        """Writes the current data every day in the data lists

        Parameters
        ----------
        day: int
            current day
        """
        if self.infected < 0:
            self.infectious += self.infected
            self.infected = 0
        self.data_days.append(day)
        self.data_healthy.append(self.healthy)
        self.data_infected.append(self.infected)
        self.data_infectious.append(self.infectious)
        self.data_immune.append(self.immune)
        self.data_deceased.append(self.deceased)

    """
    Change data
    """

    def becomes_infected(self) -> None:
        """Calculates the new data for one infection"""
        self.infected += 1
        self.healthy -= 1

    def becomes_infectious(self) -> None:
        """Calculates the new data for one particle becomes infectious"""
        self.infected -= 1
        self.infectious += 1

    def becomes_immune(self, pre_status: ParticleState) -> None:
        """Calculates the new data for one recovery which follows immunity"""
        self.immune += 1
        if pre_status == ParticleState.INFECTED:
            self.infected -= 1
        else:
            self.infectious -= 1

    def becomes_healthy(self, pre_status: ParticleState) -> None:
        """Calculates the new data for one recovery which follows no immunity"""
        self.healthy += 1
        if pre_status == ParticleState.INFECTED:
            self.infected -= 1
        else:
            self.infectious -= 1

    def becomes_deceased(self, pre_status: ParticleState) -> None:
        """Calculates the new data for one death"""
        if pre_status == ParticleState.INFECTED:
            self.infected -= 1
        else:
            self.infectious -= 1
        self.deceased += 1

    def init_infectious(self) -> None:
        """Calculates the init data for one infection"""
        self.healthy -= 1
        self.infectious += 1

    def init_immune(self) -> None:
        """Calculates the init data for one immune particle"""
        self.immune += 1
        self.healthy -= 1

    def init_deceased(self) -> None:
        """Calculates the init data for one death"""
        self.deceased += 1
        self.healthy -= 1
