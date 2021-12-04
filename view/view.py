"""
    Element of the view.
    Contains the View class.
"""

import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5 import QtGui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QRegularExpression
from PyQt5.QtGui import QBrush, QPixmap, QRegularExpressionValidator

from constants import *
from util import *
from view.mainWindow import Ui_MainWindow


class View(QtWidgets.QMainWindow, Ui_MainWindow):
    """A View which shows the Ui_MainWindow.

        Attributes
        ----------
        timer_hide_error_bar : QTimer
            contains the timer, which hides the message when it expires
        size_world : dict
            contains a dict with includes the width and height of the world
        old_size_world : dict
            contains a dict with includes the old width and height of the world
        size_diagram : dict
            contains a dict with includes the width and height of the diagram
        plot_healthy : PlotItem
            contains the plot for healthy particles
        plot_immune : PlotItem
            contains the plot for immune particles
        plot_infected : PlotItem
            contains the plot for infected particles
        plot_infectious : PlotItem
            contains the plot for infectious particles
        plot_deceased : PlotItem
            contains the plot for deceased particles
        lang : str
            contains the language of the view
        todays_preset : dict
            contains a dict which includes the name of the today's preset and its data
        current_preset : dict
            contains a dict which includes the name of the current preset and its data
        anim_error_bar: QPropertyAnimation
            contains the animation for the error bar
        warning_is_currently_shown : bool
            shows people instead of particles
        scene_welt: QGraphicsScene
            scene of the world
        scene_pi_chart: QGraphicsScene
            scene of the pi chart

    """
    start_simulation_signal = QtCore.pyqtSignal()  # is emitted when the start or stop button are pressed
    reset_simulation_signal = QtCore.pyqtSignal()  # is emitted when the reset button is pressed
    window_resized_signal = QtCore.pyqtSignal()  # is emitted when the window is resized
    export_signal = QtCore.pyqtSignal()  # is emitted when the export menu button is pressed
    show_about_signal = QtCore.pyqtSignal()  # is emitted when the about menu button is pressed
    export_confirmation_signal = QtCore.pyqtSignal()  # is emitted when the export confirmation button is pressed
    abort_export_signal = QtCore.pyqtSignal()  # is emitted when the back button of the export widget is pressed
    simulation_speed_changed_signal = QtCore.pyqtSignal(int)  # is emitted when the simulation speed slider changed
    show_infection_radius_signal = QtCore.pyqtSignal()  # is emitted when the show infection radius check changed
    show_social_distance_signal = QtCore.pyqtSignal()  # is emitted when the show social distance check changed
    show_home_signal = QtCore.pyqtSignal()  # is emitted when the show home check changed
    show_humans_signal = QtCore.pyqtSignal()  # is emitted when the show humans check changed
    language_changed_signal = QtCore.pyqtSignal()  # is emitted when the language is changed
    open_doc_signal = QtCore.pyqtSignal()  # is emitted when the documentation menu button is pressed

    def __init__(self) -> None:
        """Inits the View."""
        super(View, self).__init__()
        self.setupUi(self)

        self.size_world = {'width': 0, 'height': 0}
        self.old_size_world = {'width': 0, 'height': 0}
        self.size_diagram = {'width': 0, 'height': 0}

        self.plot_healthy = None
        self.plot_immune = None
        self.plot_infected = None
        self.plot_infectious = None
        self.plot_deceased = None
        self.widget_plot.setBackground('#1e1e1e')

        self.action_lang_german.setEnabled(False)
        self.lang = 'en'

        self.todays_preset = {'name_de': '', 'name_en': '', 'data': {}}
        self.current_preset = {'id': 0, 'name': '', 'data': {}}

        self.warning_is_currently_shown = False
        self.anim_error_bar = QPropertyAnimation(self.errorBar, b"pos")
        self.timer_hide_error_bar = QtCore.QTimer(self)

        self.scene_welt = QtWidgets.QGraphicsScene()
        self.view_welt.setScene(self.scene_welt)

        self.scene_pi_chart = QtWidgets.QGraphicsScene()
        self.view_pi_chart.setScene(self.scene_pi_chart)

        self.button_pi_chart.setDisabled(True)
        self.button_reset.setDisabled(True)

        self.set_icons()
        self.init_validators()
        self.connect_signals()
        self.init_frames()
        #self.init_today_preset()
        self.statusbar.hide()
        self.hide_warning()

    '''
    Getter
    '''

    def get_infected(self) -> str:
        """Returns the text from the field for the number of infected particles

        Returns
        -------
        str:
            number of infected particles
        """
        return self.eingabe_infiziert.text()

    def get_number_of_particles(self) -> str:
        """Returns the text from the field for the number of total particles

        Returns
        -------
        str:
            number of total particles
        """
        return self.eingabe_menschen.text()

    def get_average_death_time(self) -> str:
        """Returns the text from the field for the average time of death

        Returns
        -------
        str:
            average time of death
        """
        return self.eingabe_sterbezeitpunkt.text()

    def get_death_rate(self) -> str:
        """Returns the text from the field for the death rate

        Returns
        -------
        str:
            death rate
        """
        return self.eingabe_sterberate.text()

    def get_average_recovery_time(self) -> str:
        """Returns the text from the field for the average time of recovery

        Returns
        -------
        str:
            average time of recovery
        """
        return self.eingabe_genesungszeitpunkt.text()

    def get_reinfection(self) -> bool:
        """Returns the checked state from the checkbox for the reinfection

        Returns
        -------
        bool:
            reinfection
        """
        return self.check_reinfection.isChecked()

    def get_reinfection_rate(self) -> str:
        """Returns the text from the field for the reinfection rate

        Returns
        -------
        str:
            reinfection rate
        """
        return self.eingabe_wiederanstreckungsrate.text()

    def get_infection_rate(self) -> str:
        """Returns the text from the field for the infection rate

        Returns
        -------
        str:
            infection rate
        """
        return self.eingabe_infektionswahr.text()

    def get_infektion_radius(self) -> int:
        """Returns the value from the slider for the infection radius

        Returns
        -------
        str:
            infection radius
        """
        return self.slider_infection_radius.value()

    def get_incubation_time(self) -> str:
        """Returns the text from the field for the incubation time

        Returns
        -------
        str:
            incubation time
        """
        return self.eingabe_incubation_time.text()

    def get_simulation_speed(self) -> int:
        """Returns the value from the slider for the simulation speed

        Returns
        -------
        str:
            simulation speed
        """
        return self.slider_speed.value()

    def get_social_distancing(self) -> bool:
        """Returns the checked state from the checkbox for the social distancing

        Returns
        -------
        bool:
            social distancing
        """
        return self.check_social_distancing.isChecked()

    def get_social_distance(self) -> int:
        """Returns the value from the slider for the social distance

        Returns
        -------
        str:
            social distance
        """
        return self.slider_social_distancing.value()

    def get_lockdown(self) -> bool:
        """Returns the checked state from the checkbox for the lockdown

        Returns
        -------
        bool:
            lockdown
        """
        return self.check_lockdown.isChecked()

    def get_lockdown_state(self) -> int:
        """Returns the value from the slider for the lockdown state

        Returns
        -------
        str:
            lockdown state
        """
        return self.slider_lockdown.value()

    def get_quarantine(self) -> bool:
        """Returns the checked state from the checkbox for the quarantine

        Returns
        -------
        bool:
            quarantine
        """
        return self.check_quarantaene.isChecked()

    def get_quarantine_breakout_rate(self) -> str:
        """Returns the text from the field for the quarantine breakout rate

        Returns
        -------
        str:
            quarantine breakout rate
        """
        return self.eingabe_quarantaeneausbrecher.text()

    def get_movement_speed(self) -> int:
        """Returns the value from the slider for the movement speed

        Returns
        -------
        str:
            movement speed
        """
        return self.slider_bewegungsgeschw.value()

    def get_collision_all(self) -> bool:
        """Returns the checked state from the checkbox for the general collision

        Returns
        -------
        bool:
            general collision
        """
        return self.check_collision.isChecked()

    def get_extended_view(self) -> bool:
        """Returns the checked state from the checkbox for the extended view

        Returns
        -------
        bool:
            extended view
        """
        return self.check_extended_view.isChecked()

    def get_show_infection_radius(self) -> bool:
        """Returns the checked state from the checkbox for the visibility of the infection radius

        Returns
        -------
        bool:
            visibility of infection radius
        """
        return self.check_show_infection_radius.isChecked()

    def get_show_home(self) -> bool:
        """Returns the checked state from the checkbox for the visibility of homes

        Returns
        -------
        bool:
            visibility of homes
        """
        return self.check_show_home.isChecked()

    def get_export_data(self) -> bool:
        """Returns the checked state from the checkbox for the csv export

        Returns
        -------
        bool:
            export simulation parameters
        """
        return self.check_export_csv.isChecked()

    def get_export_granularity(self) -> str:
        """Returns the text from the field for the granularity

        Returns
        -------
        str:
            granularity
        """
        return self.eingabe_granulartaet.text()

    def get_export_include_parameters(self) -> bool:
        """Returns the checked state from the checkbox for the include of the parameters in the export

        Returns
        -------
        bool:
            export simulation parameters
        """
        return self.check_export_parameters.isChecked()

    def get_export_plot(self) -> bool:
        """Returns the checked state from the checkbox for the plot export

        Returns
        -------
        bool:
            export simulation parameters
        """
        return self.check_export_plot.isChecked()

    def get_risk_group(self) -> bool:
        """Returns the checked state from the checkbox for the risk group

        Returns
        -------
        bool:
            risk group
        """
        return self.check_risk_group.isChecked()

    def get_risk_group_age(self) -> dict:
        """Returns the values from the slider for the age of the risk group

        Returns
        -------
        dict:
            min and max age of the risk group
        """
        return {'min': self.range_risk_group_age.GetLowerValue(), 'max': self.range_risk_group_age.GetUpperValue()}

    def get_risk_group_death_rate(self) -> str:
        """Returns the text from the field for the death rate of the risk group

        Returns
        -------
        str:
            death rate of the risk group
        """
        return self.eingabe_risk_group_death_rate.text()

    def get_show_humans(self) -> bool:
        """Returns the checked state from the checkbox for the visibility of humans instead of particles

        Returns
        -------
        bool:
            visibility of humans
        """
        return self.check_show_humans.isChecked()

    def get_show_social_distance(self) -> bool:
        """Returns the checked state from the checkbox for the visibility of the social distance radius

        Returns
        -------
        bool:
            visibility of social distance radius
        """
        return self.check_show_social_distance.isChecked()

    def get_current_preset_data(self) -> dict:
        """Returns the data of the current preset

        Returns
        -------
        dict:
            data from the current preset
        """
        return self.current_preset['data']

    def get_size_world(self) -> dict:
        """Returns the size of the world

        Returns
        -------
        dict:
            size of the world
        """
        return self.size_world

    def get_old_size_world(self) -> dict:
        """Returns the old size of the world

        Returns
        -------
        dict:
            old size of the world
        """
        return self.old_size_world

    def get_size_diagram(self) -> dict:
        """Returns the size of the diagram

        Returns
        -------
        dict:
            size of the diagram
        """
        return self.size_diagram

    def connect_signals(self) -> None:
        """Connects all signals."""
        self.button_play.pressed.connect(self.start_simulation_signal.emit)
        self.button_stop.pressed.connect(self.start_simulation_signal.emit)
        self.button_reset.pressed.connect(self.reset_simulation_signal.emit)
        self.action_export_data.triggered.connect(self.export_signal.emit)
        self.confirm_export.pressed.connect(self.export_confirmation_signal.emit)
        self.check_quarantaene.stateChanged.connect(self.show_frame_quarantine)
        self.check_reinfection.stateChanged.connect(self.show_frame_reinfection)
        self.check_lockdown.stateChanged.connect(self.show_frame_lockdown)
        self.comboBox_preset.currentIndexChanged.connect(self.preset_changed)
        self.check_social_distancing.stateChanged.connect(self.show_frame_social_distancing)
        self.actionAbout.triggered.connect(self.show_about_signal.emit)
        self.button_pi_chart.pressed.connect(self.switch_diagrams)
        self.button_plot.pressed.connect(self.switch_diagrams)
        self.check_extended_view.stateChanged.connect(self.show_frame_extended_view)
        self.check_show_home.stateChanged.connect(self.show_home_signal.emit)
        self.check_show_infection_radius.stateChanged.connect(self.show_infection_radius_signal.emit)
        self.check_show_humans.stateChanged.connect(self.show_humans_signal.emit)
        self.check_show_social_distance.stateChanged.connect(self.show_social_distance_signal.emit)
        self.check_risk_group.stateChanged.connect(self.show_frame_risk_group)
        self.range_risk_group_age.valueChanged.connect(self.range_risk_group_age_changed)
        self.slider_lockdown.valueChanged.connect(self.lockdown_state_changed)
        self.slider_bewegungsgeschw.valueChanged.connect(self.movement_speed_changed)
        self.slider_infection_radius.valueChanged.connect(self.infection_radius_changed)
        self.slider_social_distancing.valueChanged.connect(self.social_distancing_distance_changed)
        self.slider_speed.valueChanged.connect(self.simulation_speed_changed)
        self.toolButton_error.clicked.connect(self.hide_warning)
        self.timer_hide_error_bar.timeout.connect(self.hide_warning)
        self.action_lang_english.triggered.connect(self.language_changed_signal.emit)
        self.action_lang_german.triggered.connect(self.language_changed_signal.emit)
        self.view_welt.sizeChanged.connect(self.window_resized)
        self.actionDocumentation.triggered.connect(self.open_doc_signal.emit)
        self.back_export.pressed.connect(self.abort_export_signal.emit)
        self.check_export_csv.stateChanged.connect(self.show_frame_export_csv)

    def set_icons(self) -> None:
        """Sets the icons."""
        self.setWindowIcon(QtGui.QIcon('resources/images/windowicon.png'))
        self.action_lang_german.setIcon(QtGui.QIcon('resources/images/flag_de.png'))
        self.action_lang_english.setIcon(QtGui.QIcon('resources/images/flag_uk.png'))

    def change_lang(self, lang: str) -> None:
        """Changes the language of the GUI

        Parameters
        ----------
        lang: str
            new language
        """
        self.lang = lang
        self.hide_warning()
        if lang == 'en':
            self.widget_plot.setLabel('bottom', 'Time', units='days')
            self.action_lang_english.setEnabled(False)
            self.action_lang_german.setEnabled(True)
        else:
            self.widget_plot.setLabel('bottom', 'Zeit', units='Tage')
            self.action_lang_english.setEnabled(True)
            self.action_lang_german.setEnabled(False)
        self.retranslateUi(self)
        self.init_presets(lang)

    def init_frames(self) -> None:
        """Inits the frames of the addition parameters as hidden."""
        self.show_frame_risk_group(False)
        self.show_frame_quarantine(False)
        self.show_frame_reinfection(False)
        self.show_frame_lockdown(False)
        self.show_frame_social_distancing(False)
        self.show_frame_extended_view(False)

    def show_frame_risk_group(self, checked: bool) -> None:
        """Show or hides the frame of the risk group

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_risk_group.show()
        else:
            self.frame_risk_group.hide()

    def show_frame_quarantine(self, checked: bool) -> None:
        """Show or hides the frame of the quarantine

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_quarantaeneausbrecher.show()
        else:
            self.frame_quarantaeneausbrecher.hide()

    def show_frame_lockdown(self, checked: bool) -> None:
        """Show or hides the frame of the lockdown

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_lockdown.show()
        else:
            self.frame_lockdown.hide()

    def show_frame_reinfection(self, checked: bool) -> None:
        """Show or hides the frame of the reinfection

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_wiederansteckungsrate.show()
        else:
            self.frame_wiederansteckungsrate.hide()

    def show_frame_social_distancing(self, checked: bool) -> None:
        """Show or hides the frame of the risk group

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_social_distancing.show()
            self.check_show_social_distance.setEnabled(True)
        else:
            self.frame_social_distancing.hide()
            self.check_show_social_distance.setEnabled(False)

    def show_frame_extended_view(self, checked: bool) -> None:
        """Show or hides the frame of the extended view

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_extended_view.show()
        else:
            self.frame_extended_view.hide()

    def show_frame_export_csv(self, checked: bool) -> None:
        """Show or hides the frame of the csv export

        Parameters
        ----------
        checked: bool
            True: show
            False: hide
        """
        if checked:
            self.frame_export_csv.show()
        else:
            self.frame_export_csv.hide()

    def init_validators(self) -> None:
        """Inits the validators of the text fields."""
        percentage_with_null_val = QRegularExpressionValidator(QRegularExpression("(0)|(100)|([1-9]\\d{0,1})"))
        percentage_without_null_val = QRegularExpressionValidator(QRegularExpression("(100)|([1-9]\\d{0,1})"))
        self.eingabe_menschen.setValidator(percentage_without_null_val)
        self.eingabe_infektionswahr.setValidator(percentage_with_null_val)
        self.eingabe_sterberate.setValidator(percentage_with_null_val)
        self.eingabe_incubation_time.setValidator(percentage_with_null_val)
        self.eingabe_sterbezeitpunkt.setValidator(percentage_with_null_val)
        self.eingabe_granulartaet.setValidator(percentage_with_null_val)
        self.eingabe_quarantaeneausbrecher.setValidator(percentage_with_null_val)
        self.eingabe_genesungszeitpunkt.setValidator(percentage_with_null_val)
        self.eingabe_wiederanstreckungsrate.setValidator(percentage_with_null_val)
        self.eingabe_risk_group_death_rate.setValidator(percentage_with_null_val)

    def reset_simulation(self) -> None:
        """Resets the view."""
        self.preset_changed(self.current_preset['id'])
        self.scene_welt.clear()
        self.scene_pi_chart.clear()
        self.widget_plot.clear()
        self.stackedWidget_start_stop.setCurrentIndex(0)
        self.dis_enable_preset_selection(False)
        self.button_reset.setEnabled(False)
        self.show_warning(QtWidgets.QApplication.instance().translate('Message reset',
                                                                      "Simulation successfully reset."),
                          "green", 3000)

    def reset_displays(self) -> None:
        """Resets the displays with the statistics."""
        self.lcd_verstorben.display(str(0))
        self.lcd_genesen.display(str(0))
        self.lcd_infiziert.display(str(0))
        self.lcd_gesund.display(str(0))
        self.lcd_tag.display(str(0))

    def window_resized(self, old_width: int, old_height: int, new_width: int, new_height: int) -> None:
        """Sets the sizes of the QGraphicsViews and emits the resized signal.

        Parameters
        ----------
        old_width: int
            old width
        old_height: int
            old height
        new_width: int
            new width
        new_height: int
            new height
        """
        self.old_size_world['width'] = old_width
        self.old_size_world['height'] = old_height
        self.size_world['width'] = new_width
        self.size_world['height'] = new_height
        self.size_diagram['width'] = self.view_pi_chart.size().width()
        self.size_diagram['height'] = self.view_pi_chart.size().height()
        self.scene_welt = QtWidgets.QGraphicsScene()
        self.view_welt.setScene(self.scene_welt)
        self.scene_pi_chart = QtWidgets.QGraphicsScene()
        self.view_pi_chart.setScene(self.scene_pi_chart)
        self.window_resized_signal.emit()

    def switch_start_stop_buttons(self) -> None:
        """Switches the start and stop buttons"""
        if self.stackedWidget_start_stop.currentIndex() == 0:  # simulation is not running
            self.stackedWidget_start_stop.setCurrentIndex(1)
            self.show_warning(QtWidgets.QApplication.instance().translate('Message Start', "Simulation started."),
                              "green", 3000)
            self.check_pi_chart_module()
        else:  # simulation is running
            self.stackedWidget_start_stop.setCurrentIndex(0)
            self.show_warning(QtWidgets.QApplication.instance().translate('Message Stopped', "Simulation stopped."),
                              "green", 3000)

    def dis_enable_inputs(self, b: bool) -> None:
        """Switches the dis and enable state of the inputs.

        Parameters
        ----------
        b: bool
            True: disable
            False: enable
        """
        self.eingabe_infiziert.setEnabled(not b)
        self.eingabe_sterberate.setEnabled(not b)
        self.eingabe_infektionswahr.setEnabled(not b)
        self.eingabe_menschen.setEnabled(not b)
        self.eingabe_sterbezeitpunkt.setEnabled(not b)
        self.eingabe_incubation_time.setEnabled(not b)
        self.eingabe_quarantaeneausbrecher.setEnabled(not b)
        self.slider_bewegungsgeschw.setEnabled(not b)
        self.check_collision.setEnabled(not b)
        self.slider_lockdown.setEnabled(not b)
        self.check_quarantaene.setEnabled(not b)
        self.eingabe_quarantaeneausbrecher.setEnabled(not b)
        self.eingabe_genesungszeitpunkt.setEnabled(not b)
        self.check_reinfection.setEnabled(not b)
        self.check_lockdown.setEnabled(not b)
        self.eingabe_wiederanstreckungsrate.setEnabled(not b)
        self.slider_infection_radius.setEnabled(not b)
        self.check_social_distancing.setEnabled(not b)
        self.slider_social_distancing.setEnabled(not b)
        self.check_risk_group.setEnabled(not b)
        self.range_risk_group_age.setEnabled(not b)
        self.eingabe_risk_group_death_rate.setEnabled(not b)

    def disable_inputs_for_todays_preset(self) -> None:
        """Switches the dis and enable state of the inputs for the todays preset."""
        self.eingabe_infiziert.setEnabled(False)
        self.eingabe_menschen.setEnabled(False)
        self.eingabe_sterberate.setEnabled(True)
        self.eingabe_infektionswahr.setEnabled(True)
        self.eingabe_sterbezeitpunkt.setEnabled(True)
        self.eingabe_incubation_time.setEnabled(True)
        self.eingabe_quarantaeneausbrecher.setEnabled(True)
        self.slider_bewegungsgeschw.setEnabled(True)
        self.check_collision.setEnabled(False)
        self.slider_lockdown.setEnabled(True)
        self.check_quarantaene.setEnabled(True)
        self.eingabe_quarantaeneausbrecher.setEnabled(True)
        self.eingabe_genesungszeitpunkt.setEnabled(True)
        self.check_reinfection.setEnabled(True)
        self.check_lockdown.setEnabled(True)
        self.eingabe_wiederanstreckungsrate.setEnabled(True)
        self.slider_infection_radius.setEnabled(True)
        self.check_social_distancing.setEnabled(True)
        self.slider_social_distancing.setEnabled(True)
        self.check_risk_group.setEnabled(True)
        self.range_risk_group_age.setEnabled(True)
        self.eingabe_risk_group_death_rate.setEnabled(True)

    def dis_enable_preset_selection(self, b: bool) -> None:
        """Switches the dis and enable state of the preset selection.

        Parameters
        ----------
        b: bool
            True: disable
            False: Enable
        """
        self.comboBox_preset.setEnabled(not b)

    def dis_enable_export(self, b: bool) -> None:
        """Switches the dis and enable state of the simulation control.

        Parameters
        ----------
        b: bool
            True: disable
            False: Enable
        """
        self.button_reset.setEnabled(not b)
        self.button_stop.setEnabled(not b)
        self.button_play.setEnabled(not b)

    def update_data(self, data: dict) -> None:
        """Updates the view.

        Parameters
        ----------
        data: dict
            data of the step
        """
        self.scene_welt.clear()
        self.draw_particles(data['particles'], data['show_infection_radius'], data['infection_radius'],
                            data['show_home'], data['show_humans'], data['show_social_distance'],
                            data['social_distance'])

        self.lcd_verstorben.display(str(data['deceased'][-1]))
        self.lcd_genesen.display(str(data['immune'][-1]))
        self.lcd_infiziert.display(str(data['infected'][-1]))
        self.lcd_infektioes.display(str(data['infectious'][-1]))
        self.lcd_gesund.display(str(data['healthy'][-1]))
        self.lcd_tag.display(str(data['days'][-1]))

        if self.stackedWidget_diagrams.currentIndex() == 0:
            self.create_pi_chart(data)
        self.update_plot(data)

    def draw_particles(self, particles: list, show_infection_radius: bool, infection_radius: float,
                       show_home: bool, show_humans: bool, show_social_distance: bool, social_distance: float) -> None:
        """Draws the particles and related information in the world

        Parameters
        ----------
        particles: list
            list of all particles
        show_infection_radius: bool
            show infection radius
        infection_radius: float
            infection radius
        show_home: bool
            show homes
        show_humans: bool
            show humans instead of particles
        show_social_distance: bool
            show social distance
        social_distance: float
            social distance
        """
        infectious_state, deceased_state = get_infectious_state(), get_deceased_state()

        for particle in particles:
            if particle.get_state() != deceased_state:
                x, y = particle.get_pos()
                home_x, home_y = particle.get_home_pos()
                if show_home:
                    self.draw_home(home_x, home_y)
                if particle.get_quarantine():
                    self.draw_quarantine(x, y)
                if show_humans:
                    self.draw_humans(x, y, get_particle_pixmap(particle.get_state(), particle.get_in_risk_group()))
                else:
                    self.draw_particle(x, y, get_particle_brush(particle.get_state()), particle.get_in_risk_group())
                if show_infection_radius and particle.get_state() == infectious_state:
                    self.draw_infection_radius(x, y, infection_radius)
                if show_social_distance:
                    self.draw_social_distance(x, y, social_distance)

    def draw_particle(self, x: float, y: float, brush: QBrush, in_risk_group: bool) -> None:
        """Draws the particle.

        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle
        brush: QBrush
            brush of the particle
        in_risk_group: bool
            in risk group
        """
        pen = QPen(COLOR_BLACK)
        if not in_risk_group:
            self.scene_welt.addEllipse(x - DRAW_PARTICLE_RADIUS, y - DRAW_PARTICLE_RADIUS, DRAW_PARTICLE_RADIUS * 2,
                                       DRAW_PARTICLE_RADIUS * 2, pen, brush)
        else:
            pen_risk = QPen(COLOR_DARK_RED)
            pen_risk.setWidth(2)
            self.scene_welt.addEllipse(x - DRAW_PARTICLE_RADIUS, y - DRAW_PARTICLE_RADIUS,
                                       DRAW_PARTICLE_RADIUS * 2, DRAW_PARTICLE_RADIUS * 2, pen_risk, brush)

    def draw_quarantine(self, x: float, y: float) -> None:
        """Draws the quarantine rect if the particle is in quarantine

        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle

        """
        self.scene_welt.addRect(x - DRAW_QUARANTINE_PARTICLE_WIDTH / 2,
                                y - DRAW_QUARANTINE_PARTICLE_WIDTH / 2,
                                DRAW_QUARANTINE_PARTICLE_WIDTH, DRAW_QUARANTINE_PARTICLE_WIDTH,
                                QPen(COLOR_BLACK), QBrush(Qt.gray))

    def draw_humans(self, x: float, y: float, pixmap: QPixmap) -> None:
        """Draws humans instead of particles
        
        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle
        pixmap: QPixmap
            image of the human

       """
        pixmap_world = self.scene_welt.addPixmap(pixmap)
        pixmap_world.setX(x - HUMAN_PIXMAP_SIZE / 2)
        pixmap_world.setY(y - HUMAN_PIXMAP_SIZE / 2)

    def draw_infection_radius(self, x: float, y: float, infection_radius: float) -> None:
        """Draws the infection radius of the particle if the circle is in the world

        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle
        infection_radius: float
            infection radius

        """
        if self.check_circle_in_world(x, y, infection_radius):
            pen = QPen(COLOR_RED)
            self.scene_welt.addEllipse(x - infection_radius, y - infection_radius, infection_radius * 2,
                                       infection_radius * 2,
                                       pen, QBrush())

    def draw_social_distance(self, x: float, y: float, social_distance: float) -> None:
        """Draws the social distance of the particle if the circle is in the world

        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle
        social_distance: float
            social distance

        """
        if self.check_circle_in_world(x, y, social_distance):
            pen = QPen(COLOR_GRAY)
            self.scene_welt.addEllipse(x - social_distance, y - social_distance, social_distance * 2,
                                       social_distance * 2,
                                       pen, QBrush())

    def check_circle_in_world(self, x: float, y: float, radius: float) -> bool:
        """Checks if the circle is in the world

        Parameters
        ----------
        x: float
            x position of the particle
        y: float
            y position of the particle
        radius: float
            radius of the circle

        Returns
        -------
        bool:
            is the radius in the world?
        """
        return (self.size_world['width'] / 2 - radius - 1) > x > -(self.size_world['width'] / 2 - radius - 1) \
               and (self.size_world['height'] / 2 - radius - 1) > y > -(self.size_world['height'] / 2 - radius - 1)

    def draw_home(self, x: float, y: float) -> None:
        """Draws the home of the particle

        Parameters
        ----------
        x: float
            x position of the particle's home
        y: float
            y position of the particle's home

        """
        pixmap = self.scene_welt.addPixmap(QPixmap('resources/images/house.png'))
        pixmap.setX(x - 7.5)
        pixmap.setY(y - 7.5)

    def create_simulation(self) -> dict:
        """Prepares everything for the creation of the simulation and returns the values of the parameter inputs.

        Returns
        -------
        dict:
            values of the inputs
        """
        self.window_resized(0, 0, self.view_welt.size().width(), self.view_welt.size().height())
        self.dis_enable_inputs(True)
        self.dis_enable_preset_selection(True)
        self.create_plot()
        self.button_reset.setEnabled(True)
        return self.get_simulation_parameter()

    def get_simulation_parameter(self) -> dict:
        """Returns the values of the parameter inputs.

        Returns
        -------
        dict:
            values of the parameter inputs
        """
        return {'humans': self.get_number_of_particles(), 'infected': self.get_infected(),
                'simulation_speed': self.get_simulation_speed(),
                'movement_speed': self.get_movement_speed(),
                'infection_rate': self.get_infection_rate(), 'infection_radius': self.get_infektion_radius(),
                'death_rate': self.get_death_rate(), 'incubation_time': self.get_incubation_time(),
                'average_death_time': self.get_average_death_time(),
                'average_recover_time': self.get_average_recovery_time(),
                'reinfection_after_recovery': self.get_reinfection(), 'reinfection_rate': self.get_reinfection_rate(),
                'social_distancing': self.get_social_distancing(),
                'social_distancing_distance': self.get_social_distance(), 'lockdown': self.get_lockdown(),
                'lockdown_state': self.get_lockdown_state(),
                'quarantine': self.get_quarantine(), 'quarantine_breakout': self.get_quarantine_breakout_rate(),
                'extended_view': self.get_extended_view(), 'show_infection_radius': self.get_show_infection_radius(),
                'show_home': self.get_show_home(), 'risk_group': self.get_risk_group(),
                'risk_group_age': self.get_risk_group_age(), 'risk_group_death_rate': self.get_risk_group_death_rate(),
                'show_humans': self.get_show_humans(), 'preset': self.current_preset['id'],
                'show_social_distance': self.get_show_social_distance(), 'all_collision': self.get_collision_all()
                }

    def get_export_parameter(self) -> dict:
        """Returns the values of the export inputs.

        Returns
        -------
        dict:
            values of the export inputs
        """
        return {'csv': self.get_export_data(),
                'granularity': self.get_export_granularity(),
                'include_parameters': self.get_export_include_parameters(),
                'plot': self.get_export_plot(),
                'plot_image': pg.exporters.ImageExporter(self.widget_plot.plotItem)
                }

    def show_warning(self, text: str, color: str, ms: int) -> None:
        """Creates, shows and animates the warning.

        Parameters
        ----------
        text: str
            text of the warning
        color: str
            color of the warning
        ms: int
            displayed time in ms

        Returns
        -------

        """
        # Add Text and Icon to the error bar.
        if self.warning_is_currently_shown:
            self.hide_warning()

        self.error_message.setText(text)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('resources/images/icon_close.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_error.setIcon(icon)

        # Set color of the error bar.
        if color == "red":
            self.errorBar.setStyleSheet(
                "QWidget"
                "{"
                "background : #FF331D;"
                "border-radius: 7px"
                "}"
            )
        if color == "green":
            self.errorBar.setStyleSheet(
                "QWidget"
                "{"
                "background : #7AC485;"
                "border-radius: 7px"
                "}"
            )
        if color == "blue":
            self.errorBar.setStyleSheet(
                "QWidget"
                "{"
                "background : #70B9DB;"
                "border-radius: 7px"
                "}"
            )
        # Shows the error bar, corrects the position of the main layout and creates an animation which which lets the
        # error bar fly in
        self.errorBar.show()
        self.anim_error_bar.setStartValue(QPoint(self.errorBar.x(), -30))
        self.anim_error_bar.setEndValue(QPoint(self.errorBar.x(), 5))
        self.anim_error_bar.setDuration(1000)
        self.anim_error_bar.start()

        self.timer_hide_error_bar.start(ms)
        self.warning_is_currently_shown = True
        self.verticalLayout.setGeometry(QRect(12, 12, self.width() - 24, self.height() - 24))

    def hide_warning(self) -> None:
        """hides the warning"""
        self.errorBar.hide()
        self.timer_hide_error_bar.stop()
        self.warning_is_currently_shown = False

    def switch_parameter_widget(self) -> None:
        """Switches the parameter and export widget"""
        if self.stackedWidget_parameter.currentIndex() == 0:
            self.stackedWidget_parameter.setCurrentIndex(1)
        else:
            self.stackedWidget_parameter.setCurrentIndex(0)

    def switch_diagrams(self) -> None:
        """Switches the pi and plot chart"""
        if self.stackedWidget_diagrams.currentIndex() == 0:
            self.stackedWidget_diagrams.setCurrentIndex(1)
            self.button_plot.setDisabled(True)
            self.button_pi_chart.setDisabled(False)
        else:
            self.stackedWidget_diagrams.setCurrentIndex(0)
            self.button_pi_chart.setDisabled(True)
            self.button_plot.setDisabled(False)

    def preset_changed(self, index: int) -> None:
        """Changes the preset.

        Parameters
        ----------
        index: int
            index of the new preset

        """
        self.current_preset['id'] = index
        if index > 0:
            if index != 4:
                self.current_preset['name_de'] = PRESETS[index][0]
                self.current_preset['name_en'] = PRESETS[index][1]
                self.current_preset['data'] = PRESETS[index][2]
            else:
                self.current_preset['name_de'] = self.todays_preset['name_en']
                self.current_preset['name_en'] = self.todays_preset['name_en']
                self.current_preset['data'] = self.todays_preset['data']
            self.set_inputs_for_preset(index)
            self.msg_preset_changed()
        else:
            self.current_preset['name_de'] = 'Benutzerdefiniert'
            self.current_preset['name_en'] = 'Custom'
            self.current_preset['data'] = {}
            self.lcd_verstorben.display("0")
            self.lcd_genesen.display("0")
            self.lcd_infiziert.display("0")
            self.lcd_infektioes.display("0")
            self.lcd_gesund.display("0")
            self.dis_enable_inputs(False)

    def set_inputs_for_preset(self, index: int) -> None:
        """Sets the inputs for the current preset

        Parameters
        ----------
        index: int
            index of the new preset

        Returns
        -------

        """
        if index != 4:
            self.eingabe_menschen.setText(str(self.current_preset['data']['humans']))
            self.eingabe_infiziert.setText(str(self.current_preset['data']['infected']))
            self.slider_bewegungsgeschw.setSliderPosition(self.current_preset['data']['movement_speed'])
            self.check_collision.setChecked(self.current_preset['data']['all_collision'])
            self.eingabe_infektionswahr.setText(str(self.current_preset['data']['infection_rate']))
            self.slider_infection_radius.setSliderPosition(self.current_preset['data']['infection_radius'])
            self.eingabe_sterberate.setText(str(self.current_preset['data']['death_rate']))
            self.check_risk_group.setChecked(self.current_preset['data']['risk_group'])
            if self.current_preset['data']['risk_group']:
                self.range_risk_group_age.setLowerValue(self.current_preset['data']['risk_group_age']['min'])
                self.range_risk_group_age.setUpperValue(self.current_preset['data']['risk_group_age']['max'])
                self.eingabe_risk_group_death_rate.setText(str(self.current_preset['data']['risk_group_death_rate']))
            self.eingabe_incubation_time.setText(str(self.current_preset['data']['incubation_time']))
            self.eingabe_sterbezeitpunkt.setText(str(self.current_preset['data']['average_death_time']))
            self.eingabe_genesungszeitpunkt.setText(str(self.current_preset['data']['average_recover_time']))
            self.check_reinfection.setChecked(self.current_preset['data']['reinfection_after_recovery'])
            if self.current_preset['data']['reinfection_after_recovery']:
                self.eingabe_wiederanstreckungsrate.setText(str(self.current_preset['data']['reinfection_rate']))
            self.check_social_distancing.setChecked(self.current_preset['data']['social_distancing'])
            if self.current_preset['data']['social_distancing']:
                self.slider_social_distancing.setSliderPosition(
                    self.current_preset['data']['social_distancing_distance'])
            self.check_lockdown.setChecked(self.current_preset['data']['lockdown'])
            if self.current_preset['data']['lockdown']:
                self.slider_lockdown.setSliderPosition(self.current_preset['data']['lockdown_state'])
            self.check_quarantaene.setChecked(self.current_preset['data']['quarantine'])
            if self.current_preset['data']['quarantine']:
                self.eingabe_quarantaeneausbrecher.setText(str(self.current_preset['data']['quarantine_breakout']))
            self.dis_enable_inputs(True)
        else:
            self.eingabe_menschen.setText(str(self.current_preset['data']['humans']))
            self.eingabe_infiziert.setText(str(self.current_preset['data']['infected']))
            self.disable_inputs_for_todays_preset()

        self.lcd_verstorben.display(str(self.current_preset['data']['deceased']))
        self.lcd_genesen.display(str(self.current_preset['data']['immune']))
        self.lcd_infiziert.display(str(self.current_preset['data']['infected']))
        self.lcd_infektioes.display(str(self.current_preset['data']['infectious']))
        self.lcd_gesund.display(
            str(self.current_preset['data']['humans'] - self.current_preset['data']['infectious'] -
                self.current_preset['data']['immune'] - self.current_preset['data']['deceased'] -
                self.current_preset['data']['infected']))

    def create_pi_chart(self, data: dict) -> None:
        """Creates the pi chart

        Parameters
        ----------
        data: dict
            data for the pi chart

        """
        try:
            from PyQt5.QtChart import QChart, QPieSeries
            imported = True
        except ImportError:
            imported = False
        if imported:
            self.scene_pi_chart.clear()
            series = QPieSeries()
            series.append("healthy", data['healthy'][-1])
            series.append("immune", data['immune'][-1])
            series.append("infected", data['infected'][-1])
            series.append("infectious", data['infectious'][-1])
            series.append("deceased", data['deceased'][-1])

            for i in range(4):
                piece = series.slices()[i]
                color = get_color_for_chart_piece(i)
                piece.setPen(color[0])
                piece.setBrush(color[1])

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setBackgroundVisible(False)

            chart.setPreferredSize(self.size_diagram['width'], self.size_diagram['height'])
            self.scene_pi_chart.addItem(chart)

    def create_plot(self) -> None:
        """Creates the plot."""
        self.plot_healthy = self.widget_plot.plot(pen=COLOR_GRAY, fillLevel=0, fillBrush=COLOR_GRAY)
        self.plot_immune = self.widget_plot.plot(pen=COLOR_GREEN, fillLevel=0, fillBrush=COLOR_GREEN)
        self.plot_infected = self.widget_plot.plot(pen=COLOR_YELLOW, fillLevel=0, fillBrush=COLOR_YELLOW)
        self.plot_infectious = self.widget_plot.plot(pen=COLOR_RED, fillLevel=0, fillBrush=COLOR_RED)
        self.plot_deceased = self.widget_plot.plot(pen=COLOR_BLACK, fillLevel=0, fillBrush=COLOR_BLACK)
        # self.widget_plot.setLabel('left', 'Number of people')
        self.widget_plot.setLabel('bottom', 'Time', units='days')
        self.widget_plot.setYRange(0, int(self.get_number_of_particles()))
        self.widget_plot.setXRange(0, 5)
        self.widget_plot.enableAutoRange(pg.ViewBox.XAxis, 1.0)

    def update_plot(self, data: dict) -> None:
        """Updates the plot

        Parameters
        ----------
        data: dict
            new data

        """
        self.plot_healthy.setData(y=list(
            map(lambda a, b, c, d, e: a + b + c + d + e, data['healthy'], data['immune'], data['infected'],
                data['infectious'], data['deceased'])), x=data['days'])
        self.plot_immune.setData(y=list(
            map(lambda b, c, d, e: b + c + d + e, data['immune'], data['infected'], data['infectious'],
                data['deceased'])), x=data['days'])
        self.plot_infected.setData(
            y=list(map(lambda c, d, e: c + d + e, data['infected'], data['infectious'], data['deceased'])),
            x=data['days'])
        self.plot_infectious.setData(y=list(map(lambda d, e: d + e, data['infectious'], data['deceased'])),
                                     x=data['days'])
        self.plot_deceased.setData(y=data['deceased'], x=data['days'])

    def range_risk_group_age_changed(self, min_age: int, max_age: int) -> None:
        """Displays an information when the range of the risk group changed.

        Parameters
        ----------
        min_age: int
            min age
        max_age: int
            max age

        """
        if self.current_preset['id'] == 0:
            self.show_warning(QtWidgets.QApplication.instance().translate('Message risk group changed',
                                                                          "Age of the risk group: %d - %d.")
                              % min_age % max_age,
                              "blue", 5000)

    def movement_speed_changed(self, speed: int) -> None:
        """Displays an information when the movement speed changed.

        Parameters
        ----------
        speed: int
            movement speed
        """
        if self.current_preset['id'] == 0:
            text = QtWidgets.QApplication.instance().translate('value movement speed fast', "fast")
            if speed == 1:
                text = QtWidgets.QApplication.instance().translate('value movement speed slow', "slow")
            elif speed == 2:
                text = QtWidgets.QApplication.instance().translate('value movement speed middle', "middle")
            self.show_warning(QtWidgets.QApplication.instance().translate('Message movement speed changed',
                                                                          "Movement speed changed to %s.") % text,
                              "blue", 5000)

    def infection_radius_changed(self, radius: int) -> None:
        """Displays an information when the infection radius changed.

        Parameters
        ----------
        radius: int
            infection radius
        """
        if self.current_preset['id'] == 0:
            self.show_warning(QtWidgets.QApplication.instance().translate('Message infection radius changed',
                                                                          "Infection radius changed to %d.") % radius,
                              "blue", 5000)

    def social_distancing_distance_changed(self, distance: int) -> None:
        """Displays an information when the social distance changed.

        Parameters
        ----------
        distance: int
            social distance
        """
        if self.current_preset['id'] == 0:
            text = QtWidgets.QApplication.instance().translate('value social distance very large', "very large")
            if distance == 1:
                text = QtWidgets.QApplication.instance().translate('value social distance very small', "very small")
            elif distance == 2:
                text = QtWidgets.QApplication.instance().translate('value social distance small', "small")
            elif distance == 3:
                text = QtWidgets.QApplication.instance().translate('value social distance middle', "middle")
            elif distance == 4:
                text = QtWidgets.QApplication.instance().translate('value social distance large', "large")
            self.show_warning(QtWidgets.QApplication.instance().translate('Message social distance changed',
                                                                          "Social distance changed to %s.") % text,
                              "blue", 5000)

    def lockdown_state_changed(self, state: int) -> None:
        """Displays an information when the lockdown state changed.

        Parameters
        ----------
        state: int
            lockdown state
        """
        if self.current_preset['id'] == 0:
            text = QtWidgets.QApplication.instance().translate('value lockdown very strict', "very strict")
            if state == 1:
                text = QtWidgets.QApplication.instance().translate('value lockdown relaxed', "relaxed")
            elif state == 2:
                text = QtWidgets.QApplication.instance().translate('value lockdown middle', "middle")
            elif state == 3:
                text = QtWidgets.QApplication.instance().translate('value lockdown strict', "strict")
            self.show_warning(QtWidgets.QApplication.instance().translate('Message lockdown state changed',
                                                                          "Lockdown state changed to %s.") % text,
                              "blue", 5000)

    def simulation_speed_changed(self, speed: int) -> None:
        """Displays an information when the simulation speed changed.

        Parameters
        ----------
        speed: int
            simulation speed
        """
        self.simulation_speed_changed_signal.emit(speed)
        self.show_warning(QtWidgets.QApplication.instance().translate('Message simulation speed changed',
                                                                      "Simulation speed changed to %d.") % speed,
                          "blue", 5000)

    def msg_preset_changed(self) -> None:
        """Displays an information when the preset changed."""
        if self.lang == "de":
            self.show_warning(QtWidgets.QApplication.instance().translate('Message preset changed',
                                                                          "Preset changed to %s.")
                              % self.current_preset['name_de'],
                              "blue", 5000)
        else:
            self.show_warning(QtWidgets.QApplication.instance().translate('Message preset changed',
                                                                          "Preset changed to %s.")
                              % self.current_preset['name_en'],
                              "blue", 5000)

    def init_today_preset(self) -> None:
        """Sets the today's preset."""
        data = get_data_for_today_preset()
        self.todays_preset['name_de'] = "COVID-19, DE, " + data['last_update']
        self.todays_preset['name_en'] = "COVID-19, GER, " + data['last_update']
        self.todays_preset['data'] = {
            'humans': 100,
            'infectious': data['infectious'],
            'immune': data['immune'],
            'deceased': data['deceased'],
            'infected': 0
        }
        self.init_presets(self.lang)

    def init_presets(self, lang: str) -> None:
        """Inits the presets.

        Parameters
        ----------
        lang: str
            language
        """
        self.comboBox_preset.clear()
        if lang == "de":
            self.comboBox_preset.addItems(
                [PRESET_0_DE, PRESET_1_NAME_DE, PRESET_2_NAME_DE, PRESET_3_NAME_DE, self.todays_preset['name_de'],
                 PRESET_4_NAME_DE,
                 PRESET_5_NAME_DE, PRESET_6_NAME_DE])
        else:
            self.comboBox_preset.addItems(
                [PRESET_0_EN, PRESET_1_NAME_EN, PRESET_2_NAME_EN, PRESET_3_NAME_EN, self.todays_preset['name_en'],
                 PRESET_4_NAME_EN,
                 PRESET_5_NAME_EN, PRESET_6_NAME_EN])

        # Corrects the width of the popup that the text is fully displayed
        self.comboBox_preset.setStyleSheet('''*    
        QComboBox QAbstractItemView 
            {
            min-width: 270px;
            }
        ''')

    def check_pi_chart_module(self):
        """Checks if pyqtchart is installed."""
        try:
            from PyQt5.QtChart import QChart, QPieSeries
        except ImportError:
            self.show_warning(QtWidgets.QApplication.instance().translate('Message import pyqtchart',
                                                                          "Line diagram cannot be displayed because "
                                                                          "the module 'pyqtchart' is not installed."),
                              "red", 5000)
