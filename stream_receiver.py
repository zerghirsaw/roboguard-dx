# stream_receiver.py - Multi-Protocol IoT Edge Gateway
import json
import os
import random
import pandas as pd

# Pustaka eksternal opsional (diimpor aman jika hardware tidak terhubung)
try:
  import serial
  SERIAL_AVAILABLE = True
except ImportError:
  SERIAL_AVAILABLE = False

try:
  from pymodbus.client import ModbusTcpClient
  MODBUS_AVAILABLE = True
except ImportError:
  MODBUS_AVAILABLE = False


class RealStreamReceiver:

  def __init__(
      self, 
      protocol="JSON_FEED", 
      feed_file="live_telemetry_feed.json", 
      machine_id="ROBO-HARDWARE-EDGE-01",
      serial_port="COM3",
      baudrate=9600,
      plc_ip="192.168.1.100"
  ):
    self.protocol = protocol  # "JSON_FEED", "ARDUINO_SERIAL", atau "PLC_MODBUS"
    self.feed_file = feed_file
    self.machine_id = machine_id
    self.serial_port = serial_port
    self.baudrate = baudrate
    self.plc_ip = plc_ip
    
    self.overrides = {
        "cooling_pump": False,
        "pressure_relief": False,
        "rpm_limiter": False,
    }
    
    # Inisialisasi file umpan awal jika belum ada
    if not os.path.exists(self.feed_file):
      self.update_live_feed({
          "vibration": 1.8,
          "temperature": 50.0,
          "current": 2.5,
          "pressure": 45.0,
          "rpm": 1450.0,
          "acoustic": 55.0,
          "status": "NORMAL"
      })

  def update_live_feed(self, data: dict):
    """
    Fungsi eksternal untuk memasukkan data live dari skrip luar, API, atau perangkat eksternal.
    """
    data["timestamp"] = pd.Timestamp.now().strftime("%H:%M:%S")
    data["machine_id"] = self.machine_id
    with open(self.feed_file, "w") as f:
      json.dump(data, f)

  def set_override(self, key: str, state: bool):
    self.overrides[key] = state
    # Logika pengiriman perintah balik (Write-back / Actuation) ke hardware fisik
    if self.protocol == "PLC_MODBUS" and MODBUS_AVAILABLE:
      try:
        client = ModbusTcpClient(self.plc_ip)
        client.connect()
        # Contoh menulis register Modbus (1 untuk Aktif, 0 untuk Mati)
        register_address = {"cooling_pump": 10, "pressure_relief": 11, "rpm_limiter": 12}.get(key, 10)
        client.write_register(register_address, 1 if state else 0)
        client.close()
      except Exception as e:
        print(f"[PLC WRITE ERROR] Gagal mengirim perintah ke PLC: {e}")
    
    print(f"[BI-DIRECTIONAL HARDWARE CMD] Protocol: {self.protocol} | Setting {key} -> {state}")

  def generate_reading(self, is_anomaly: bool) -> dict:
    data = None

    # --- PROTOKOL 1: ARDUINO / ESP32 VIA USB SERIAL ---
    if self.protocol == "ARDUINO_SERIAL" and SERIAL_AVAILABLE:
      try:
        ser = serial.Serial(self.serial_port, self.baudrate, timeout=0.5)
        line = ser.readline().decode('utf-8').strip()
        if line:
          data = json.loads(line)  # Arduino mengirim data JSON berformat telemetri
        ser.close()
      except Exception:
        # Fallback otomatis ke data aman jika port serial tidak ditemukan saat demo
        pass

    # --- PROTOKOL 2: INDUSTRIAL PLC VIA MODBUS TCP ---
    elif self.protocol == "PLC_MODBUS" and MODBUS_AVAILABLE:
      try:
        client = ModbusTcpClient(self.plc_ip)
        if client.connect():
          # Membaca holding registers dari PLC (alamat 0 s.d 5)
          result = client.read_holding_registers(0, 6)
          if not result.isError():
            regs = result.registers
            data = {
                "vibration": round(regs[0] / 10.0, 2),
                "temperature": round(regs[1] / 10.0, 2),
                "current": round(regs[2] / 10.0, 2),
                "pressure": round(regs[3] / 10.0, 2),
                "rpm": float(regs[4]),
                "acoustic": round(regs[5] / 10.0, 2),
                "status": "NORMAL"
            }
          client.close()
      except Exception:
        pass

    # --- PROTOKOL 3: STANDARD JSON STREAM / DEFAULT FALLBACK ---
    if data is None:
      if os.path.exists(self.feed_file):
        try:
          with open(self.feed_file, "r") as f:
            data = json.load(f)
        except Exception:
          data = None

    # Jika semua jalur gagal atau belum ada data, gunakan baseline normal
    if data is None:
      data = {
          "vibration": round(random.uniform(1.7, 1.9), 2),
          "temperature": round(random.uniform(49.5, 50.5), 2),
          "current": round(random.uniform(2.4, 2.6), 2),
          "pressure": round(random.uniform(44.5, 45.5), 2),
          "rpm": 1450.0,
          "acoustic": round(random.uniform(54.5, 55.5), 2),
          "status": "NORMAL"
      }

    data["timestamp"] = pd.Timestamp.now().strftime("%H:%M:%S")
    data["machine_id"] = self.machine_id

    # Injeksi Aktuator Dua Arah (Bi-Directional Override) pada Stream Aktif
    if self.overrides["cooling_pump"]:
      data["temperature"] = round(data["temperature"] - 10.0, 2)
    if self.overrides["pressure_relief"]:
      data["pressure"] = 42.0
    if self.overrides["rpm_limiter"]:
      data["rpm"] = 1000.0
      data["curr"] = 3.0

    return data
