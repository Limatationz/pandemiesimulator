"""
    Coordinator of the simulator.
    Contains the Presenter class.
"""

from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFileDialog

from constants import FPS
from model.simulation import Simulation
from presenter.errors import InfectionError
from util import open_doc_in_browser
from view.aboutView import AboutView
from view.docView import DocView
from view.view import View


class Presenter(QtCore.QObject):
    """A Presenter which controls the model and the view.

    Attributes
    ----------
    ui : View
        the main view
    about_view : AboutView
        the about view
    doc_view : DocView
        the doc view
    simulation : Simulation
        the model
    is_simulation_running : bool
        contains if the simulation is running
    has_simulation_started : bool
        contains if the simulation has already started
    timer : QtCore.QTimer
        timer which calls the main loop 60 times a second
    trans_window : QTranslator
            contains the translator of the window
    trans_about_window : QTranslator
            contains the translator of the about window
    trans_view : QTranslator
            contains the translator of the view
    trans_presenter : QTranslator
            contains the translator of the presenter
    trans_export : QTranslator
            contains the translator of the export
    lang : str
        contains the language
    """

    def __init__(self) -> None:
        """ inits Presenter, creates a view and a model."""
        super(Presenter, self).__init__()
        # create the windows
        self.ui = View()
        self.about_view = AboutView()
        try:
            from PyQt5.QtWebEngineWidgets import QWebEngineView
            self.doc_view = DocView()
        except ImportError:
            self.doc_view = None

        self.simulation = None
        self.is_simulation_running = False
        self.has_simulation_started = False

        # create timer that will call the mainLoop every 1000/FPS milliseconds
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.main_loop)
        self.timer.start(int(1000 / FPS))

        # install translators
        self.trans_window, self.trans_about_window, self.trans_view, self.trans_presenter, self.trans_export = \
            QtCore.QTranslator(self), QtCore.QTranslator(self), QtCore.QTranslator(self), QtCore.QTranslator(self), \
            QtCore.QTranslator(self)
        QtCore.QCoreApplication.instance().installTranslator(self.trans_window)
        QtCore.QCoreApplication.instance().installTranslator(self.trans_about_window)
        QtCore.QCoreApplication.instance().installTranslator(self.trans_view)
        QtCore.QCoreApplication.instance().installTranslator(self.trans_presenter)
        QtCore.QCoreApplication.instance().installTranslator(self.trans_export)
        self.lang = 'de'
        self.change_lang()

        self.connect_ui_elements()

    def main_loop(self) -> None:
        """Main loop which is called 60 times per second.

        Tells the model to simulate a step. Request the simulation data from the model and sends it to the view."""
        if self.is_simulation_running:
            self.simulation.simulate()
            self.ui.update_data(self.simulation.get_data())

    def start_simulation(self) -> None:
        """Starts and stops the simulation. When no simulation is available, a new one is created."""
        if not self.has_simulation_started:
            self.create_simulation()
        else:
            if self.is_simulation_running:
                self.is_simulation_running = False
            else:
                self.is_simulation_running = True
            self.ui.switch_start_stop_buttons()

    def reset_simulation(self) -> None:
        """Resets the simulation and the view."""
        self.simulation.reset()
        self.has_simulation_started = False
        self.is_simulation_running = False
        self.simulation = None
        self.ui.reset_simulation()

    def create_simulation(self) -> None:
        """Creates the simulation.

        Request the parameters from the view, checks if they are valid and
        creates a SimulationParameter object which contains all parameters
        and starts the simulation. If the data is invalid, a warning_text is
        displayed."""
        try:
            data = self.ui.create_simulation()
            if int(data['humans']) < int(data['infected']):
                raise InfectionError()
            if data['preset'] != 0:
                preset_data = self.ui.get_current_preset_data()
            else:
                preset_data = None

            self.simulation = Simulation(data, self.ui.get_size_world(), preset_data)
            self.has_simulation_started = True
            self.start_simulation()
        except InfectionError:
            self.ui.reset_simulation()
            self.ui.show_warning(QtCore.QCoreApplication.instance().translate('Warning infected',
                                                                              "Warning: The number of infected "
                                                                              "people must not exceed that of "
                                                                              "humans."),
                                 "red", 10000)

    def connect_ui_elements(self) -> None:
        """Connects all signals of the view with the presenter."""
        self.ui.start_simulation_signal.connect(self.start_simulation)
        self.ui.reset_simulation_signal.connect(self.reset_simulation)
        self.ui.window_resized_signal.connect(self.resize_window)
        self.ui.simulation_speed_changed_signal.connect(self.speed_changed)
        self.ui.export_signal.connect(self.export_granularity)
        self.ui.export_confirmation_signal.connect(self.save_export)
        self.ui.show_about_signal.connect(self.show_about_view)
        self.ui.show_infection_radius_signal.connect(self.show_infection_radius_changed)
        self.ui.show_home_signal.connect(self.show_home_changed)
        self.ui.show_humans_signal.connect(self.show_humans_changed)
        self.ui.show_social_distance_signal.connect(self.show_social_distance_changed)
        self.ui.language_changed_signal.connect(self.change_lang)
        self.ui.open_doc_signal.connect(self.open_doc)
        self.ui.abort_export_signal.connect(self.abort_export)

    def resize_window(self) -> None:
        """Is called, when the window is resized. Tells the simulation that the size of the world has changed."""
        if self.simulation is not None:
            self.simulation.set_world_size(self.ui.get_old_size_world(), self.ui.get_size_world())
            self.ui.update_data(self.simulation.get_data())

    def speed_changed(self, speed: int) -> None:
        """Is called, when the simulation speed is changed. Corrects the speed in the simulation parameter via the
        simulation.

        Parameters
        ----------
        speed : int
            The value of the simulation speed slider
        """
        if self.simulation is not None:
            self.simulation.speed_changed(speed)

    def export_granularity(self) -> None:
        """Is called, when the user wants to start the export-process.
        Switches stacked widget from parameter to export and stops the simulation.
        If there is no simulation a warning_text will be displayed."""
        if not self.has_simulation_started:
            self.ui.show_warning(QtCore.QCoreApplication.instance().translate('Warning export',
                                                                              "Warning: No data is available yet. The "
                                                                              "simulation must first be started."),
                                 "red", 10000)
        else:
            self.ui.switch_parameter_widget()
            if self.is_simulation_running:
                self.start_simulation()
                self.ui.dis_enable_export(True)

    def save_export(self) -> None:
        """Is called, when the user wants to choose the file location where the exported data will be saved.
        Switches stacked widget from export to the parameters.
        Displays an information when the data is successfully exported."""
        export_parameter = self.ui.get_export_parameter()
        if not export_parameter['plot'] and not export_parameter['csv']:
            self.ui.show_warning(QtCore.QCoreApplication.instance().translate('Message export not chosen',
                                                                              "The export failed, because no option is "
                                                                              "selected."),
                                 "red", 5000)
            return
        options = QFileDialog.Options()
        location = ""
        if export_parameter['csv'] and export_parameter['plot']:
            location, _ = QFileDialog.getSaveFileName(self.ui,
                                                         QtCore.QCoreApplication.instance().translate('Export data',
                                                                                                      "Export data"),
                                                         "",
                                                         QtCore.QCoreApplication.instance().translate('Export file zip',
                                                                                                      "zip-file "
                                                                                                      "(*.zip)"),
                                                         options=options)
        elif export_parameter['csv']:
            location, _ = QFileDialog.getSaveFileName(self.ui,
                                                         QtCore.QCoreApplication.instance().translate('Export data',
                                                                                                      "Export data"),
                                                         "",
                                                         QtCore.QCoreApplication.instance().translate('Export file csv',
                                                                                                         "csv-file "
                                                                                                         "(*.csv)"),
                                                         options=options)
        elif export_parameter['plot']:
            location, _ = QFileDialog.getSaveFileName(self.ui,
                                                         QtCore.QCoreApplication.instance().translate('Export data',
                                                                                                      "Export data"),
                                                         "",
                                                         QtCore.QCoreApplication.instance().translate('Export file png',
                                                                                                      "png-file "
                                                                                                      "(*.png)"),
                                                         options=options)
        res = self.simulation.export_data(location, export_parameter)
        self.ui.switch_parameter_widget()
        if res:
            self.ui.show_warning(QtCore.QCoreApplication.instance().translate('Message export successful',
                                                                              "The simulation data was exported "
                                                                              "successfully."),
                                 "green", 5000)
        else:
            self.ui.show_warning(QtCore.QCoreApplication.instance().translate('Message export failed',
                                                                              "The export failed."),
                                 "red", 5000)
        self.ui.dis_enable_export(False)

    def abort_export(self) -> None:
        """Aborts export and changes the widget and enables the control"""
        self.ui.switch_parameter_widget()
        self.ui.dis_enable_export(False)

    def show_about_view(self) -> None:
        """Show the aboutWindow"""
        self.about_view.show()
        self.about_view.foregroundRole()

    def show_infection_radius_changed(self) -> None:
        """Is called when the parameter show infection radius from the extended view section is toggled.
        Saves the change to the simulation parameters via the simulation"""
        if self.simulation is not None:
            self.simulation.show_infection_radius_changed(self.ui.get_show_infection_radius())

    def show_home_changed(self) -> None:
        """Is called when the parameter show homes from the extended view section is toggled.
                Saves the change to the simulation parameters via the simulation"""
        if self.simulation is not None:
            self.simulation.show_home_changed(self.ui.get_show_home())

    def show_humans_changed(self) -> None:
        """Is called when the parameter show humans from the extended view section is toggled.
                Saves the change to the simulation parameters via the simulation"""
        if self.simulation is not None:
            self.simulation.show_humans_changed(self.ui.get_show_humans())

    def show_social_distance_changed(self) -> None:
        """Is called when the parameter show social distance from the extended view section is toggled.
                Saves the change to the simulation parameters via the simulation"""
        if self.simulation is not None:
            self.simulation.show_social_distance_changed(self.ui.get_show_social_distance())

    def change_lang(self) -> None:
        """Is called when the user wants to switch the language in the menubar.
        Changes the language and tells the view to translate itself."""
        if self.lang == 'de':
            self.lang = 'en'
            self.trans_presenter.load('resources/translations/presenter-en-en.qm')
            self.trans_window.load('resources/translations/window-de-en.qm')
            self.trans_about_window.load('resources/translations/about-de-en.qm')
            self.trans_view.load('resources/translations/view-en-en.qm')
            self.trans_export.load('resources/translations/export-en-en.qm')
        else:
            self.lang = 'de'
            self.trans_presenter.load('resources/translations/presenter-en-de.qm')
            self.trans_window.load('resources/translations/window-de-de.qm')
            self.trans_about_window.load('resources/translations/about-de-de.qm')
            self.trans_view.load('resources/translations/view-en-de.qm')
            self.trans_export.load('resources/translations/export-en-de.qm')
        self.ui.change_lang(self.lang)
        self.about_view.change_lang()

    def open_doc(self) -> None:
        """Opens the documentation in a new window or in a browser."""
        if self.doc_view is not None:
            self.doc_view.setFixedSize(QSize(self.ui.size().width(), self.ui.size().height()))
            self.doc_view.show()
        else:
            open_doc_in_browser()
