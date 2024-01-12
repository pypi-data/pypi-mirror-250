# Part of voltage glitch Arduino fault injection formation
# Original author: Hugo PERRIN (h.perrin@emse.fr).
# License: check the LICENSE file.
"""
Base Experiment class that handles plotting and controlling the glitcher and target Arduinos.
Do not instanciate/use. Instanciate specific child classes.
"""

########################################################################################################################
#################################################### IMPORTS ###########################################################

from abc import ABC, abstractmethod
from queue import Queue
import datetime
from pathlib import Path
from typing import Callable, Any
from logger import Log
import logging
from parallel_thread import ParallelThread
# Modules to display things in jupyterlab notebook
from IPython.display import display
# Module to create buttons making experiment manipulation easier
import panel as pn
import pandas as pd
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# ##############################################################################################
# ##############################################################################################
# ##############################################################################################

class Experiment(ABC):
    """
    Base Experiment class that handles plotting and controlling the glitcher and target Arduinos.
    Do not instanciate/use. Instanciate specific child classes.
    """
    def __init__(self, log: Log):
        self.log = log

        # Initialization values, should be set before starting an experiment
        self.min_delay  = 0
        self.max_delay  = 1
        self.step_delay = 1
        self.params_initialized = False

        self.static_text = pn.widgets.StaticText()
        self.data: pd.DataFrame = pd.DataFrame({})

        # Parallel processes for the experiment function
        self.glitch_process = None

        # Main panel is only build when GUI is started/restarted
        self.panel = None

        # Definition of the widget in which messages can be printed (to replace the logger output).
        # A placeholder is created and popped for the purpose of creating an empty log during start-up.
        self.alert_log = pn.Column(pn.pane.Alert("placeholder"))
        self.alert_log.scroll = True # type: ignore
        #self.alert_log.scroll_button_threshold = 200
        self.alert_log.pop(0)

        self.csv_filepath = str(Path(__file__).absolute().parent) + "/../csv/" + self.__class__.__name__ + ".csv"

    @abstractmethod
    def build_gui_panel(self):
        """
        Method that builds and returns the panel that contains an interactive plot. Child classes need to implement it.
        """
        pass

    def load_and_display_gui(self):
        """
        Method that builds and displays the panel in the Jupyterlab Notebook.
        """
        try:
            # Try to resume from last saved data (in csv file)
            self.data = pd.read_csv(self.csv_filepath)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If no csv file was found or if it was empty, generate an empty dataframe
            self.data = self.generate_empty_dataframe()
            self.data.to_csv(path_or_buf = self.csv_filepath)

        # Generate panel with current dataframe
        self.panel = self.build_gui_panel()

        # Display panel in Notebook
        display(self.panel)

    @abstractmethod
    def update_gui(self, *args):
        """
        Method used to push data to plot to a queue shared with the graph plot process.
        Child classes need to implement it.
        """
        pass

    def clear_graph(self):
        """
        Method should clear the graph and update it's size depending on min/max/step_delays.
        Child classes need to implement it.
        """
        self.data = self.generate_empty_dataframe()
        self.static_text.value = f"last update: {datetime.datetime.now()}"

    def log_alert(self, md_msg: str, alert_type: str = "info"):
        """
        Appends an alert in the corresponding section of the GUI.

        Args:
            - md_msg: (str) Markdown-formatted message to render in alert.
            - alert_type: (str) See Holoviz Panel lib panel.pane.Alert for reference of possible values.
        """
        self.alert_log.height = 300
        self.alert_log.styles = {"border-radius": "15px", "padding": "10px", "border": "0.1em solid black"}
        self.alert_log.insert(0, pn.pane.Alert("*" + str(datetime.datetime.now()) + "* - " + md_msg, alert_type=alert_type))

    def set_experiment_function(self, exp_fn: Callable[[Log, Queue, Any], None], params: list[Any] | None = None):
        if params is not None:
            self.glitch_process = ParallelThread(self.log, exp_fn, *[self, *params])
        else:
            self.glitch_process = ParallelThread(self.log, exp_fn, self)

    def start_gui(self):
        """
        Initializes and displays GUI.
        """
        if self.params_initialized:
            # To prevent panel from showing unnecessary information (because self.log is setup for DEBUG level)
            # (TODO: dirty solution, find alternative; without self.log ?)
            logging.basicConfig()
            logging.getLogger().setLevel(logging.INFO)

            self.load_and_display_gui()

    @abstractmethod
    def generate_empty_dataframe(self) -> pd.DataFrame:
        """
        Uses the min/max/step_delay attributes to generate an empty dataframe with the correct X axis values.
        """
        pass

    def start_exp(self):
        if self.params_initialized and (self.glitch_process is not None):
            self.glitch_process.start()
        else:
            self.log.critical("Attempted to start experiment without having set parameters with `self.set_delays()` or an experiment fn with `self.set_experiment_function()`. Ignoring.")

    def stop_exp(self):
        if self.glitch_process is None:
            self.log.critical("Attempted to stop experiment without having set an experiment fn with `self.set_experiment_function()`. Ignoring.")
        else:
            self.glitch_process.stop()

    def set_delays(self, min_delay, max_delay, step_delay):
        """
        Set the minimum, maximum, and step delays for the experiment.
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.step_delay = step_delay
        # boolean to make sure params were set at least once before allowing experiment start
        self.params_initialized = True

    # The next 3 functions are used to handle on_click event of basic start, stop and resume buttons
    def button_start_run(self, _):
        self.clear_graph()
        self.log_alert("**Starting/Restarting experiment.**", alert_type="info")
        self.start_exp()

    def button_stop_run(self, _):
        self.log_alert("**Stopping experiment.**", alert_type="info")
        self.stop_exp()

    def button_resume_run(self, _):
        self.log_alert("**Resume experiment.**", alert_type="info")
        self.start_exp()

    def create_start_stop_resume_buttons(self):
        """
        Misc function to generate typical start, stop and resume buttons.

        Returns:
            - tuple of 3 pn.Button
        """
        button_start = pn.widgets.Button(name="Start/Restart experiment", button_type="primary", icon="caret-right", icon_size="1.5em")
        button_stop = pn.widgets.Button(name="Stop experiment", button_type="primary", icon="player-stop-filled", icon_size="1.5em")
        button_resume = pn.widgets.Button(name="Resume experiment", button_type="primary", icon="arrow-forward-up", icon_size="1.5em")

        button_start.on_click(self.button_start_run)
        button_stop.on_click(self.button_stop_run)
        button_resume.on_click(self.button_resume_run)

        return (button_start, button_stop, button_resume)


# ##############################################################################################
# ##############################################################################################
# ##############################################################################################

def should_stop_thread(control_queue: Queue) -> bool:
    if not control_queue.empty():
        return control_queue.get() == "stop"
    return False
