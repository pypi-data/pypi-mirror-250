import time

from .boards import Board
from .constants import ASCII_CODE, DEFAULT, PA_DAC, REG
from .my_types import IRQ, MODE


class LoRa(object):
    # SPI
    _board: Board

    # ID del dispositivo
    _device_id: list[int]

    # Frequency of Transmission
    _frequency: float

    # Mode:
    #   - É la modalità di inizio, utilizzata per salvare la modalità quando si effettuano più operazioni
    #   -  É la modalità CURRENT
    _initial_mode: int | None = None
    _current_mode: int | None = None

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def Setup(
        device_id: str,
        frequency: float = DEFAULT.FREQUENCY,
        tx_power: int = DEFAULT.TX_POWER,
        modem_config: tuple[int, int, int] = DEFAULT.MODEM_CONFIG,
        handler: object = None,
        reset: bool = DEFAULT.RESET,
    ):
        try:
            # --- Device ID ---- #
            LoRa._device_id = LoRa._encode(device_id)

            # --- Handler --- #
            LoRa.on_receive = handler  # type: ignore

            # --- Board--- #
            LoRa._board = Board()

            # Reset ?¿?
            if reset:
                LoRa._board.reset()

            # Setup
            LoRa._board.add_events(
                callback_dio0=LoRa._handle_interrupt_dio0,
                callback_dio1=LoRa._handle_interrupt_dioX,
                callback_dio2=LoRa._handle_interrupt_dioX,
                callback_dio3=LoRa._handle_interrupt_dioX,
            )  # Add Events

            # --- Settings --- #
            LoRa.check_module()  # Check if module LoRa is connected
            LoRa.set_mode(MODE.SLEEP)  # For calibration
            # LoRa.reset_fifo()  # Reset Fifo buffer
            LoRa.set_modem_config(modem_config)  # Set Modem Config
            # self.set_preamble()  # Set Preamble
            LoRa.set_frequency(frequency)  # Frequency
            LoRa.set_tx_power(tx_power)  # Transmission Power
            LoRa.set_mode(
                MODE.STANDBY
            )  # Module in Standby -> In questo modo sarà il Main a scegliere il da farsi
        except Exception:
            # Blink del Led
            if LoRa._board:
               LoRa._board.blink(3, 2.5, 3, 0.3)

            # Raise al chiamante
            raise

    # -------------------------------------------------------------------------------------------- #
    # --- Events --- #
    @staticmethod
    def on_receive(payload: bytes, snr: float, rssi: float) -> None:
        raise NotImplementedError(
            "Coglione ti sei dimenticato di implementare la funzione!"
        )

    # -------------------------------------------------------------------------------------------- #
    # --- Module Function --- #
    @staticmethod
    def check_module():
        # Controllo se il modulo è stato correttamente collegato al microcontrollore
        #     Scrivo nel registro e quando rileggo mi devo aspettare lo stesso risultato
        LoRa._board.write(REG.OP_MODE, MODE.SLEEP)
        time.sleep(0.1)

        if LoRa._board.read(REG.OP_MODE) != MODE.SLEEP:
            raise ConnectionError("LoRa initialization failed!")

    @staticmethod
    def reset_fifo():
        # Imposto la posizione di base del buffer FIFO di trasmissione ('FIFO TX') e di ricezione ('FIFO RX) a 0
        # In questo modo i dati trasmessi/ricevuti verranno scritti/letti dall'inizio del Buffer
        LoRa._board.write(REG.FIFO_TX_BASE_ADDR, 0)
        LoRa._board.write(REG.FIFO_RX_BASE_ADDR, 0)

    @staticmethod
    def set_modem_config(modem_config: tuple[int, int, int]):
        # Modem Config: si riferisce alla configurazione del modem LoRa, responsabile della modulazione
        # e della demodulazione dei dati da trasmettere e ricevere su una rete LoRa.
        # La configurazione del modem è una serie di parametri:
        #     - Larghezza di banda (BW)
        #     - Fattore di spreading (SF)
        #     - Codice di correzione degli errori (CR)
        #     - Frequenza di trasmissione:
        #     - Potenza di trasmissione
        #     - Lunghezza del pacchetto
        #     - Tipo di modulazione
        LoRa._board.write(REG.MODEM_CONFIG_1, modem_config[0])
        LoRa._board.write(REG.MODEM_CONFIG_2, modem_config[1])
        LoRa._board.write(REG.MODEM_CONFIG_3, modem_config[2])

    @staticmethod
    def set_preamble() -> None:
        # Set Preamble: è una sequenza di bit inviata prima dei dati effettivi nella trasmissione ed è utilizzato per sincronizzare il ricevitore con il trasmettitore.
        # La configurazione del preambolo è importante perché aiuta il ricevitore a riconoscere l'inizio di una trasmissione e sincronizzarsi con il trasmettitore.
        LoRa._board.write(REG.PREAMBLE_MSB, 0)
        LoRa._board.write(REG.PREAMBLE_LSB, 8)

    @staticmethod
    def set_mode(mode: int):
        if LoRa._current_mode == mode:
            return

        # Aggiorno il registro della modalità
        LoRa._current_mode = mode
        LoRa._board.write(REG.OP_MODE, mode)

        # 1. Interrupt on RXDone: Se trasmetto imposto il dio0 per notificarmi dell'invio dei dati
        # 2. Interrupt on TxDone: Se ricevo imposto il dio0 per notificarmi che ci sta un nuovo messaggio da leggere
        LoRa._board.write(REG.DIO_MAPPING_1, 0x40 if mode == MODE.TX else 0x00)

    @staticmethod
    def set_frequency(frequency: float):
        # Set Frequency: a cui il dispositivo trasmette e riceve dati.
        LoRa._frequency = frequency

        i = int(frequency * 16384.0)
        msb = i // 65536
        i -= msb * 65536
        mid = i // 256
        i -= mid * 256
        lsb = i
        LoRa._board.write(REG.FR_MSB, [msb, mid, lsb])

    @staticmethod
    def set_tx_power(tx_power: int):
        # TX Power (Potenza di Trasmissione): rappresenta la quantità di potenza RF (radiofrequenza) utilizzata dal dispositivo
        # per inviare un segnale, espressa in dBm (decibel-milliwatt)
        #     - Potenza massima 23 dBm
        #     - Potenza minima   5 dBm
        tx_power = max(min(tx_power, 23), 5)

        # Set TX Power:
        #     - in base alla potenza che si vorrà utilizzare per trasmettere i dati, si attiverà/disattiverà un amplificatore di potenza
        #     - imposto la potenza di trasmissione
        if tx_power < 20:
            LoRa._board.write(REG.PA_DAC, PA_DAC.ENABLE)
            tx_power -= 3
        else:
            LoRa._board.write(REG.PA_DAC, PA_DAC.DISABLE)

        LoRa._board.write(REG.PA_CONFIG, PA_DAC.SELECT | (tx_power - 5))

    @staticmethod
    def cleanup():
        LoRa._board.cleanup()

    # -------------------------------------------------------------------------------------------- #
    # --- Writer --- #
    @staticmethod
    def send(data: dict[str, float]):
        # Creo il Payload -> MyDeviceID?Key1=Value1&Key2=Value2
        payload = (
            ASCII_CODE.QUESTION_MARK
            + LoRa._device_id
            + LoRa._encode("&".join(f"{key}={value}" for key, value in data.items()))
        )

        # Mi salvo la modalità, in questo modo appena ricevo il TxDone la rimetto
        LoRa._initial_mode = LoRa._current_mode

        # Size del messaggio
        payload_size = len(payload)
        LoRa._board.write(REG.PAYLOAD_LENGTH, payload_size)

        # Entro in modalità Standby, in questo modo mentre modifico il FIFO non ci sarà il rischio che il modulo si metta in mezzo
        LoRa.set_mode(MODE.STANDBY)
        base_addr = LoRa._board.read(REG.FIFO_TX_BASE_ADDR)
        LoRa._board.write(REG.FIFO_ADDR_PTR, base_addr)
        LoRa._board.write(REG.FIFO, payload)

        # Quando c'è il passaggio dalla modalità di Standby alla modalità di TX (Trasmissione), il modulo trasmette i dati.
        # Infatti esso andrà a leggere dal fifo quello che abbiamo appena inserito
        LoRa.set_mode(MODE.TX)

    # -------------------------------------------------------------------------------------------- #
    # --- Interrupts --- #
    # FIFO (First-In, First-Out): è un buffer dove vengono memorizzati temporaneamente i dati che devono essere
    # trasmetti o che sono stati ricevuti, in ordine FIFO.
    #
    # Questo buffer è diviso in due parti:
    #   - FIFO RX: per i dati che vengono ricevuti
    #   - FIFO TX: per i dati che vengono trasmessi
    #
    # Esso ha 3 puntatori, dove 1 è gestito da noi (FifoAddrPtr) e gli altri due sono gestiti dal modulo (RX Addr e TX Addr):
    #   - FifoAddrPtr (Fifo Address Pointer): punta nella locazione in cui vogliamo effettuare un'operazione di lettura/scrittura.
    #     Ogni volta che vorremmo leggere/scrivere nel FIFO dobbiamo puntare in quella locazione utilizzando questo registro.
    #
    #   - FIFO RX Addr: punta nella locazione di memoria dove sono stati appena ricevuti dei dati
    #   - FIFO TX Addr: punta nella locazione di memoria dove sono stati appena trasmessi dei dati
    #
    # Quando il puntatore raggiunge la fine della FIFO, spesso si "ricicla" all'inizio in modo circolare,
    # poiché la FIFO è una struttura dati circolare.
    #

    # DIO0 00: RxDone
    # DIO0 01: TxDone
    @staticmethod
    def _handle_interrupt_dio0(_: int):
        irq_flags = LoRa.read_irq_flags()

        # DIO0 00: RxDone
        if LoRa._current_mode == MODE.RX_CONTINUOUS and (irq_flags & IRQ.RxDone):
            LoRa.clear_irq_flags(IRQ.RxDone)  # Clear RxDone Flag
            LoRa._on_rx_done()

        # DIO0 01: TxDone
        elif LoRa._current_mode == MODE.TX and (irq_flags & IRQ.TxDone):
            LoRa.clear_irq_flags(IRQ.TxDone)  # Clear TxDone Flag
            LoRa._on_tx_done()

    @staticmethod
    def _handle_interrupt_dioX(channel: int):
        print("Handle Interrupt:", channel)

    # -------------------------------------------------------------------------------------------- #
    # --- On ---- #

    # Messaggio:
    #   [0..7] to -> Device ID del Mittente
    #   [8:] payload -> Messaggio

    @staticmethod
    def _on_rx_done():
        # Recupero la lunghezza del packet appena ricevuto
        packet_len = LoRa._board.read(REG.RX_NB_BYTES)

        # 1. Ottengo l'indirizzo del messaggio appena ricevuto
        # 2. Imposto il puntatore del FIFO a questo indirizzo, così potrò leggere
        fifo_rx_current_addr = LoRa._board.read(REG.FIFO_RX_CURR_ADDR)
        LoRa._board.write(
            REG.FIFO_ADDR_PTR, fifo_rx_current_addr
        )  # Recupero l'indirizzo dell'inizio packet

        # Recupero il packet dal FIFO
        packet = LoRa._board.reads(REG.FIFO, packet_len)

        # (Rapporto segnale-rumore, Potenza del segnale ricevuto)
        (snr, rssi) = LoRa._get_signal_info()

        # Richiamo l'Handler
        LoRa.on_receive(bytes(packet), snr, rssi)

    @staticmethod
    def _on_tx_done():
        # Una volta che ho ricevuto la conferma che il packed che ho appena inserito nel FIFO è stato trasmetto, ritorno alla modalità iniziale (Prima del send)
        LoRa.set_mode(
            LoRa._initial_mode if LoRa._initial_mode is not None else MODE.SLEEP
        )
        LoRa._initial_mode = None

    # -------------------------------------------------------------------------------------------- #
    # --- Utils --- #
    @staticmethod
    def clear_irq_flags(flags: int):
        LoRa._board.write(REG.IRQ_FLAGS, flags)

    @staticmethod
    def read_irq_flags() -> int:
        return LoRa._board.read(REG.IRQ_FLAGS)

    @staticmethod
    def get_all_registers() -> list[int]:
        return [0] + LoRa._board.reads(0x00, 0x3E)[1:]

    @staticmethod
    def _get_signal_info() -> tuple[float, float]:
        # Rapporto segnale-rumore (SNR) espresso in db. Un valore SNR più alto indica una migliore qualità del segnale rispetto al rumore
        snr = LoRa._board.read(REG.PKT_SNR_VALUE) / 4
        # Potenza del segnale ricevuto (RSSI) espresso in dBm. Rappresenta la potenza del segnale ricevuto
        rssi = LoRa._board.read(REG.PKT_RSSI_VALUE)

        # Valori calcoli per correggere l'rssi a seconda di varie condizioni
        if snr < 0:
            rssi = snr + rssi
        else:
            rssi = rssi * 16 / 15
        if LoRa._frequency >= 779:
            rssi = round(rssi - 157, 2)
        else:
            rssi = round(rssi - 164, 2)

        return (snr, rssi)

    @staticmethod
    def _encode(str: str) -> list[int]:
        # Converto la stringa in una lista di int che rappresentano i byte
        return [ord(carattere) for carattere in str]
