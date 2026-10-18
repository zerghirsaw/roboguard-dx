# RoboGuard DX // Enterprise Diagnostic Terminal & Intelligent Industry Co-pilot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://roboguard-dx-dcwmz85en4n63ycqgyukfu.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> **Live Demo App:** [Try RoboGuard DX Live Here](https://roboguard-dx-dcwmz85en4n63ycqgyukfu.streamlit.app/)

---

## Overview
**RoboGuard DX** is an AI-powered smart industrial diagnostic terminal designed to monitor, detect, and intervene in factory machine health in real-time. Inspired by professional automotive diagnostic standards (such as ECU standards and *Freeze Frame*), the system bridges multi-point telemetry data with artificial intelligence (*LSTM Autoencoder*) to minimize downtime and Mean Time To Repair (MTTR).

---

## Core Features

1. **Live Telemetry & Custom Metric Builder**
   - Real-time monitoring across subsystems (Thermal, Kinematic, Mechanical, Hydraulic, Electrical).
   - Instant custom sensor addition via GUI with automatic vector dimension adjustment.

2. **Universal Active Testing**
   - Direct intervention panel for technicians (controlling Cooling Pump, Pressure Relief, RPM Limiter).
   - Real-time write-back that interactively dampens sensor values and oscilloscope charts without triggering false-positive anomaly alarms.

3. **LSTM Autoencoder AI Engine**
   - Multivariate sequential analysis using Mean Squared Error (MSE) reconstruction for early anomaly deviation detection.

4. **ECU Freeze Frame (Black Box Memory)**
   - Automatic 10-second flight recorder capturing data when a critical anomaly is detected, complete with Diagnostic Trouble Codes (DTC) and repair guidelines.

---

## Local Installation & Running

If you wish to run this project locally on your machine:

```bash
# 1. Clone repository
git clone [https://github.com/zerghirsaw/roboguard-dx.git](https://github.com/zerghirsaw/roboguard-dx.git)
cd roboguard-dx

# 2. Create and activate a virtual environment (Optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit application
streamlit run app.py

Project Structure

    app.py — Main entry point for the Streamlit user interface.

    anomaly_detector.py — AI engine based on LSTM Autoencoder & anomaly cooldown management.

    sensor_simulator.py — Multi-point telemetry data generator & active testing handler.

    stream_receiver.py — Multi-protocol stream data ingestion handler.

    requirements.txt — Lightweight dependencies list (streamlit, pandas, numpy, altair).

License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the LICENSE file for details.

Developed by Muhammad Rifat Qolby Almusawa

Built for Intelligent Industry Solutions.
