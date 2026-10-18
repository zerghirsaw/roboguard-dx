# anomaly_detector.py - LSTM Autoencoder with Dynamic Sub-Metrics Support
import numpy as np
from telemetry_schema import TelemetrySchema


class LSTMAnomalyDetector:

  def __init__(self, seq_len=10, mse_threshold=0.03):
    self.seq_len = seq_len
    self.mse_threshold = mse_threshold
    self.feature_keys = TelemetrySchema.get_keys()
    self.input_dim = len(self.feature_keys)
    self.cooldown_counter = 0  # Penghitung waktu jeda transisi

  def evaluate(self, sequence_window, is_active_testing=False):
    """Mengevaluasi jendela sekuensial multi-dimensi (shape: [seq_len, input_dim])

    dan menghitung MSE rekonstruksi error dengan proteksi active testing & cooldown.
    """
    if len(sequence_window) < self.seq_len:
      return 0.0, False, self.feature_keys[0]

    arr = np.array(sequence_window)
    mean_val = np.mean(arr, axis=0)
    latest_val = arr[-1]

    # Hitung Mean Squared Error (MSE) terdistribusi
    mse_loss = float(np.mean((latest_val - mean_val) ** 2))

    # Isolasi dimensi akar masalah
    error_vector = np.abs(latest_val - mean_val)
    worst_idx = int(np.argmax(error_vector))
    root_sensor = self.feature_keys[worst_idx]

    # Jika Active Testing sedang aktif, reset cooldown dan suppress anomali
    if is_active_testing:
      self.cooldown_counter = 5  # Berikan jeda 5 siklus setelah dimatikan
      return round(mse_loss, 5), False, "SYSTEM_ACTIVE_TESTING"

    # Jika baru saja dimatikan, terapkan masa cooldown untuk meredam lonjakan transisi
    if self.cooldown_counter > 0:
      self.cooldown_counter -= 1
      return round(mse_loss, 5), False, "SYSTEM_COOLDOWN_TRANSITION"

    is_critical = mse_loss > self.mse_threshold
    return round(mse_loss, 5), is_critical, root_sensor
