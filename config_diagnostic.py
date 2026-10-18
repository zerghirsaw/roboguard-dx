# config_diagnostic.py

"""
Konfigurasi Pustaka Deskripsi Diagnostik (Root Cause Map)
Modul ini berisi pemetaan standar industri untuk isolasi dimensi anomali.
Developer atau ahli domain (mekanik/insinyur) dapat melakukan ekspansi matriks 
diagnostik ini tanpa perlu melakukan refactoring pada logika inti deteksi LSTM.
"""

ROOT_CAUSE_MAP = {
    # --- DIMENSI KINEMATIK & MEKANIK ---
    "Vibration": {
        "desc": (
            "Fluktuasi amplitudo getaran mekanis tingkat tinggi yang melampaui"
            " toleransi harmonik pada poros transmisi atau struktur dudukan."
        ),
        "cause": (
            "1. Degradasi material pada bantalan (journal/ball bearing).\n2."
            " Misalignment poros (angular atau parallel misalignment).\n3."
            " Resonansi struktural akibat kegagalan isolator (mounting pad).\n4."
            " Asimetri massa pada rotor yang memicu gaya sentrifugal tidak"
            " seimbang."
        ),
    },
    "vib_axial": {
        "desc": (
            "Amplitudo getaran arah aksial melampaui batas toleransi normal."
        ),
        "cause": (
            "1. Misalignment (ketidaksejajaran) poros vertikal atau"
            " horizontal.\n2. Kelonggaran baut jangkar fondasi atau dudukan"
            " mesin.\n3. Beban dorong aksial (*thrust load*) berlebih pada"
            " sudu atau roda gigi."
        ),
    },
    "vib_radial": {
        "desc": "Peningkatan getaran radial pada rotor atau selubung mesin.",
        "cause": (
            "1. Ketidakseimbangan massa (*mass unbalance*) pada komponen"
            " berputar.\n2. Keausan pada roda gigi atau selongsong"
            " kopling.\n3. Eksentrisitas poros akibat kelelahan mekanis."
        ),
    },
    "RPM": {
        "desc": (
            "Fluktuasi kecepatan sudut (angular velocity) yang menyimpang dari"
            " pita toleransi regulasi sistem kontrol loop tertutup"
            " (closed-loop)."
        ),
        "cause": (
            "1. Distorsi atau kehilangan sinyal pada rotary encoder / sensor"
            " Hall.\n2. Kesalahan kalkulasi parameter PID pada Variable Frequency"
            " Drive (VFD).\n3. Selip pada transmisi mekanis (belt/clutch"
            " slippage).\n4. Kejut beban (load shock) seketika yang melampaui"
            " batas desain torsi maksimal."
        ),
    },
    "rpm_spindle": {
        "desc": "Deviasi kecepatan sudut pada poros utama penggerak (RPM Drop).",
        "cause": (
            "1. Beban mekanis berlebih pada mata potong atau beban"
            " kerja.\n2. Slip kopling transmisi utama.\n3. Penurunan suplai"
            " torsi dari inverter VFD."
        ),
    },
    "rpm_aux": {
        "desc": (
            "Ketidakstabilan putaran pada motor penggerak pembantu (Auxiliary"
            " RPM Fluctuation)."
        ),
        "cause": (
            "1. Fluktuasi tegangan pada jalur bantu DC.\n2. Hambatan mekanis"
            " pada transmisi sekunder.\n3. Degradasi motor penggerak bantu."
        ),
    },
    "Torque": {
        "desc": (
            "Anomali pada gaya puntir (twisting force) poros penggerak yang"
            " tidak proporsional dengan output kecepatan putaran motor."
        ),
        "cause": (
            "1. Peningkatan gesekan statis (stiction) akibat kegagalan"
            " pelumasan.\n2. Kelelahan torsional pada material poros utama"
            " (driveshaft fatigue).\n3. Pembebanan eksternal (overload) yang"
            " melebihi kapasitas desain mekanis.\n4. Malfungsi pada sistem"
            " kopling fluida (fluid coupling) atau konverter torsi."
        ),
    },
    # --- DIMENSI TERMAL & FLUIDA ---
    "Temperature": {
        "desc": (
            "Ekskalasi gradien termal abnormal pada area stator, blok gearbox,"
            " atau sirkuit fluida yang berisiko memicu degradasi metalurgi."
        ),
        "cause": (
            "1. Penurunan viskositas atau kehabisan agen pelumas (lubricant"
            " starvation).\n2. Malfungsi sirkulasi cairan pendingin (coolant pump"
            " failure).\n3. Gesekan berlebih akibat keausan toleransi celah"
            " (clearance wear).\n4. Disipasi panas yang terhambat oleh"
            " penumpukan residu/debris eksternal."
        ),
    },
    "temp_core": {
        "desc": (
            "Lonjakan suhu termal inti mesin melebihi batas operasional aman"
            " (Thermal Overload)."
        ),
        "cause": (
            "1. Friksi gesek internal tinggi akibat beban berlebih.\n2."
            " Sirkulasi pendingin primer terhambat.\n3. Hambatan hambatan"
            " termal pada isolasi lilitan."
        ),
    },
    "temp_bearing": {
        "desc": (
            "Peningkatan temperatur pada komponen bantalan poros (Bearing"
            " Heating)."
        ),
        "cause": (
            "1. Keausan sangkar bantalan mekanis.\n2. Kekurangan suplai gemuk"
            " pelumas (*grease*).\n3. Kontaminasi partikel asing pada rumah"
            " bantalan."
        ),
    },
    "temp_ambient": {
        "desc": (
            "Peningkatan suhu lingkungan sekitar kabin kontrol dan unit kerja."
        ),
        "cause": (
            "1. Sirkulasi ventilasi ruang mesin terhambat.\n2. Kegagalan kipas"
            " buang (*exhaust fan*).\n3. Paparan sumber panas eksternal yang"
            " berdekatan."
        ),
    },
    "Pressure": {
        "desc": (
            "Penurunan kompresi statis atau lonjakan tekanan hidro-pneumatik"
            " dinamis yang mengganggu stabilitas aktuasi silinder dan sistem"
            " perpipaan."
        ),
        "cause": (
            "1. Kegagalan integritas segel mekanis (blown O-rings atau"
            " gaskets).\n2. Malfungsi atau sumbatan pada katup proporsional"
            " (stuck valve).\n3. Efek kavitasi akibat fluktuasi tekanan ekstrem"
            " pada jalur filtrasi.\n4. Kelelahan material (material fatigue)"
            " pada diafragma pompa utama."
        ),
    },
    "pressure_inlet": {
        "desc": (
            "Penurunan tekanan suplai fluida pada jalur masuk (Inlet Drop)."
        ),
        "cause": (
            "1. Penyumbatan pada filter saringan utama.\n2. Kavitasi pada"
            " pompa hidrolik suplai.\n3. Penurunan tinggi tekan reservoir"
            " fluida."
        ),
    },
    "pressure_outlet": {
        "desc": (
            "Penurunan tekanan kompresi pada jalur keluar (Outlet Collapse)."
        ),
        "cause": (
            "1. Kebocoran pada katup seal silinder hidrolik.\n2. Bypass katup"
            " relief yang aus atau terbuka permanen.\n3. Resistensi hilir"
            " sistem yang tidak mencukupi."
        ),
    },
    "FlowRate": {
        "desc": (
            "Deviasi drastis pada volume aliran (liter per menit) cairan"
            " pendingin, bahan bakar, atau fluida hidrolik melewati sirkuit"
            " perpipaan."
        ),
        "cause": (
            "1. Blokade parsial pada filter fluida atau saringan masuk"
            " (suction strainer).\n2. Kebocoran eksternal/internal pada jalur"
            " distribusi utama.\n3. Kerusakan impeler pada pompa sentrifugal.\n4."
            " Viskositas fluida yang meningkat tajam akibat kontaminasi atau"
            " suhu ekstrem."
        ),
    },
    # --- DIMENSI ELEKTRIKAL & AKUSTIK ---
    "Current": {
        "desc": (
            "Deviasi profil konsumsi daya listrik (lonjakan ampere) yang"
            " mengindikasikan ketidakseimbangan beban kerja motor atau"
            " aktuator."
        ),
        "cause": (
            "1. Hubungan pendek antar lilitan stator (shorted stator"
            " coils).\n2. Degradasi ketahanan insulasi kabel (insulation"
            " breakdown).\n3. Ketidakseimbangan fasa (phase imbalance) dari"
            " suplai daya utama.\n4. Resistensi mekanis ekstrem yang memaksa"
            " motor menarik arus puncak secara kontinu (overload)."
        ),
    },
    "current_draw": {
        "desc": (
            "Lonjakan tarikan arus listrik motor di atas beban nominal"
            " (Overcurrent Draw)."
        ),
        "cause": (
            "1. Tahanan mekanis yang sangat berat pada beban kerja.\n2."
            " Korsleting parsial pada lilitan stator motor.\n3. Tegangan suplai"
            " drop yang memicu peningkatan penarikan arus."
        ),
    },
    "Voltage": {
        "desc": (
            "Penurunan tegangan (voltage drop) atau lonjakan (surge) di luar"
            " toleransi yang mengganggu stabilitas suplai daya ke unit"
            " kontrol elektronik (ECU) atau motor."
        ),
        "cause": (
            "1. Kegagalan sistem alternator atau generator utama.\n2."
            " Peningkatan resistansi kontak pada terminal akibat"
            " oksidasi/korosi.\n3. Malfungsi pada modul regulator tegangan"
            " otomatis (AVR).\n4. Kegagalan sistem pentanahan (grounding fault)"
            " pada sirkuit kelistrikan."
        ),
    },
    "Acoustic": {
        "desc": (
            "Anomali spektrum emisi suara pada rentang frekuensi tinggi"
            " (ultrasonik) atau gemuruh mekanis frekuensi rendah yang"
            " mencirikan friksi destruktif."
        ),
        "cause": (
            "1. Kavitasi mikro yang meletus di dalam ruang pompa fluida.\n2."
            " Pengelupasan material (pitting/spalling) pada profil gigi"
            " persneling (gear teeth).\n3. Benturan komponen internal akibat"
            " perenggangan celah toleransi (excessive backlash).\n4. Intervensi"
            " serpihan asing (foreign object debris) di dalam sistem rotasi"
            " tertutup."
        ),
    },
    "acoustic_db": {
        "desc": (
            "Peningkatan emisi tingkat kebisingan operasional di atas batas"
            " aman akustik."
        ),
        "cause": (
            "1. Gesekan logam langsung akibat kehabisan pelumas.\n2."
            " Resonansi struktur bodi mesin akibat kelonggaran baut.\n3."
            " Turbulensi aliran fluida berkecepatan tinggi."
        ),
    },
    # --- DIMENSI KIMIAWI & STRUKTURAL (ADVANCED SENSING) ---
    "LubricantQuality": {
        "desc": (
            "Akumulasi partikel logam ferrous mikroskopis atau penurunan"
            " drastis viskositas pelumas yang terdeteksi oleh sensor kualitas"
            " oli (oil condition monitoring)."
        ),
        "cause": (
            "1. Friksi ekstrem yang mengikis permukaan logam pelindung"
            " komponen (abrasive wear).\n2. Kontaminasi air atau bahan bakar ke"
            " dalam karter oli.\n3. Oksidasi pelumas akibat paparan suhu tinggi"
            " yang terus-menerus.\n4. Interval penggantian pelumas dan filter"
            " telah jauh melampaui batas wajar."
        ),
    },
    "ExhaustGas": {
        "desc": (
            "Pergeseran rasio emisi gas buang (lonjakan NOx, CO, atau"
            " hidrokarbon yang tidak terbakar) yang mengindikasikan inefisiensi"
            " ruang bakar mesin diesel/bensin."
        ),
        "cause": (
            "1. Injektor bahan bakar tersumbat atau pola semprotan (spray"
            " pattern) terganggu.\n2. Malfungsi pada sistem resirkulasi gas"
            " buang (EGR valve tersangkut).\n3. Kegagalan kompresi pada silinder"
            " akibat keausan ring piston.\n4. Kejenuhan (saturation) pada"
            " Diesel Particulate Filter (DPF)."
        ),
    },
    "Strain": {
        "desc": (
            "Deformasi mikroskopis pada sasis struktural, rangka penyangga,"
            " atau boom hidrolik yang melampaui batas elastisitas material"
            " (yield strength)."
        ),
        "cause": (
            "1. Pengoperasian alat berat melebihi Safe Working Load (SWL).\n2."
            " Kelelahan struktural (metal fatigue) akibat beban"
            " dinamis/getaran puluhan ribu siklus.\n3. Kegagalan integritas"
            " metalurgi pada area sambungan las.\n4. Distribusi bobot yang"
            " sangat tidak merata selama manuver operasional ekstrim."
        ),
    },
}
