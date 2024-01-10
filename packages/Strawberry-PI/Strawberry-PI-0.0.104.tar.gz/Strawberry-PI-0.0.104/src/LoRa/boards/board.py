class Board:
    # --- Pins --- #
    pin_nss: int | None
    pin_mosi: int | None
    pin_miso: int | None
    pin_sck: int | None
    pin_rst: int | None
    pin_dio0: int | None
    pin_dio1: int | None
    pin_dio2: int | None
    pin_dio3: int | None
    pin_dio4: int | None
    pin_dio5: int | None

    pin_led: int | None

    # -------------------------------------------------------------------------------------------- #
    # --- SPI (Serial Peripheral Interface) for LoRa Module (SX1278) ---  #
    # Serve per aprire una connessione seriale (SPI) utilizzato per la comunicazione tra
    # dispositivi esterni (dispositivi come sensori, display e altre periferiche) e il microcontrollore:
    #     - Bus: Il primo argomento specifica il numero del BUS SPI  si desidera utilizzare
    #       In genere, Raspberry Pi ha due bus SPI (SPI0, quello principale e SPI1 quello secondario)
    #     - Channel: Il secondo argomento specifica i PIN da utilizzare per comunicare con il dispositivo:
    #        1. SPI0 (bus 0): È accessibile tramite i pin GPIO 9 (MISO), 10 (MOSI), 11 (SCLK), 8 (CE0), e 7 (CE1).
    #        2. SPI1 (bus 1): È accessibile tramite i pin GPIO 19 (MISO), 20 (MOSI), 21 (SCLK), 18 (CE0), e 17 (CE1).
    _spi: object

    def __init__(
        self,
        pin_nss: int | None,
        pin_mosi: int | None,
        pin_miso: int | None,
        pin_sck: int | None,
        pin_rst: int | None,
        pin_dio0: int | None,
        pin_dio1: int | None,
        pin_dio2: int | None,
        pin_dio3: int | None,
        pin_dio4: int | None,
        pin_dio5: int | None,
        pin_led: int | None,
    ) -> None:
        self.pin_nss = pin_nss
        self.pin_mosi = pin_mosi
        self.pin_miso = pin_miso
        self.pin_sck = pin_sck
        self.pin_rst = pin_rst
        self.pin_dio0 = pin_dio0
        self.pin_dio1 = pin_dio1
        self.pin_dio2 = pin_dio2
        self.pin_dio3 = pin_dio3
        self.pin_dio4 = pin_dio4
        self.pin_dio5 = pin_dio5
        self.pin_led = pin_led

        self._spi = self.spi()

    # -------------------------------------------------------------------------------------------- #
    def spi(self) -> object:
        raise NotImplementedError()

    def pin(self, pin_id: int | None, **args: object) -> object:
        raise NotImplementedError()

    def add_event(self, pin_id: int | None, callback: object) -> None:
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------------- #
    def add_events(
        self,
        callback_dio0: object,
        callback_dio1: object,
        callback_dio2: object,
        callback_dio3: object,
    ):
        # Aggiungo tutti gli eventi da detectare
        self.add_event(self.pin_dio0, callback_dio0)
        self.add_event(self.pin_dio1, callback_dio1)
        self.add_event(self.pin_dio2, callback_dio2)
        self.add_event(self.pin_dio3, callback_dio3)

    # -------------------------------------------------------------------------------------------- #
    def reset(self) -> None:
        raise NotImplementedError()

    def cleanup(self) -> None:
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------------- #
    def blink(
        self,
        times: int,
        secs: float,
        blink_times: int,
        blink_secs: float,
    ) -> None:
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------------- #
    def write(self, reg: int, value: int | list[int]) -> None:
        # Converto il value in un Array
        payload: list[int] = value if isinstance(value, list) else [value]

        self._write(reg, payload)

    def _write(self, reg: int, value: list[int]) -> None:
        raise NotImplementedError()

    def read(self, reg: int) -> int:
        raise NotImplementedError()

    def reads(self, reg: int, length: int) -> list[int]:
        raise NotImplementedError()