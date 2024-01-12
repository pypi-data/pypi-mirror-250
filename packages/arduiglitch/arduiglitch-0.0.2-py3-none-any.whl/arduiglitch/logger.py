# Part of EM induced Arduino fault injection formation
# Original author: Hugo PERRIN (h.perrin@emse.fr).
# License: check the LICENSE file.
"""
Contains a function that handles configuring the main Logger. The actual configuration is
contained in the associated yaml file. The goal is to enable easy switch between a PyLabSAS version
or without with minimal change in the actual scripts.
"""

import logging
import logging.config
import yaml

class Log:
    def __init__(self, log_config_file_name: str):
        self.log_config_file_name = log_config_file_name
        try:
            # Create logger instances and configure it
            with open(log_config_file_name, mode="r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
            self._f = logging.getLogger(__name__)
        except Exception as err:
            print(f"Logger init error : {err}")
            exit(-1)

    def info(self, data : str):
        self._f.info(data)

    def critical(self, data : str):
        self._f.critical(data)

    def debug(self, data : str):
        self._f.debug(data)

    def error(self, data: str):
        self._f.error(data)

    def write_header(
        self,
        x_min, x_max,
        y_min, y_max,
        xy_step,
        pulse_delay_min,
        pulse_delay_max,
        pulse_delay_step,
        pulse_width_min,
        pulse_width_max,
        pulse_width_step,
        pulse_amp_min,
        pulse_amp_max,
        pulse_amp_step,
    ):
        """
        Write the correct header at the very start of the log file to enable the Rust log viewer
        app to create the graphs correctly.
        """
        # TODO: log file name should be defined only in one place: right now here and in log config yaml file.
        with open("data.log", mode="w+", encoding="utf-8") as f:
            f.write(f"{x_min},{x_max},{y_min},{y_max},{xy_step},(XYZ [x_min;x_max;y_min;y_max;xy_step])\n")
            f.write(f"{pulse_delay_min},{pulse_delay_max},{pulse_delay_step},(Pulse delay [min;max;step])\n")
            f.write(f"{pulse_width_min},{pulse_width_max},{pulse_width_step},(Pulse width [min;max;step])\n")
            f.write(f"{pulse_amp_min},{pulse_amp_max},{pulse_amp_step},(Amp [min;max;step])\n")
            f.write("# | Time | Log type | x | y | z | pulse delay | pulse width | pulse amp | error number\n")
