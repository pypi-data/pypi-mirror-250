import RPi.GPIO as GPIO  # type:ignore
import spidev  # type:ignore
import time

from .board import Board as IBoard


class Board(IBoard):
    def __init__(self):
        super().__init__(
            8,
            10,
            9,
            11,
            22,
            4,
            17,
            18,
            27,
            None,
            None,
            None,
        )

        GPIO.setmode(GPIO.BCM)  #  Così posso utilizzare i numeri

        # Setup di tutti i DIO
        for pin in [self.pin_dio0, self.pin_dio1, self.pin_dio2, self.pin_dio3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # -------------------------------------------------------------------------------------------- #
    def spi(self) -> object:
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 5000000

        return spi

    def pin(self, pin_id: int | None, **args: object) -> object:
        GPIO.setup(pin_id, args["in_out"], pull_up_down=args["pull_up_down"])

    def add_event(self, pin_id: int | None, callback: object) -> None:
        if pin_id is not None:
            self.pin(pin_id, in_out=GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin_id, GPIO.RISING, callback=callback)

    # -------------------------------------------------------------------------------------------- #
    def reset(self):
        # Reset del modulo SX127x
        try:
            GPIO.setup(self.pin_rst, GPIO.OUT)  # Set Pin in OUTPUT mode
            GPIO.output(self.pin_rst, GPIO.LOW)  # Send low

            time.sleep(0.2)
            GPIO.output(self.pin_rst, GPIO.HIGH)  # Send High
            time.sleep(0.2)
        finally:
            GPIO.cleanup(self.pin_rst)

    def cleanup(self) -> None:
        GPIO.cleanup()

    # -------------------------------------------------------------------------------------------- #
    def blink(
        self,
        times: int,
        secs: float,
        blink_times: int,
        blink_secs: float,
    ) -> None:
        pass  # Non esiste un Led integrato su questo modello

    # -------------------------------------------------------------------------------------------- #
    def _write(self, reg: int, value: list[int]) -> None:
        self._spi.xfer([reg | 0x80] + value)

    def read(self, reg: int) -> int:
        return self._spi.xfer([reg] + [0])[1]

    def reads(self, reg: int, length: int) -> list[int]:
        return self._spi.xfer([reg] + [0] * length)[1:]
