from dataclasses import dataclass
import threading

@dataclass
class ThermoData:
    def __init__(self, energy=None):
        self.energy = energy  # Total energy
        self.temp = None  # Temperature
        self.freq_scale = None  # Frequency scaling parameter
        self.zpe = None  # Zero-point correction to energy
        self.te = None  # Thermal correction to energy
        self.th = None  # Thermal correction to enthalpy
        self.ts = None  # Total entropy
        self.ts_trans = None  # Translational entropy
        self.ts_rot = None  # Rotational entropy
        self.ts_vib = None  # Vibrational entropy
        self.cv = None  # Cv (constant volume heat capacity)
        self.cv_trans = None  # Translational Cv
        self.cv_rot = None  # Rotational Cv
        self.cv_vib = None  # Vibrational Cv


@dataclass
class Step:
    step: int
    energy: float
    delta_e: float
    gmax: float
    grms: float
    xrms: float
    xmax: float
    walltime: float


@dataclass
class SystemInfo:
    system_id: str
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str
    ntotal: int


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
