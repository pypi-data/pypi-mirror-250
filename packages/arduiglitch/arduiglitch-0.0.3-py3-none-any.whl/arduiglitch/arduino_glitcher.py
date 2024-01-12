"""
Child class of ArduinoComBase that handles the communication
with the glitcher Arduino.
"""

# built-in modules
import time

# local dependencies
from .arduino_com_base import ArduinoComBase
from .logger import Log
from .arduino_com_result import Result, Ok, Err

class ArduinoGlitcher(ArduinoComBase):
    """
    Class that handles communication with the Arduino board which generates the
    glitch trigger and resets the target board.
    """

    def __init__(
        self,
        log : Log,
        port : str,
        baudrate: int = 9600,
        timeout_s: float = 0.5,
        cooldown_ms: int = 10,
        experiment = None
    ):
        """
        The class constructor.

        Args:
            - log: (Log) Log object to use for console logging.
            - port: (str) Com port to use :
                - Windows: "COMx"
                - Linux: "/dev/ttyACMx" or "/dev/ttyUSBx"
            - baudrate: (int) Baudrate to use, usually 9600 or 115200.
            - timeout_s: (float) Serial com timeout in seconds.
            - cooldown_ms: (int) Minimum elapsed time before a new glitch.
            - experiment: (Experiment) Experiment object to use for GUI logging.
        """
        super().__init__(log, port, baudrate, timeout_s, experiment)
        self.cooldown_ms = cooldown_ms
        time.sleep(2)
        self.set_glitch_cooldown(self.cooldown_ms)

    def set_led_on(self) -> Result[None]:
        self._safe_instrument_reset_input_buffer()
        match self._safe_write_then_readline("H"):
            case Ok("OK\n"):
                return Ok(None)
            case Ok(_):
                return Err(Exception("Unexpected response from Arduino."))
            case err:
                return err

    def set_led_off(self) -> Result[None]:
        self._safe_instrument_reset_input_buffer()
        match self._safe_write_then_readline("L"):
            case Ok("OK\n"):
                return Ok(None)
            case Ok(_):
                return Err(Exception("Unexpected response from Arduino."))
            case err:
                return err

    def set_first_glitch_delay(self, delay: int) -> Result[int]:
        """
        See `set_nth_glitch_delay` method for documentation.
        """
        return self.set_nth_glitch_delay(delay, 0)

    def set_second_glitch_delay(self, delay: int) -> Result[int]:
        """
        See `set_nth_glitch_delay` method for documentation.
        """
        return self.set_nth_glitch_delay(delay, 1)


    def set_nth_glitch_delay(
        self,
        delay: int,
        glitch_index: int = 0
    ) -> Result[int]:
        """
        Sends the number of nop instructions that the glitcher should insert
        after firing the (N-1)th glitch and before doing the Nth glitch.

        Returns a Result object containing the delay that was actually set by
        the glitcher.

        Args:
            - delay: (int) number of nop instructions to append before glitch.
            - glitch_index: (int) glitch index to set the delay for (0 or 1).
        """

        # Should be a positive number
        delay = abs(delay)

        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                prefix = "D" if glitch_index == 0 else "d"
                match self._safe_write_then_readline(f"{prefix}{delay}\n"):
                    case Ok(answer):
                        answer_array = answer.rstrip().split(" ")
                        if len(answer_array) < 2:
                            return Err(Exception(
                                f"Unexpected response from Arduino: {answer}."
                            ))
                        else:
                            real_delay = answer_array[1]
                            try:
                                return Ok(int(real_delay))
                            except ValueError:
                                return Err(Exception(
                                    f"Could not parse the delay value returned by the Arduino: {real_delay}."
                                ))
                    case err:
                        return err
            case err:
                return err

    def set_glitch_cooldown(self, cooldown_ms: int) -> Result[int]:
        """
        Sends the cooldown in milliseconds that prevent the glitch to trigger
        again.

        Args:
            - cooldown_ms: (int) Minimum elapsed time before a new glitch.
        """

        # Should be a positive number
        cooldown_ms = abs(cooldown_ms)

        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline(f"T{cooldown_ms}\n"):
                    case Ok(answer):
                        answer_array = answer.rstrip().split(" ")
                        if len(answer_array) < 2:
                            return Err(Exception(
                                f"Unexpected response from Arduino: {answer}."
                            ))
                        else:
                            real_cooldown_ms = answer_array[1]
                            try:
                                return Ok(int(real_cooldown_ms))
                            except ValueError:
                                return Err(Exception(
                                    f"Could not parse the cooldown value returned: {real_cooldown_ms}."
                                ))
                    case err:
                        return err
            case err:
                return err

    def reset_target(self) -> Result[None]:
        """
        With the Arduino glitcher, resets the target through it's reset pin.
        """
        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline("R"):
                    case Ok("OK\n"):
                        return Ok(None)
                    case Ok(_):
                        return Err(Exception("Received something else than OK"))
                    case err:
                        return err
            case err:
                return err

    def glitch_after_reset(self) -> Result[None]:
        """
        Resets the target through it's reset pin, then glitch after the set
        delay.
        """
        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline("r"):
                    case Ok("OK\n"):
                        return Ok(None)
                    case Ok(_):
                        return Err(Exception("Received something else than OK"))
                    case err:
                        return err
            case err:
                return err

    def set_no_glitch(self) -> Result[None]:
        """
        Setup the glitcher not to glitch on interrupt.
        """
        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline("G0"):
                    case Ok("Detached glitch interrupt.\n"):
                        return Ok(None)
                    case Ok(answer):
                        return Err(Exception(
                            f"Received unexpected answer: {answer}"
                        ))
                    case err:
                        return err
            case err:
                return err

    def set_simple_glitch(self) -> Result[None]:
        """
        Setup the glitcher to do mono glitches.
        """
        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline("G1"):
                    case Ok("Switched to simple glitch.\n"):
                        return Ok(None)
                    case Ok(answer):
                        return Err(Exception(
                            f"Received unexpected answer: {answer}"
                        ))
                    case err:
                        return err
            case err:
                return err

    def set_double_glitch(self) -> Result[None]:
        """
        Setup the glitcher to do double glitches.
        """
        match self._safe_instrument_reset_input_buffer():
            case Ok(_):
                match self._safe_write_then_readline("G2"):
                    case Ok("Switched to simple glitch.\n"):
                        return Ok(None)
                    case Ok(answer):
                        return Err(Exception(
                            f"Received unexpected answer: {answer}"
                        ))
                    case err:
                        return err
            case err:
                return err
