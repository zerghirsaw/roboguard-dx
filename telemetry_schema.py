# telemetry_schema.py - Modular Multi-Point Telemetry & Sub-Metrics Schema
import time
import numpy as np
import streamlit as st


class TelemetrySchema:
  """Mengelola hierarki sub-metrik telemetri multi-titik industri dan custom metrics dinamis."""

  BASE_REGISTRY = {
      # Thermal Group
      "temp_core": {
          "group": "Thermal Sub-System",
          "label_id": "Suhu Inti Mesin (Core)",
          "label_en": "Core Temperature",
          "unit": "°C",
          "default": 50.0,
          "safe_max": 65.0,
      },
      "temp_bearing": {
          "group": "Thermal Sub-System",
          "label_id": "Suhu Bantalan (Bearing)",
          "label_en": "Bearing Temperature",
          "unit": "°C",
          "default": 48.0,
          "safe_max": 60.0,
      },
      "temp_ambient": {
          "group": "Thermal Sub-System",
          "label_id": "Suhu Lingkungan (Ambient)",
          "label_en": "Ambient Temperature",
          "unit": "°C",
          "default": 30.0,
          "safe_max": 45.0,
      },
      # Kinematic Group
      "rpm_spindle": {
          "group": "Kinematic Sub-System",
          "label_id": "RPM Poros Utama (Spindle)",
          "label_en": "Spindle Angular Velocity",
          "unit": "RPM",
          "default": 1450.0,
          "target": 1450.0,
      },
      "rpm_aux": {
          "group": "Kinematic Sub-System",
          "label_id": "RPM Penggerak Pembantu (Aux)",
          "label_en": "Auxiliary Motor RPM",
          "unit": "RPM",
          "default": 720.0,
          "target": 720.0,
      },
      # Mechanical & Vibration Group
      "vib_axial": {
          "group": "Mechanical & Vibration",
          "label_id": "Getaran Aksial (RMS)",
          "label_en": "Axial Shaft Vibration",
          "unit": "mm/s",
          "default": 1.8,
          "safe_max": 2.0,
      },
      "vib_radial": {
          "group": "Mechanical & Vibration",
          "label_id": "Getaran Radial (RMS)",
          "label_en": "Radial Shaft Vibration",
          "unit": "mm/s",
          "default": 1.5,
          "safe_max": 2.0,
      },
      # Hydraulic Group
      "pressure_inlet": {
          "group": "Hydraulic Sub-System",
          "label_id": "Tekanan Masuk (Inlet Pressure)",
          "label_en": "Inlet Line Pressure",
          "unit": "Bar",
          "default": 45.0,
          "target": 45.0,
      },
      "pressure_outlet": {
          "group": "Hydraulic Sub-System",
          "label_id": "Tekanan Keluar (Outlet Pressure)",
          "label_en": "Outlet Line Pressure",
          "unit": "Bar",
          "default": 42.0,
          "target": 42.0,
      },
      # Electrical & Acoustic Group
      "current_draw": {
          "group": "Electrical Sub-System",
          "label_id": "Arus Total Motor (Current Draw)",
          "label_en": "Total Motor Current",
          "unit": "A",
          "default": 2.5,
          "safe_max": 3.2,
      },
      "acoustic_db": {
          "group": "Acoustic Sub-System",
          "label_id": "Emisi Kebisingan (Acoustic Spectrum)",
          "label_en": "Acoustic Emission dB",
          "unit": "dB",
          "default": 55.0,
          "safe_max": 65.0,
      },
  }

  @classmethod
  def get_registry(cls):
    """Menggabungkan registry bawaan dengan custom metrics dari st.session_state."""
    registry = cls.BASE_REGISTRY.copy()
    if "custom_metrics_registry" in st.session_state:
      registry.update(st.session_state.custom_metrics_registry)
    return registry

  @classmethod
  def get_keys(cls):
    return list(cls.get_registry().keys())

  @classmethod
  def create_baseline_reading(cls, machine_id="ROBO-MULTI-EDGE-01"):
    reg = cls.get_registry()
    reading = {k: v["default"] for k, v in reg.items()}
    reading["machine_id"] = machine_id
    reading["status"] = "NORMAL"
    reading["timestamp"] = time.strftime("%H:%M:%S")
    return reading

  @classmethod
  def vectorize(cls, telemetry_dict):
    reg = cls.get_registry()
    return np.array(
        [
            float(telemetry_dict.get(k, reg[k]["default"]))
            for k in reg.keys()
        ],
        dtype=np.float32,
    )
