from machine import Pin, SPI #type: ignore
import time

from .board import Board as IBoard


class Board(IBoard):
    # --- Pins --- #
    nss: Pin

    led: Pin

    def __init__(self):
        super().__init__(
            8,
            19,
            16,
            18,
            9,
            7,
            10,
            None,
            None,
            None,
            None,
            25,
        )

        # Creo il pin NSS
        self.nss = self.pin(self.pin_nss, in_out=Pin.OUT)

    # -------------------------------------------------------------------------------------------- #
    def spi(self) -> object:
        spi = SPI(
            0,
            baudrate=10_000_000,
            polarity=0,
            phase=0,
            sck=Pin(self.pin_sck, Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(self.pin_mosi, Pin.OUT, Pin.PULL_UP),
            miso=Pin(self.pin_miso, Pin.IN, Pin.PULL_UP),
        )
        spi.init()

        return spi

    def pin(self, pin_id: int | None, **args: object) -> object:
        return Pin(pin_id, args["in_out"])

    def add_event(self, pin_id: int | None, callback: object) -> None:
        if pin_id is not None:
            pin = self.pin(pin_id, in_out=Pin.IN)
            pin.irq(handler=callback, trigger=Pin.IRQ_RISING)

    # -------------------------------------------------------------------------------------------- #
    def reset(self) -> None:
        rst = self.pin(self.pin_rst, in_out=Pin.OUT)  # Set Pin in OUTPUT mode
        rst.off()  # Send low

        time.sleep(0.2)
        rst.on()  # Send High
        time.sleep(0.2)

    def cleanup(self) -> None:
        pass  # Non esiste un equivalente di cleanup per la libreria machine

    # -------------------------------------------------------------------------------------------- #
    def blink(
        self,
        times: int,
        secs: float,
        blink_times: int,
        blink_secs: float,
    ) -> None:
        if self.led is None:
            self.led = self.pin(self.pin_led, int_out=Pin.OUT)

        for _ in range(1, times):
            for _ in range(1, blink_times * 2):
                self.led.toggle()
                time.sleep(blink_secs)

            time.sleep(secs)

    # -------------------------------------------------------------------------------------------- #
    def _write(self, reg: int, value: list[int]) -> None:
        wb = bytes([reg | 0x80])
        try:
            self.nss.value(0)
            self._spi.write(wb + bytes(value))
        finally:
            self.nss.value(1)

    def read(self, reg: int) -> int:
        try:
            self.nss.value(0)
            return self._spi.read(2, reg)[1]
        finally:
            self.nss.value(1)

    def reads(self, reg: int, length: int) -> list[int]:
        try:
            self.nss.value(0)
            return self._spi.read(length + 1, reg)[1:]
        finally:
            self.nss.value(1)
