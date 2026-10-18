# ROBOGUARD(8) -- Industrial IoT Subsystem Manual

## NAME
**roboguard** — Deep Learning Telemetry Anomaly Detection and AI Technician Co-Pilot Daemon

## SYNOPSIS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## DESCRIPTION
**RoboGuard** is a modular, edge-capable industrial monitoring subsystem engineered for robotic spare parts manufacturing plants. It executes real-time multivariate time-series analysis on high-frequency machine telemetry using a PyTorch-backed Long Short-Term Memory (LSTM) Autoencoder. 

Upon detecting statistical reconstruction drift or temporal anomalies, the system engages an explainable AI (XAI) technician co-pilot daemon powered by local large language models (IBM Granite via Ollama) with automated industrial fallback protocols to minimize Mean Time To Repair (MTTR).

---

## ARCHITECTURE & SUBSYSTEM SPECIFICATION

The subsystem follows a strict decoupled, modular architecture residing within the workspace root:

```text
roboguard/
├── app.py                  # Control room frontend daemon (Streamlit + Altair)
├── anomaly_detector.py     # PyTorch LSTM Autoencoder & normalization pipeline
├── copilot_engine.py       # AI diagnostic connector (Ollama / IBM Granite)
├── sensor_simulator.py     # Multivariate 6D industrial telemetry simulator
└── requirements.txt        # Pinned runtime dependencies
```

### 1. Telemetry Ingestion Layer (`sensor_simulator.py`)
Generates high-frequency, multivariate industrial streams across 6 canonical feature dimensions at adjustable temporal intervals:
* **Vibration RMS (`vibration`):** Measured in $\text{mm/s}$ (Normal baseline: $1.8 \pm 0.2$).
* **Component Temperature (`temperature`):** Measured in $\text{°C}$ (Normal baseline: $50.0 \pm 1.0$).
* **Electrical Current (`current`):** Measured in $\text{Amperes}$ (Normal baseline: $2.5 \pm 0.1$).
* **Hydraulic Pressure (`pressure`):** Measured in $\text{Bar}$ (Normal baseline: $45.0 \pm 1.0$).
* **Motor Speed (`rpm`):** Measured in $\text{RPM}$ (Normal baseline: $1450.0 \pm 10.0$).
* **Acoustic Noise (`acoustic`):** Measured in $\text{dB}$ (Normal baseline: $55.0 \pm 1.0$).

### 2. Deep Learning Anomaly Detection Core (`anomaly_detector.py`)
* **Model Topology:** Unsupervised LSTM Autoencoder (`LSTMAutoencoder`) comprising an encoder LSTM cell, temporal latent state projection, and a decoder reconstruction layer.
* **Feature Normalization:** Multi-dimensional scaling vector (`scale_factors`) normalizes disparate telemetry units into a stable $[0, 1]$ numerical manifold prior to tensor conversion.
* **Inference Logic:** Evaluates sliding sequence windows of length $T = 10$. Computes Mean Squared Error (MSE) reconstruction loss:
  $$\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{t=1}^{N} \|\mathbf{x}_t - \hat{\mathbf{x}}_t\|^2$$
* **Thresholding:** Triggers an critical state interrupt flag when $\mathcal{L}_{\text{MSE}} > 0.03$.

### 3. Explainable AI & Co-Pilot Engine (`copilot_engine.py`)
* **Primary Interface:** Connects to local daemon endpoints (`http://localhost:11434/api/generate`) running **IBM Granite** (`granite3.0:3b`) with a 3-second strict timeout constraint.
* **Fail-Safe Mechanism:** Automatically switches to an enterprise rule-based fallback dictionary if local inference latency exceeds constraints or daemon offline status is detected, ensuring 100% uptime reliability during live demonstrations.

### 4. Control Room Presentation Layer (`app.py`)
* Built on **Streamlit** with responsive grid metrics (`st.metric`) and real-time multi-sensor vector visualization powered by **Altair** (`alt.Chart`), configured with horizontal timestamp axes (`labelAngle=0`) to prevent visual crowding.
* Supports runtime localization toggles (`Indonesia` / `English`).

---

## DEPENDENCIES & ENVIRONMENT SETUP

The runtime environment requires Python 3.10+ and the packages specified in `requirements.txt`:

```text
streamlit>=1.35.0
torch>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
altair>=5.0.0
requests>=2.31.0
```

To export the active environment configuration manually:
```bash
pip freeze > requirements.txt
```

---

## DEPLOYMENT & OPERATION

### Local Execution
1. Initialize virtual environment and activate shell.
2. Execute the frontend dashboard daemon:
   ```bash
   streamlit run app.py
   ```
3. Access the control room interface locally at `http://localhost:8501`.

### Production & Cloud Distribution
For cloud deployment (Hugging Face Spaces or Streamlit Community Cloud):
1. Push repository root containing `app.py`, modules, and `requirements.txt` to a remote public repository.
2. Link repository to the target cloud container runner. The runtime executes `app.py` as the entrypoint, automatically falling back to structured diagnostic protocols if hardware accelerators or local LLM daemons are absent.

## AUTHOR
RoboGuard Engineering Task Force (Intelligent Industry Track).