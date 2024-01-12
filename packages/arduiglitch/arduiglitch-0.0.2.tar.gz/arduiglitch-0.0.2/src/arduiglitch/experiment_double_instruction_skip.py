from experiment import Experiment
from logger import Log
import numpy as np
import pandas as pd
import hvplot.pandas
import datetime
# Module to create buttons making experiment manipulation easier
import panel as pn
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

class ExperimentDoubleInstructionSkip(Experiment):
    """
    Experiment child class that handles the duplicate register instruction skip experiment.
    """
    def __init__(self, log: Log):
        super().__init__(log)
        # Initialization values, should be set before starting an experiment
        self.min_delay1 = 0
        self.max_delay1 = 1
        self.step_delay1 = 1

    def set_delays(self, min_delay, max_delay, step_delay, min_delay1, max_delay1, step_delay1):
        """
        Overrides the method defined in the inherited class to handle more params.
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.step_delay = step_delay
        self.min_delay1 = min_delay1
        self.max_delay1 = max_delay1
        self.step_delay1 = step_delay1
        # boolean to make sure params were set at least once before allowing experiment start
        self.params_initialized = True

    def build_gui_panel(self):
        errors_plot = hvplot.bind(lambda _: self.data, self.static_text).interactive().hvplot.heatmap(
            x="Delay first glitch",
            y="Delay second glitch",
            C="errors",
            title="Successful errors depending on the delays",
            rot=45,
            xaxis="top",
            width=600,
            height=400,
            #toolbar=None,
            fontsize={"title": 10, "xticks": 8, "yticks": 8}
        ).opts(default_tools = ["save"])

        crashes_plot = hvplot.bind(lambda _: self.data, self.static_text).interactive().hvplot.heatmap(
            x="Delay first glitch",
            y="Delay second glitch",
            C="Crash",
            title="Target com crashes depending on the delays",
            rot=45,
            xaxis="top",
            width=600,
            height=400,
            #toolbar=None,
            fontsize={"title": 10, "xticks": 8, "yticks": 8}
        ).opts(default_tools = ["save"])

        (button_start, button_stop, button_resume) = self.create_start_stop_resume_buttons()

        first_app = pn.Column(pn.Row(button_start, button_stop, button_resume), pn.Row(errors_plot, crashes_plot), self.alert_log)
        return pn.panel (first_app, loading_indicator=True, width=2000)

    def generate_empty_dataframe(self):
        """
        Uses the min/max/step_delay attributes to generate an empty dataframe with the correct X axis values.
        """
        delays0 = np.arange(self.min_delay, self.max_delay, self.step_delay)
        delays1 = np.arange(self.min_delay1, self.max_delay1, self.step_delay1)

        errors = np.zeros((len(delays0) * len(delays1)))
        bad_responses = np.zeros((len(delays0) * len(delays1)))

        index = pd.MultiIndex.from_product([list(delays0), list(delays1)], names=["Delay first glitch", "Delay second glitch"])
        return pd.DataFrame({
            "errors": list(errors),
            "Crash": list(bad_responses)
        }, index=index)

    def update_gui(self, delay0: int, delay1: int, error_type: str = "Crash"):
        self.data.at[(delay0, delay1), error_type] += 1
        self.static_text.value = f"last update: {datetime.datetime.now()}"
        # Update data
        self.data.to_csv(path_or_buf = self.csv_filepath)
