# sensor_simulator.py - Multi-Point Telemetry Simulator
import random
from telemetry_schema import TelemetrySchema


class SensorSimulator:

  def __init__(self):
    self.machine_id = "ROBO-MULTI-EDGE-01"
    self.overrides = {}

  def set_override(self, key: str, value: bool):
    """Menyimpan status override dari panel Universal Active Testing."""
    self.overrides[key] = value

  def generate_reading(self, scenario_name: str) -> dict:
    # Membangkitkan baseline termasuk custom metrics dari registry dinamis
    data = TelemetrySchema.create_baseline_reading(self.machine_id)

    # 1. Injeksi gangguan berdasarkan skenario industri terlebih dahulu
    if "Thermal" in scenario_name or "Suhu" in scenario_name:
      if "temp_core" in data:
        data["temp_core"] = round(random.uniform(68.0, 75.0), 2)
      if "temp_bearing" in data:
        data["temp_bearing"] = round(random.uniform(62.0, 68.0), 2)
      if "current_draw" in data:
        data["current_draw"] = round(random.uniform(3.0, 3.5), 2)
      data["status"] = "CRITICAL_ANOMALY"

    elif "Pressure" in scenario_name or "Tekanan" in scenario_name:
      if "pressure_inlet" in data:
        data["pressure_inlet"] = round(random.uniform(32.0, 38.0), 2)
      if "pressure_outlet" in data:
        data["pressure_outlet"] = round(random.uniform(28.0, 34.0), 2)
      data["status"] = "CRITICAL_ANOMALY"

    elif "Overcurrent" in scenario_name or "Arus" in scenario_name:
      if "current_draw" in data:
        data["current_draw"] = round(random.uniform(3.5, 4.2), 2)
      if "temp_core" in data:
        data["temp_core"] = round(random.uniform(58.0, 63.0), 2)
      data["status"] = "CRITICAL_ANOMALY"

    elif "Bearing" in scenario_name or "Getaran" in scenario_name:
      if "vib_axial" in data:
        data["vib_axial"] = round(random.uniform(2.5, 3.2), 2)
      if "vib_radial" in data:
        data["vib_radial"] = round(random.uniform(2.3, 3.0), 2)
      if "acoustic_db" in data:
        data["acoustic_db"] = round(random.uniform(62.0, 70.0), 2)
      data["status"] = "CRITICAL_ANOMALY"

    elif "RPM" in scenario_name or "Speed" in scenario_name:
      if "rpm_spindle" in data:
        data["rpm_spindle"] = round(random.uniform(1200.0, 1300.0), 2)
      if "rpm_aux" in data:
        data["rpm_aux"] = round(random.uniform(550.0, 620.0), 2)
      data["status"] = "CRITICAL_ANOMALY"

    else:
      # Kondisi Normal (Fluktuasi mikro acak untuk seluruh parameter termasuk custom metrics)
      for k in data:
        if isinstance(data[k], (int, float)):
          data[k] = round(
              data[k] + random.uniform(-0.1, 0.1),
              2,
          )

    # 2. Terapkan efek intervensi aktif (Active Testing Write-Back) di akhir
    # agar langsung mengubah/menstabilkan nilai sensor di monitor secara interaktif
    if self.overrides.get("cooling_pump", False):
      if "temp_core" in data:
        data["temp_core"] = max(35.0, round(data["temp_core"] - 15.0, 2))
      if "temp_bearing" in data:
        data["temp_bearing"] = max(33.0, round(data["temp_bearing"] - 10.0, 2))
      data["status"] = "OPTIMIZING_COOLING"

    if self.overrides.get("pressure_relief", False):
      if "pressure_inlet" in data:
        data["pressure_inlet"] = max(10.0, round(data["pressure_inlet"] - 15.0, 2))
      if "pressure_outlet" in data:
        data["pressure_outlet"] = max(8.0, round(data["pressure_outlet"] - 12.0, 2))
      data["status"] = "RELIEVING_PRESSURE"

    if self.overrides.get("rpm_limiter", False):
      if "rpm_spindle" in data:
        data["rpm_spindle"] = min(1000.0, round(data["rpm_spindle"] * 0.75, 2))
      data["status"] = "LIMITING_RPM"

    return data
