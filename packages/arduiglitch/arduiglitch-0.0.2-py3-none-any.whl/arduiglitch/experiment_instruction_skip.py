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

class ExperimentInstructionSkip(Experiment):
    """
    Experiment child class that handles the instruction skip experiment.
    """
    def __init__(self, log: Log):
        super().__init__(log)
        # Reference of was the registers look like after asm code was loaded
        # if no fault was caused.
        self.GOLD_REG = [0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30]

    def send_fault_to_gui(self, delay_i, res_str: str):
        try:
            res = res_str.split(' ')
            for i in range(len(res)):
                if res[i] == "0x55":
                    self.update_gui(delay_i, "reg" + str(i))
                    self.log_alert(f"Detected a correct error : {res} => reg{i}", "info")
        except Exception:
            self.update_gui(delay_i, "Crash")

    def build_gui_panel(self):
        total_plot = hvplot.bind(lambda _: self.data, self.static_text).interactive().hvplot.bar(
            x="X",
            y=["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6", "reg7", "reg8", "reg9", "Crash"],
            stacked=True,
            cmap=["red", "blue", "green", "yellow", "purple", "cyan", "orange", "pink", "grey", "brown", "olive"],
            rot=45,
            width=1200,
            height=400,
            title="Stacked errors"
        )

        unique_plots = []
        for i in range(10):
            unique_plots.append((f"reg[{i}]", hvplot.bind(lambda _: self.data, self.static_text).interactive().hvplot.bar(
                x="X",
                y="reg" + str(i),
                color=["red", "blue", "green", "yellow", "purple", "cyan", "orange", "pink", "grey", "brown"][i],
                rot=45,
                width=1200,
                height=400,
                title=f"Errors on reg[{i}]"
            )))

        plot_tabs = pn.Tabs(("Stacked errors", total_plot), *unique_plots)

        (button_start, button_stop, button_resume) = self.create_start_stop_resume_buttons()

        first_app = pn.Column(pn.Row(button_start, button_stop, button_resume), plot_tabs, self.alert_log)
        return pn.panel (first_app, loading_indicator=True, width=2000)

    def generate_empty_dataframe(self):
        """
        Uses the min/max/step_delay attributes to generate an empty dataframe with the correct X axis values.
        """
        X = np.arange(self.min_delay, self.max_delay, self.step_delay)
        Y = np.zeros((X.shape[0]))

        return pd.DataFrame({
            "X": list(X),
            "reg0": list(Y),
            "reg1": list(Y),
            "reg2": list(Y),
            "reg3": list(Y),
            "reg4": list(Y),
            "reg5": list(Y),
            "reg6": list(Y),
            "reg7": list(Y),
            "reg8": list(Y),
            "reg9": list(Y),
            "Crash": list(Y),
        })

    def update_gui(self, delay_i: int, error_type: str = "Crash"):
        self.data.at[delay_i, error_type] += 1
        self.static_text.value = f"last update: {datetime.datetime.now()}"
        # Update data
        self.data.to_csv(path_or_buf = self.csv_filepath)
