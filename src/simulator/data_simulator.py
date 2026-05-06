"""
Simula el flujo de datos de un wearable (FC + acelerómetro).
Genera escenarios: normal, taquicardia, caída, inactividad prolongada.
"""

import random
import time
from dataclasses import dataclass, asdict
from enum import Enum


class Scenario(Enum):
    NORMAL = "normal"
    TACHYCARDIA = "tachycardia"
    FALL = "fall"
    INACTIVITY = "inactivity"
    PANIC_ATTACK = "panic_attack"


@dataclass
class SensorReading:
    timestamp: float
    heart_rate: int          # bpm
    acceleration_x: float   # g
    acceleration_y: float   # g
    acceleration_z: float   # g
    impact_detected: bool   # pico brusco de aceleración
    scenario: str


def _random_normal() -> SensorReading:
    return SensorReading(
        timestamp=time.time(),
        heart_rate=random.randint(60, 85),
        acceleration_x=round(random.uniform(-0.2, 0.2), 3),
        acceleration_y=round(random.uniform(-0.2, 0.2), 3),
        acceleration_z=round(random.uniform(0.9, 1.1), 3),
        impact_detected=False,
        scenario=Scenario.NORMAL.value,
    )


def _random_tachycardia() -> SensorReading:
    return SensorReading(
        timestamp=time.time(),
        heart_rate=random.randint(110, 150),
        acceleration_x=round(random.uniform(-0.3, 0.3), 3),
        acceleration_y=round(random.uniform(-0.3, 0.3), 3),
        acceleration_z=round(random.uniform(0.8, 1.2), 3),
        impact_detected=False,
        scenario=Scenario.TACHYCARDIA.value,
    )


def _random_fall() -> SensorReading:
    # Una caída real produce picos de 3-8g. Garantizamos al menos 3g en un eje.
    return SensorReading(
        timestamp=time.time(),
        heart_rate=random.randint(90, 130),
        acceleration_x=round(random.uniform(2.5, 4.0), 3),
        acceleration_y=round(random.uniform(1.5, 3.0), 3),
        acceleration_z=round(random.uniform(-2.0, -0.5), 3),
        impact_detected=True,
        scenario=Scenario.FALL.value,
    )


def _random_inactivity() -> SensorReading:
    return SensorReading(
        timestamp=time.time(),
        heart_rate=random.randint(55, 70),
        acceleration_x=0.0,
        acceleration_y=0.0,
        acceleration_z=1.0,
        impact_detected=False,
        scenario=Scenario.INACTIVITY.value,
    )


def _random_panic_attack() -> SensorReading:
    return SensorReading(
        timestamp=time.time(),
        heart_rate=random.randint(130, 175),
        acceleration_x=round(random.uniform(-0.5, 0.5), 3),
        acceleration_y=round(random.uniform(-0.5, 0.5), 3),
        acceleration_z=round(random.uniform(0.7, 1.3), 3),
        impact_detected=False,
        scenario=Scenario.PANIC_ATTACK.value,
    )


_GENERATORS = {
    Scenario.NORMAL: _random_normal,
    Scenario.TACHYCARDIA: _random_tachycardia,
    Scenario.FALL: _random_fall,
    Scenario.INACTIVITY: _random_inactivity,
    Scenario.PANIC_ATTACK: _random_panic_attack,
}


def generate(scenario: Scenario = Scenario.NORMAL) -> dict:
    """Devuelve una lectura como dict listo para pasar al AlertRouter."""
    return asdict(_GENERATORS[scenario]())


def stream(scenario: Scenario = Scenario.NORMAL, interval: float = 1.0):
    """Generador infinito de lecturas. Útil para simular tiempo real."""
    while True:
        yield generate(scenario)
        time.sleep(interval)
