# -------------------------------------------------------------------------------------------- #
# --- Modem Config --- #
# -------------------------------------------------------------------------------------------- #


class ModemConfigs:
    Bw125Cr45Sf128 = (0x72, 0x74, 0x04)
    Bw500Cr45Sf128 = (0x92, 0x74, 0x04)
    Bw31_25Cr48Sf512 = (0x48, 0x94, 0x04)
    Bw125Cr48Sf4096 = (0x78, 0xC4, 0x0C)


# -------------------------------------------------------------------------------------------- #
# LoRa Modes #
# -------------------------------------------------------------------------------------------- #
class MODE:
    SLEEP = 0x80
    # In questa modalità il modulo non fa nulla, questo è molto utile quando bisogna lavorare sui buffer, tipo FIFO
    STANDBY = 0x81

    # Ricezione continua -> Continuo a ricevere fino a quando non cambierò MODE
    RX_CONTINUOUS = 0x85
    # Ricezione singola -> Ricevo una singola volta per poi tornare nello stato STANDBY (Tutto questo in automatico)
    RX_SINGLE = 0x86

    # Modalità di Invio: TX | LONG_RANGE
    TX = 0x83


# -------------------------------------------------------------------------------------------- #
# LoRa IRF (Interrupt Request Flags) #
# -------------------------------------------------------------------------------------------- #
class IRQ:
    CadDetected = 1
    FhssChangeChannel = 2
    CadDone = 4
    TxDone = 8
    ValidHeader = 16
    PayloadCrcError = 32
    RxDone = 64
    RxTimeout = 128
