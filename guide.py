# guide.py - Interactive Operational User Manual for RoboGuard DX
import streamlit as st


def render_user_guide(lang="Indonesian"):
  if lang == "Indonesian":
    st.markdown("### BUKU PANDUAN OPERASIONAL & ARSITEKTUR SISTEM ENTERPRISE")
    st.markdown(
        "Dokumentasi teknis komprehensif tingkat lanjut untuk pengoperasian sistem diagnostik"
        " industri cerdas, bedah arsitektur kecerdasan buatan, protokol komunikasi edge,"
        " serta metodologi pemeliharaan prediktif (*Predictive Maintenance*) berbasis data."
    )

    with st.expander(
        "1. Pengantar & Filosofi Desain Sistem (System Philosophy & Overview)"
    ):
      st.markdown("""
            * **Latar Belakang Industri & Kompleksitas Data:**
              * Pabrik modern dan armada alat berat menghasilkan aliran data masif setiap detiknya dari berbagai sensor suhu, getaran, tekanan, dan kelistrikan. Tantangan utamanya bukanlah kekurangan informasi, melainkan bagaimana menyaring kebisingan (*noise*) data dan mengetahui tindakan preventif secara instan sebelum kegagalan katastrofik terjadi.
            * **Inspirasi Profesional Ala Hino DX3 & SCADA Enterprise:**
              * RoboGuard DX dirancang mengadopsi standar antarmuka alat diagnostik ECU kendaraan berat profesional (seperti Hino DX3) yang dipadukan dengan ketangguhan platform SCADA industri. Tampilan antarmuka mengusung tema monokrom kontras tinggi untuk memastikan keterbacaan optimal bagi teknisi di ruang kontrol maupun di lapangan dalam kondisi pencahayaan apapun.
            * **Cakupan Modul Fungsional Utama:**
              * *Live Telemetry & Oscilloscope (Tab 1):* Pemantauan waktu nyata multi-titik dan tren osiloskop presisi desimal.
              * *Active Testing (Tab 2):* Intervensi kendali aktuator tertutup (*closed-loop write-back*).
              * *Freeze Frames (Tab 3):* Perekaman data hitam (*black-box*) pasca-insiden anomali.
              * *User Manual (Tab 4):* Panduan teknis interaktif yang sedang diakses.
              * *Custom Metric Builder (Tab 5):* Pembangun sensor dan aliran data dinamis langsung via GUI.
            """)

    with st.expander(
        "2. Panduan Operasional & Navigasi Dasbor (Operational Navigation)"
    ):
      st.markdown("""
            * **Pemilihan Sumber Aliran Data (*Ingestion Source* pada Sidebar):**
              * *Simulation Mode (Internal Generator):* Digunakan untuk simulasi dan pelatihan. Anda dapat memilih berbagai skenario kegagalan industri (seperti *Thermal Overheat*, *Hydraulic Pressure Drop*, *Overcurrent Spike*, *Bearing Vibration*, dan *RPM Drop*) untuk memicu anomali secara terkendali.
              * *Real Stream Mode (Multi-Protocol Gateway):* Digunakan untuk integrasi fisik ke perangkat keras pabrik menggunakan protokol standar industri seperti *JSON Web Feed*, *Arduino/ESP32 USB Serial*, atau *Industrial PLC Modbus TCP*.
            * **Navigasi Tab 1 (Live Telemetry & High-Precision Oscilloscope):**
              * Menyajikan kartu metrik untuk seluruh sub-sistem (Thermal, Kinematic, Mechanical, Hydraulic, Electrical, Acoustic, hingga Custom Sensors).
              * Grafik osiloskop merender data historis bergerak secara mulus dengan penanda waktu (*timestamp*) dan *tooltip* nilai presisi.
            * **Navigasi Tab 2 (Universal Active Testing & Actuator Override):**
              * Berfungsi sebagai panel kendali interaktif bagi teknisi untuk menguji respons fisik mesin dengan mengirimkan perintah balik (*write-back*): Mengaktifkan Pompa Pendingin Darurat, Membuka Katup Pelepas Tekanan, atau Membatasi RPM Spindle.
            * **Navigasi Tab 3 (ECU Freeze Frame & Audit Log):**
              * Secara otomatis menangkap *snapshot* data telemetri lengkap (memori hitam) saat sistem mendeteksi anomali kritis, disertai identifikasi akar masalah untuk keperluan investigasi dan audit keselamatan kerja.
            * **Navigasi Tab 5 (Dynamic Custom Metric & Stream Builder):**
              * Memungkinkan penambahan parameter sensor baru secara instan di tengah operasional. Cukup masukkan nama kunci (*key*), label dwibahasa, satuan, nilai dasar, dan grup subsistem—sistem AI dan osiloskop akan otomatis memperbarui vektor data secara *real-time*.
            """)

    with st.expander(
        "3. Bedah Inovasi Teknologi AI & Deteksi Anomali (Core AI Architecture)"
    ):
      st.markdown("""
            * **Model Deep Learning LSTM Autoencoder:**
              * Berbeda dari sistem tradisional yang hanya menggunakan batas ambang statis (*static thresholds*) yang sering memicu alarm palsu, RoboGuard DX menggunakan arsitektur *Long Short-Term Memory (LSTM) Autoencoder*. Model ini dilatih untuk memahami pola normal multivariat dari urutan sekuensial waktu (*temporal sequences*).
            * **Analisis Rekonstruksi MSE (*Mean Squared Error*):**
              * Setiap jendela data sekuensial dievaluasi oleh jaringan saraf tiruan. Jika pola data menyimpang dari perilaku normal operasional mesin, nilai error rekonstruksi (*MSE Loss*) akan melonjak melampaui batas kritis standar (< 0.03).
            * **Otomasi Isolasi Akar Masalah (*Root Cause Dimension Isolation*):**
              * Ketika anomali terdeteksi, sistem tidak hanya memberikan peringatan umum, melainkan melakukan pemetaan matriks galat (*Error Mapping Matrix*) untuk mengisolasi dimensi sensor spesifik mana yang menjadi pemicu utama kegagalan (misalnya mengarah langsung ke keausan bantalan atau penurunan tekanan inlet).
            * **Skalabilitas Vektor Dinamis (*Dynamic Tensor Resizing*):**
              * Berkat arsitektur penanganan skema terpusat, penambahan metrik melalui GUI Builder secara otomatis menyesuaikan ukuran dimensi tensor input pada model AI tanpa memerlukan pelatihan ulang (*retraining*) model dari awal.
            """)

    with st.expander(
        "4. Arsitektur Perangkat Keras Edge & Integrasi Industri (Industrial Edge IoT)"
    ):
      st.markdown("""
            * **Arsitektur Middleware Agnostik (*Hardware-Agnostic Gateway*):**
              * Sistem diposisikan sebagai *edge gateway* cerdas yang menjembatani lantai produksi pabrik dengan analitik tingkat tinggi, memastikan latensi rendah dan kedaulatan data lokal (*data privacy*).
            * **Dukungan Protokol Komunikasi Industri Multi-Pilar:**
              * *Arduino & ESP32 (Microcontroller Edge Nodes):* Menghubungkan sensor fisik eksternal (seperti sensor getaran piezoelektrik dan termokopel) melalui komunikasi serial USB dengan *baudrate* tinggi.
              * *Industrial PLC (Programmable Logic Controller):* Berkomunikasi langsung dengan perangkat otomasi pabrik skala besar menggunakan protokol standar industri **Modbus TCP** untuk membaca *holding registers* secara periodik.
              * *Automotive ECU (Electronic Control Unit):* Mendukung pembacaan bus data kendaraan berat dan mesin diesel industri.
            * **Kendali Tertutup Dua Arah (*Closed-Loop Bi-Directional Control*):**
              * Selain fungsi pemantauan pasif (*Read-Only*), arsitektur ini mendukung pengiriman sinyal eksekusi balik ke perangkat lapangan (*Write-Back Actuation*), memungkinkan intervensi otomatis seketika saat terdeteksi kondisi darurat.
            """)

    with st.expander(
        "5. Metrik Keberhasilan & Dampak Bisnis (Business Impact & ROI)"
    ):
      st.markdown("""
            * **Reduksi Waktu Perbaikan (*Mean Time To Repair - MTTR*):**
              * Dengan isolasi akar masalah otomatis dan panduan perbaikan instan, teknisi dapat memangkas waktu diagnosis dari jam menjadi hitungan menit.
            * **Pencegahan Henti Operasional (*Downtime Prevention*):**
              * Deteksi dini berbasis AI mengidentifikasi degradasi komponen jauh sebelum kerusakan total terjadi, menghemat biaya kerugian material pabrik yang masif.
            * **Efisiensi Sumber Daya & Keselamatan Kerja:**
              * Optimalisasi penggunaan energi mesin dan peningkatan keselamatan operator melalui pengawasan kondisi darurat secara proaktif.
            """)
  else:
    st.markdown("### ENTERPRISE OPERATIONAL USER MANUAL & SYSTEM ARCHITECTURE")
    st.markdown(
        "Advanced comprehensive technical documentation for operating the smart industrial"
        " diagnostic system, artificial intelligence architecture analysis, edge communication protocols,"
        " and data-driven predictive maintenance methodologies."
    )

    with st.expander(
        "1. Introduction & System Design Philosophy (System Philosophy & Overview)"
    ):
      st.markdown("""
            * **Industrial Background & Data Complexity:**
              * Modern factories and heavy machinery generate massive streams of data every second from temperature, vibration, pressure, and electrical sensors. The primary challenge is rarely a lack of information, but rather filtering data noise and knowing immediate preventive actions before catastrophic failures occur.
            * **Professional Hino DX3 & Enterprise SCADA Inspiration:**
              * RoboGuard DX is engineered by adopting the interface standards of professional heavy vehicle diagnostic tools (such as Hino DX3) combined with the robustness of industrial SCADA platforms. The user interface utilizes a high-contrast monochrome theme to ensure optimal readability for technicians in control rooms or field environments under any lighting condition.
            * **Core Functional Module Scope:**
              * *Live Telemetry & Oscilloscope (Tab 1):* Real-time multi-point monitoring and decimal-precision trend analysis.
              * *Active Testing (Tab 2):* Closed-loop actuator override and write-back control.
              * *Freeze Frames (Tab 3):* Post-incident black-box telemetry recording.
              * *User Manual (Tab 4):* Interactive technical documentation currently being accessed.
              * *Custom Metric Builder (Tab 5):* Dynamic sensor and data stream creator directly via GUI.
            """)

    with st.expander(
        "2. Operational Guide & Dashboard Navigation (Operational Navigation)"
    ):
      st.markdown("""
            * **Data Ingestion Source Selection (Sidebar):**
              * *Simulation Mode (Internal Generator):* Used for simulation and training. Select various industrial fault scenarios (such as *Thermal Overheat*, *Hydraulic Pressure Drop*, *Overcurrent Spike*, *Bearing Vibration*, and *RPM Drop*) to trigger anomalies in a controlled manner.
              * *Real Stream Mode (Multi-Protocol Gateway):* Used for physical integration into factory hardware using industry-standard protocols such as *JSON Web Feed*, *Arduino/ESP32 USB Serial*, or *Industrial PLC Modbus TCP*.
            * **Tab 1 Navigation (Live Telemetry & High-Precision Oscilloscope):**
              * Presents metric cards for all subsystems (Thermal, Kinematic, Mechanical, Hydraulic, Electrical, Acoustic, and Custom Sensors).
              * Oscilloscope charts render moving historical data smoothly with timestamps and high-precision tooltips.
            * **Tab 2 Navigation (Universal Active Testing & Actuator Override):**
              * Acts as an interactive control panel for technicians to test physical machine responses by transmitting write-back commands: Activating Emergency Cooling Pumps, Opening Pressure Relief Valves, or Limiting Spindle RPM.
            * **Tab 3 Navigation (ECU Freeze Frame & Audit Log):**
              * Automatically captures complete telemetry snapshots (black-box memory) when critical anomalies are detected, complete with root cause identification for safety investigations and technical audits.
            * **Tab 5 Navigation (Dynamic Custom Metric & Stream Builder):**
              * Enables instant addition of new sensor parameters on-the-fly during operation. Simply input key names, bilingual labels, units, baseline values, and subsystem groups—the AI engine and oscilloscope will automatically update tensor dimensions in real-time.
            """)

    with st.expander(
        "3. AI Technology Innovation & Anomaly Detection (Core AI Architecture)"
    ):
      st.markdown("""
            * **LSTM Autoencoder Deep Learning Model:**
              * Unlike traditional systems relying solely on static thresholds that frequently trigger false alarms, RoboGuard DX utilizes a *Long Short-Term Memory (LSTM) Autoencoder* architecture. This model is trained to comprehend multivariate normal patterns from temporal time-series sequences.
            * **MSE Reconstruction Analysis (Mean Squared Error):**
              * Every sequential data window is evaluated by the neural network. If data patterns deviate from normal operational machine behavior, the reconstruction error value (*MSE Loss*) spikes beyond standard critical thresholds (< 0.03).
            * **Automated Root Cause Dimension Isolation:**
              * When anomalies are detected, the system does not merely provide generic warnings; it performs an *Error Mapping Matrix* calculation to isolate which specific sensor dimension acts as the primary failure trigger (e.g., pointing directly to bearing wear or inlet pressure drops).
            * **Dynamic Tensor Scalability:**
              * Thanks to centralized schema management architecture, adding metrics via the GUI Builder automatically adjusts input tensor dimensions in the AI model without requiring model retraining from scratch.
            """)

    with st.expander(
        "4. Edge Hardware Architecture & Industrial Integration (Industrial Edge IoT)"
    ):
      st.markdown("""
            * **Hardware-Agnostic Middleware Architecture:**
              * The system is positioned as an intelligent edge gateway bridging factory production floors with high-level analytics, ensuring low latency and local data sovereignty (*data privacy*).
            * **Multi-Pillar Industrial Communication Protocol Support:**
              * *Arduino & ESP32 (Microcontroller Edge Nodes):* Connects external physical sensors (such as piezoelectric vibration sensors and thermocouples) via high-baud-rate USB serial communication.
              * *Industrial PLC (Programmable Logic Controller):* Interfaces directly with large-scale factory automation hardware using the industry-standard **Modbus TCP** protocol to poll holding registers periodically.
              * *Automotive ECU (Electronic Control Unit):* Supports reading heavy vehicle and industrial diesel engine data communication buses.
            * **Closed-Loop Bi-Directional Control:**
              * Beyond passive monitoring (*Read-Only*), this architecture supports transmitting execution signals back to field hardware (*Write-Back Actuation*), enabling automated intervention immediately upon emergency conditions.
            """)

    with st.expander(
        "5. Success Metrics & Business Impact (Business Impact & ROI)"
    ):
      st.markdown("""
            * **Mean Time To Repair (MTTR) Reduction:**
              * With automated root cause isolation and instant repair guidance, technicians slash diagnostic times from hours down to minutes.
            * **Downtime Prevention:**
              * AI-driven early detection identifies component degradation long before total failure occurs, saving massive factory material loss costs.
            * **Resource Efficiency & Workplace Safety:**
              * Optimizing machine energy usage and enhancing operator safety through proactive emergency condition monitoring.
            """)
