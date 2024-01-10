import setuptools
import os


# -------------------------------------------------------------------------------------------- #
# ---- Utils ---- #
def get_version() -> str:
    # Here Path -> Path di questa directory
    here = os.path.abspath(os.path.dirname(__file__))
    # __version__ path -> Path di dove si trova la versione
    version_path = os.path.join(here, ".__version__")
    __version__ = "0.0.0"

    with open(version_path, "r+") as f:
        # Read version
        __version__ = f.read().split(".")

        # Controllo se è valido
        if len(__version__) != 3:
            raise Exception(
                "Formato versione non valido! Controllare il file '.__version__'"
            )

        # Recupero i 3 numeri
        major = __version__[0]
        minor = __version__[1]
        patch = __version__[2]

        __new_version__ = f"{major}.{minor}.{int(patch) + 1}"

        # Scrivo la nuova versione
        f.seek(0)
        f.write(__new_version__)

    return ".".join(__version__)


def get_long_description():
    with open("README.md", "r") as f:
        return f.read()


# -------------------------------------------------------------------------------------------- #
# ---- Setup ---- #
setuptools.setup(
    name="Strawberry-PI",
    version=get_version(),
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    url="https://github.com/LuisTheProgrammer/Strawberry-PI",
    author="Luis Di Matteo",
    author_email="luiss.dimatteo@gmail.com",
    description="LoRa communication library for Raspberry Pi",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={"console_scripts": ["forge = forge:main"]},
    # install_requires=["RPi.GPIO", "spidev"],
)
