import sys


def get_raspberry_pi_model():
    # Apri il file /proc/cpuinfo in modalità di lettura
    with open('/proc/cpuinfo', 'r') as cpuinfo_file:
        # Leggi tutte le linee dal file
        lines = cpuinfo_file.readlines()

        # Cerca la linea che contiene il modello
        for line in lines:
            if line.startswith('Model'):
                # Estrai il modello dalla linea
                model_str = line.split(': ')[1].strip()
                return model_str

    # Se non è stata trovata la linea con il modello, restituisci None
    return None


if sys.implementation.name == "micropython":
    # Raspberry Pico Series
    print("Raspberry Pico Series")

    from .board_pico import Board
else:
    # Raspberry Model B | Raspberry Zero
    model = get_raspberry_pi_model()
    if model is None:
        raise Exception(f"Non è stato possibile recuperare il modello della Board.")

    if "Pi Zero" in model:
        print("Raspberry Pi Zero")

        from .board_zero import Board
    elif "Pi B" in model:
        print("Raspberry Model B")

        from .board_model_b import Board
    else:
        raise Exception(f"Non è stato possibile trovare la Board per il modello: {model}.")

