# app.py - RoboGuard DX Enterprise Diagnostic Terminal
import time
from collections import deque
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from anomaly_detector import LSTMAnomalyDetector
from copilot_engine import TechnicianCoPilot
from sensor_simulator import SensorSimulator
from stream_receiver import RealStreamReceiver
from config_diagnostic import ROOT_CAUSE_MAP
from i18n import TEXTS
from guide import render_user_guide  # Modul Buku Panduan Operasional
from telemetry_schema import TelemetrySchema  # Skema Multi-Point Sub-Metrics

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="ROBOGUARD DX // TERMINAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INISIALISASI CUSTOM METRICS REGISTRY ---
if "custom_metrics_registry" not in st.session_state:
  st.session_state.custom_metrics_registry = {}

# --- SIDEBAR: PEMILIH BAHASA (TEMA DIKUNCI KE STABLE DARK) ---
with st.sidebar:
  st.markdown("### SYSTEM TERMINAL")
  selected_lang = st.selectbox("Interface Language", ["Indonesian", "English"])
  t = TEXTS[selected_lang]

# Palet Warna Mono Dark Stabil
bg_color = "#0b0f19"
box_bg = "#0d1117"
text_color = "#ffffff"
border_color = "#30363d"
muted_color = "#8b949e"
line_color = "#ffffff"
tab_bg = "#161b22"
tab_box = "#1f242c"
tab_active = "#21262d"
input_bg = "#161b22"
input_text = "#ffffff"
btn_bg = "#21262d"
btn_text = "#ffffff"

# --- CUSTOM CSS STYLING (STABLE MONO DARK) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600;700&display=swap');

    /* Paksa Kontainer Utama Streamlit */
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Paksa seluruh teks, label, dan markdown */
    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {{
        color: {text_color} !important;
    }}

    /* Terminal Console Box */
    .terminal-box {{
        background-color: {box_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Share Tech Mono', monospace;
        color: {text_color} !important;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }}
    
    .terminal-header {{
        color: {muted_color} !important;
        font-size: 0.85rem;
        border-bottom: 1px solid {border_color};
        padding-bottom: 5px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}

    /* Kotak Input & Selectbox */
    input, textarea {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        -webkit-text-fill-color: {input_text} !important;
        border-color: {border_color} !important;
    }}

    div[data-baseweb="base-input"], div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        border-color: {border_color} !important;
        color: {input_text} !important;
    }}

    [data-baseweb="select"] span, [data-baseweb="select"] div, [data-baseweb="menu"] div {{
        color: {input_text} !important;
    }}

    /* Tombol Aksi */
    .stButton button, .stFormSubmitButton button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {border_color} !important;
        font-weight: 600 !important;
    }}
    .stButton button:hover, .stFormSubmitButton button:hover {{
        border-color: {line_color} !important;
        color: {line_color} !important;
    }}

    /* Override metric cards */
    [data-testid="stMetricValue"] {{
        font-family: 'Share Tech Mono', monospace;
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif;
        color: {muted_color} !important;
        font-weight: 600 !important;
    }}

    /* Delta metrik */
    [data-testid="stMetricDelta"] svg {{
        fill: {text_color} !important;
    }}
    [data-testid="stMetricDelta"] div, 
    [data-testid="stMetricDelta"] span {{
        color: {text_color} !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background-color: {tab_bg} !important;
        padding: 8px;
        border-radius: 6px;
        border: 1px solid {border_color};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Share Tech Mono', monospace;
        background-color: {tab_box} !important;
        border: 1px solid {border_color} !important;
        border-radius: 4px !important;
        opacity: 1 !important;
        cursor: pointer;
        padding: 6px 14px;
    }}

    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] p {{
        color: {text_color} !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }}

    .stTabs [data-baseweb="tab"]:hover div,
    .stTabs [data-baseweb="tab"]:hover span,
    .stTabs [data-baseweb="tab"]:hover p {{
        color: {line_color} !important;
        opacity: 1 !important;
    }}

    /* Tab Aktif */
    .stTabs [aria-selected="true"] {{
        background-color: {tab_active} !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}

    .stTabs [aria-selected="true"] div,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] p {{
        color: {text_color} !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }}
</style>
""", unsafe_allow_html=True)

SEQ_LEN = 10

if "detector" not in st.session_state:
  st.session_state.detector = LSTMAnomalyDetector(seq_len=SEQ_LEN)
if "copilot" not in st.session_state:
  st.session_state.copilot = TechnicianCoPilot()
if "data_history" not in st.session_state:
  st.session_state.data_history = deque(maxlen=35)
if "freeze_frames" not in st.session_state:
  st.session_state.freeze_frames = []
if "last_log_time" not in st.session_state:
  st.session_state.last_log_time = 0.0

# Inisialisasi Session State untuk Active Testing (Global Persistence)
if "override_cooling" not in st.session_state:
  st.session_state.override_cooling = False
if "override_relief" not in st.session_state:
  st.session_state.override_relief = False
if "override_rpm" not in st.session_state:
  st.session_state.override_rpm = False

if "sequence_buffer" not in st.session_state:
  baseline_dict = TelemetrySchema.create_baseline_reading()
  initial_vector = TelemetrySchema.vectorize(baseline_dict)
  initial_dummy = np.array([initial_vector for _ in range(SEQ_LEN)])
  st.session_state.sequence_buffer = deque(initial_dummy.tolist(), maxlen=SEQ_LEN)

if "last_metrics" not in st.session_state:
  st.session_state.last_metrics = {k: 0.0 for k in TelemetrySchema.get_keys()}

# --- SIDEBAR LANJUTAN (KONFIGURASI INGESTI) ---
with st.sidebar:
  st.markdown("---")
  st.markdown(f"### {t['sidebar_config']}")
  datasource_mode = st.selectbox(
      t["datasource_mode"], 
      [t["sim_mode_label"], t["stream_mode_label"]]
  )
  
  st.markdown("---")
  
  if t["sim_mode_label"] in datasource_mode:
    st.markdown(f"#### {t['sim_header']}")
    simulation_mode = st.selectbox(t["sim_scenario"], t["scenarios"])
    if "simulator" not in st.session_state:
      st.session_state.simulator = SensorSimulator()
    data_provider = st.session_state.simulator
  else:
    st.markdown(f"#### {t['stream_header']}")
    hardware_protocol = st.selectbox(
        t["stream_proto"],
        ["JSON Web Feed", "Arduino / ESP32 (USB Serial)", "PLC Industrial (Modbus TCP)"]
    )
    
    proto_map = {
        "JSON Web Feed": "JSON_FEED",
        "Arduino / ESP32 (USB Serial)": "ARDUINO_SERIAL",
        "PLC Industrial (Modbus TCP)": "PLC_MODBUS"
    }
    
    if "stream_receiver" not in st.session_state or st.session_state.get("active_proto") != proto_map[hardware_protocol]:
      st.session_state.active_proto = proto_map[hardware_protocol]
      st.session_state.stream_receiver = RealStreamReceiver(protocol=proto_map[hardware_protocol])
        
    data_provider = st.session_state.stream_receiver

  st.markdown("---")
  auto_refresh = st.toggle(t["auto_refresh"], value=True)
  refresh_rate = st.slider(t["refresh_rate"], 0.5, 2.0, 1.0) if auto_refresh else 0

# --- SINKRONISASI GLOBAL ACTIVE TESTING (DIKIRIM SEBELUM GENERATE) ---
if hasattr(data_provider, "set_override"):
  data_provider.set_override("cooling_pump", st.session_state.override_cooling)
  data_provider.set_override("pressure_relief", st.session_state.override_relief)
  data_provider.set_override("rpm_limiter", st.session_state.override_rpm)

# Tentukan status active testing terlebih dahulu
active_testing_engaged = (
    st.session_state.override_cooling or 
    st.session_state.override_relief or 
    st.session_state.override_rpm
)

# --- EKSEKUSI PENGAMBILAN DATA & PRESISI ---
if t["sim_mode_label"] in datasource_mode:
  raw_data = data_provider.generate_reading(simulation_mode)
  is_critical = (simulation_mode != t["scenarios"][0]) and not active_testing_engaged
else:
  raw_data = data_provider.generate_reading(is_anomaly=False)
  is_critical = (raw_data.get("status") == "CRITICAL_ANOMALY")

current_vector = TelemetrySchema.vectorize(raw_data)
if len(current_vector) != len(st.session_state.sequence_buffer[0]):
  initial_dummy = np.array([current_vector for _ in range(SEQ_LEN)])
  st.session_state.sequence_buffer = deque(initial_dummy.tolist(), maxlen=SEQ_LEN)

st.session_state.sequence_buffer.append(current_vector.tolist())

seq_window = np.array(list(st.session_state.sequence_buffer))

# Evaluasi detektor dengan menyertakan argumen is_active_testing
mse_loss, is_critical_ai, root_sensor = st.session_state.detector.evaluate(
    seq_window, 
    is_active_testing=active_testing_engaged
)

if active_testing_engaged:
  is_critical_ai = False
  is_critical = False
  root_sensor = "SYSTEM_ACTIVE_TESTING"

is_critical = is_critical or is_critical_ai

raw_data["lstm_score"] = round(float(mse_loss), 5)
st.session_state.data_history.append(raw_data)

# Freeze Frame Logic (Debounce 5 detik)
current_time = time.time()
if is_critical and (current_time - st.session_state.last_log_time > 5):
  ff_entry = {
      "time": raw_data.get("timestamp", "N/A"),
      "mse": raw_data["lstm_score"],
      "sensor_data": raw_data.copy(),
      "root_sensor": root_sensor,
      "desc": ROOT_CAUSE_MAP.get(root_sensor, {}).get("desc", "Anomali terdeteksi pada subsistem terkait."),
      "cause": ROOT_CAUSE_MAP.get(root_sensor, {}).get("cause", "Pemeriksaan lapangan diperlukan.")
  }
  st.session_state.freeze_frames.insert(0, ff_entry) 
  st.session_state.last_log_time = current_time

last = st.session_state.last_metrics
deltas = {k: round(raw_data.get(k, 0.0) - last.get(k, 0.0), 2) for k in TelemetrySchema.get_keys()}
st.session_state.last_metrics = {k: raw_data.get(k, 0.0) for k in TelemetrySchema.get_keys()}

# --- TAMPILAN UTAMA (TERMINAL STYLE) ---
st.markdown(f"""
    <div style="font-family: 'Share Tech Mono', monospace; font-size: 1.8rem; font-weight: bold; color: {text_color}; margin-bottom: 0px;">
        ROBOGUARD DX <span style="font-size: 1rem; color: {muted_color};">// MULTI-POINT & CUSTOM METRIC EXPLORER</span>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t.get("tab1", "[1] LIVE TELEMETRY"), 
    t.get("tab2", "[2] ACTIVE TESTING"), 
    t.get("tab3", "[3] FREEZE FRAMES"), 
    t.get("tab4", "[4] USER MANUAL"),
    "[5] CUSTOM METRIC & STREAM BUILDER"
])

with tab1:
  # Terminal Status Header Box
  st.markdown(f"""
      <div class="terminal-box">
          <div class="terminal-header">&gt;&gt; DYNAMIC TELEMETRY STREAM FEED // {raw_data.get('machine_id', 'ROBO-NODE')}</div>
          ACTIVE CHANNEL: <span style="color: {text_color}; font-weight: bold;">{datasource_mode}</span> | 
          TIMESTAMP: <span style="color: {text_color}; font-weight: bold;">{raw_data.get('timestamp', 'LIVE')}</span> | 
          STATUS: <span style="color: {text_color}; font-weight: bold; border: 1px solid {border_color}; padding: 2px 6px;">{raw_data.get('status', 'NORMAL')}</span>
      </div>
  """, unsafe_allow_html=True)
  
  # Menampilkan Seluruh Metrik (Bawaan & Custom) Secara Dinamis
  metric_keys = TelemetrySchema.get_keys()
  for i in range(0, len(metric_keys), 4):
    cols = st.columns(4)
    for j in range(4):
      if i + j < len(metric_keys):
        key = metric_keys[i + j]
        meta = TelemetrySchema.get_registry()[key]
        label_name = meta.get('label_id', key) if selected_lang == 'Indonesian' else meta.get('label_en', key)
        val = raw_data.get(key, meta['default'])
        d_val = deltas.get(key, 0.0)
        
        with cols[j]:
          st.metric(
              label=label_name,
              value=f"{val} {meta['unit']}",
              delta=d_val,
              delta_color="off",
              help=meta.get('group', 'Industrial Sub-System')
          )

  c_mse = st.columns(1)[0]
  c_mse.metric(
      label="Skor Error Rekonstruksi AI (LSTM MSE)",
      value=f"{raw_data['lstm_score']}",
      help="Ambang batas normal: < 0.03"
  )
  
  st.divider()

  if is_critical:
    st.error(f"ALARM KRITIS: Anomali Sekuensial Terdeteksi (MSE: {raw_data['lstm_score']}). Isolasi Autoencoder: Kerusakan berpusat pada sub-sistem {root_sensor}.")
  else:
    st.success("Sistem Stabil. Aliran telemetri multi-titik dan rekonstruksi sekuensial berada di bawah ambang batas kritis.")

  st.markdown(f"<div style='font-family: monospace; color: {muted_color}; margin-top: 15px;'>&gt;&gt; HIGH-PRECISION OSCILLOSCOPE TREND ANALYSIS (ALL METRICS)</div>", unsafe_allow_html=True)
  
  df_chart = pd.DataFrame(st.session_state.data_history)

  def render_monochrome_chart(column_name, title_text):
      if column_name not in df_chart.columns:
          df_chart[column_name] = 0.0
      base = alt.Chart(df_chart).encode(
          x=alt.X("timestamp:N", sort=None, axis=alt.Axis(labelAngle=0, title="Timestamp", labelColor=muted_color, titleColor=muted_color)),
          y=alt.Y(f"{column_name}:Q", title=title_text, scale=alt.Scale(zero=False, padding=10), axis=alt.Axis(labelColor=muted_color, titleColor=muted_color)),
          tooltip=["timestamp:N", alt.Tooltip(f"{column_name}:Q", format=".3f")]
      )
      line = base.mark_line(color=line_color, strokeWidth=2)
      points = base.mark_circle(color=line_color, size=35)
      return (line + points).properties(height=160)

  # Render Grafik secara Dinamis untuk SELURUH Metrik (Termasuk Custom Metrics)
  for i in range(0, len(metric_keys), 2):
    col_g1, col_g2 = st.columns(2)
    with col_g1:
      key1 = metric_keys[i]
      meta1 = TelemetrySchema.get_registry()[key1]
      lbl1 = meta1.get('label_id', key1) if selected_lang == 'Indonesian' else meta1.get('label_en', key1)
      st.markdown(f"<span style='font-family: monospace; color: {text_color}; font-weight: bold;'>■ {lbl1}</span>", unsafe_allow_html=True)
      st.altair_chart(render_monochrome_chart(key1, meta1['unit']), width="stretch")
      
    with col_g2:
      if i + 1 < len(metric_keys):
        key2 = metric_keys[i + 1]
        meta2 = TelemetrySchema.get_registry()[key2]
        lbl2 = meta2.get('label_id', key2) if selected_lang == 'Indonesian' else meta2.get('label_en', key2)
        st.markdown(f"<span style='font-family: monospace; color: {text_color}; font-weight: bold;'>■ {lbl2}</span>", unsafe_allow_html=True)
        st.altair_chart(render_monochrome_chart(key2, meta2['unit']), width="stretch")

with tab2:
  st.markdown(f"### {t['at_title']}")
  st.info(t["at_info"])
  
  v1, v2, v3 = st.columns(3)
  with v1:
    st.markdown(f"**{t['sub_thermal']}**")
    if st.session_state.override_cooling:
      st.success(t["status_active"])
    else:
      st.info(t["status_standby"])
      
  with v2:
    st.markdown(f"**{t['sub_hydro']}**")
    if st.session_state.override_relief:
      st.warning(t["status_bypass"])
    else:
      st.info(t["status_stable"])

  with v3:
    st.markdown(f"**{t['sub_elec']}**")
    if st.session_state.override_rpm:
      st.warning(t["status_limited"])
    else:
      st.info(t["status_optimal"])

  st.markdown("---")
  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(f"**{t['sub_thermal']}**")
    st.toggle(t["toggle_cool"], key="override_cooling")
  with col2:
    st.markdown(f"**{t['sub_hydro']}**")
    st.toggle(t["toggle_press"], key="override_relief")
  with col3:
    st.markdown(f"**{t['sub_elec']}**")
    st.toggle(t["toggle_rpm"], key="override_rpm")

with tab3:
  st.markdown(f"### {t['ff_title']}")
  st.info(t["ff_info"])
  
  if len(st.session_state.freeze_frames) == 0:
    st.write(t["ff_empty"])
  else:
    for idx, frame in enumerate(st.session_state.freeze_frames):
      with st.expander(t["ff_log"].format(time=frame['time'], mse=frame['mse'])):
        st.markdown(f"**{t['ff_root']}** **{frame['root_sensor']}**")
        st.markdown(f"**{t['ff_desc']}** {frame['desc']}")
        st.markdown(f"**{t['ff_cause']}** {frame['cause']}")
        st.markdown(f"**{t['ff_snap']}**")
        st.json(frame['sensor_data'])

with tab4:
  render_user_guide(selected_lang)

with tab5:
  st.markdown("### CUSTOM METRIC & STREAM BUILDER")
  st.markdown("Buat metrik sensor custom baru secara instan melalui GUI. Sistem AI (LSTM Autoencoder) dan osiloskop live stream akan otomatis menyesuaikan dimensi vektor data secara real-time.")
  
  with st.form("custom_metric_form"):
    c_key = st.text_input("Metric Key ID (contoh: temp_motor_b, vib_z, pressure_return)")
    c_label_id = st.text_input("Label Nama (Bahasa Indonesia)")
    c_label_en = st.text_input("Label Name (English)")
    c_unit = st.text_input("Satuan Ukur (contoh: °C, Bar, RPM, mm/s, V, A)")
    c_default = st.number_input("Nilai Awal (Default Baseline)", value=25.0)
    c_group = st.selectbox("Grup Subsistem Industri", [
        "Thermal Sub-System", 
        "Kinematic Sub-System", 
        "Mechanical & Vibration", 
        "Hydraulic Sub-System", 
        "Electrical Sub-System", 
        "Custom Field Sensor"
    ])
    
    submitted = st.form_submit_button("Daftarkan & Aktifkan Stream Metrik Baru")
    if submitted and c_key:
      clean_key = c_key.strip().lower().replace(" ", "_")
      st.session_state.custom_metrics_registry[clean_key] = {
          "group": c_group,
          "label_id": c_label_id if c_label_id else clean_key,
          "label_en": c_label_en if c_label_en else clean_key,
          "unit": c_unit if c_unit else "unit",
          "default": float(c_default),
          "safe_max": float(c_default) * 1.3
      }
      # Reset detektor AI agar ukuran vektor input sinkron dengan dimensi baru
      st.session_state.detector = LSTMAnomalyDetector(seq_len=SEQ_LEN)
      st.success(f"Berhasil! Metrik [{clean_key}] telah terdaftar dan aktif dalam live stream telemetri.")
      st.rerun()

  st.markdown("---")
  st.markdown("#### Daftar Custom Metrics Aktif dalam Sesi Ini:")
  if len(st.session_state.custom_metrics_registry) == 0:
    st.info("Belum ada custom metric yang dibuat. Gunakan form di atas untuk menambahkan sensor baru.")
  else:
    for k, v in st.session_state.custom_metrics_registry.items():
      st.write(f"- **{k}** ({v['label_id']} / {v['unit']}) -> Grup: {v['group']}")

# --- REFRESH TRIGGER ---
if auto_refresh:
  time.sleep(refresh_rate)
  st.rerun()
