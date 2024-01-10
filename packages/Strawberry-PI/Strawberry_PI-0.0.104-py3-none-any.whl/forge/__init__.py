import os
import sys
import console


# -------------------------------------------------------------------------------------------- #
# Contenuto che dovrà essere scritto nel service file
CONTENT = """[Unit]
Description={name} service
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {path}
Restart=always
RuntimeMaxSec=infinity

[Install]
WantedBy=multi-user.target"""


# -------------------------------------------------------------------------------------------- #
def main() -> int:
    # Accetto solo 2 parametri:
    #   0. Nome del file che python eseguire
    #   1. Il mio parametro, ovvero il file che dovrà essere convertito in Service
    if len(sys.argv) != 2:
        raise Exception(
            "Fornire il path dello script che si vuole trasformare in Service!"
        )

    # Path Relativo -> MyProject/MyScript.py
    relative_script_path = sys.argv[1]
    # Path Absolute -> /home/<User>/Desktop/MyProject/MyScript.py
    abs_script_path = os.path.abspath(relative_script_path)
    # Path Dir -> /home/<User>/Desktop/MyProject
    dir_path = os.path.dirname(abs_script_path)
    # Full Name -> MyScript.py
    full_name_script_path = os.path.basename(relative_script_path)
    # Name -> MyScript
    name_script = ".".join(full_name_script_path.split(".")[:-1])

    # Check if Script is a File
    if not os.path.isfile(abs_script_path):
        raise Exception("Fornire il path di uno script .py!")

    # Creo un file momentaneo
    temp_file_path = os.path.join(dir_path, f"{name_script}.service")
    try:
        with open(temp_file_path, "w") as tmp_file:
            tmp_file.write(CONTENT.format(name=name_script, path=abs_script_path))

        # Controllo se il path finale esiste
        service_path = "/etc/systemd/system/"
        if not os.path.exists(service_path):
            raise Exception(f"Impossibile trovare la directory: '{service_path}'")

        # Copio il temp file nella folder dei servizi
        os.system(f"sudo cp {temp_file_path} {service_path}")
    finally:
        # Elimino il temp_file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    # Controllo che mi trovo su Linux
    if sys.platform != "linux" and sys.platform != "linux2":
        raise Exception("Sistema operativo incompatibile, deve essere linux o linux2")

    # Enable Servizio & Start IT
    os.system("sudo systemctl daemon-reload")
    os.system(f"sudo systemctl enable {name_script}")
    os.system(f"sudo systemctl start {name_script}")
    os.system(f"sudo systemctl status {name_script}")

    return 0


if __name__ == "__main__":
    main()
