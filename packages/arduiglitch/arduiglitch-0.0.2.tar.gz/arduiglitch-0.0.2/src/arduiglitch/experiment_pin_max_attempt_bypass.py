from experiment import Experiment
from arduino_formation_faults import ArduinoFormationFaults
from arduino_com_result import Ok, Err
import numpy as np
import pandas as pd
import hvplot.pandas
import datetime
# Module to create buttons making experiment manipulation easier
import panel as pn
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

class ExperimentPINMaxAttemptBypass(Experiment):
    """
    Experiment child class that handles the PIN log-in max attempt protection skip experiment.
    """
    def log_with_pin(self, target: ArduinoFormationFaults, pin: int) -> bool:
        """
        This function ought to be used once g_ptc decrement was successfully
        faulted. It tries to authenticate with `pin`.
        """
        self.log_alert(f"Trying PIN {pin}", alert_type="info")
        match target.set_user_pin(pin):
            case Ok(None):
                match target.verifypin():
                    case Ok(True):
                        self.log_alert(f"**Success** - PIN found : {pin}", alert_type="success")
                        return True
                    case Err(err):
                        self.log_alert(f"{err}", alert_type="warning")
            case Err(err):
                self.log_alert(f"{err}", alert_type="warning")
        return False

    def build_gui_panel(self):
        total_plot = hvplot.bind(lambda _: self.data, self.static_text).interactive().hvplot.bar(
            x="X",
            y=["gptc > 0", "Crash"],
            stacked=True,
            cmap=["green", "orange"],
            rot=45,
            width=1200,
            height=400,
            title="Fault injection success and Arduino com crashes"
        )

        (button_start, button_stop, button_resume) = self.create_start_stop_resume_buttons()

        first_app = pn.Column(pn.Row(button_start, button_stop, button_resume), total_plot, self.alert_log)
        return pn.panel (first_app, loading_indicator=True, width=2000)

    def generate_empty_dataframe(self):
        """
        Uses the min/max/step_delay attributes to generate an empty dataframe with the correct X axis values.
        """
        X = np.arange(self.min_delay, self.max_delay, self.step_delay)
        Y = np.zeros((X.shape[0]))

        return pd.DataFrame({
            "X": list(X),
            "gptc > 0": list(Y),
            "Crash": list(Y),
        })

    def update_gui(self, delay_i: int, error_type: str = "Crash"):
        self.data.at[delay_i, error_type] += 1
        self.static_text.value = f"last update: {datetime.datetime.now()}"
        # Update data
        self.data.to_csv(path_or_buf = self.csv_filepath)
