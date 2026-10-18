import requests


class TechnicianCoPilot:

  def __init__(self, model_name="granite4.2:3b"):
    self.model_name = model_name
    self.ollama_url = "http://localhost:11434/api/generate"

  def get_explanation(self, metrics: dict, lang: str = "Indonesia") -> dict:
    vib = metrics["vibration"]
    temp = metrics["temperature"]
    curr = metrics["current"]
    score = metrics["lstm_score"]

    prompt = f"""
        Act as an industrial AI maintenance expert. 
        Telemetry data from Servo Gearbox Station #3 shows anomaly:
        - LSTM MSE Error Score: {score}
        - Vibration: {vib} mm/s
        - Temperature: {temp} °C
        - Current: {curr} A
        
        Provide response in {lang} with:
        1. Main Diagnosis summary.
        2. Brief technical parameter analysis.
        3. 3 concrete action steps for the technician.
        Keep it professional, formal, and structured.
        """

    try:
      payload = {
          "model": self.model_name,
          "prompt": prompt,
          "stream": False,
          "options": {"temperature": 0.2},
      }
      response = requests.post(self.ollama_url, json=payload, timeout=3)

      if response.status_code == 200:
        ai_text = response.json().get("response", "")
        return {
            "summary": f"**[AI Generated via IBM Granite]**\n{ai_text}",
            "parameters": [
                f"- **Vibration ({vib} mm/s):** Anomaly detected.",
                f"- **Temperature ({temp} °C):** Thermal deviation.",
                f"- **Current ({curr} A):** Load irregularity.",
            ],
            "steps": (
                "1. **Emergency Stop:** Halt Station #3.\n2. **Inspect:**"
                " Check gearbox housing.\n3. **Resolve:** Follow AI protocol"
                " above."
            ),
        }
    except Exception:
      pass

    # Fallback Statis
    if lang == "English":
      return {
          "summary": (
              "**[Fallback Mode] Main Diagnosis:** Excessive mechanical"
              " friction detected on the Servo Gearbox (Station #3)."
          ),
          "parameters": [
              f"- **Vibration RMS ({vib} mm/s):** Exceeds normal threshold.",
              f"- **Temperature ({temp} °C):** Overheating due to friction.",
              f"- **Current Draw ({curr} A):** Motor overload.",
          ],
          "steps": (
              "1. **Emergency Stop:** Shut down power.\n2. **Inspection:** Open"
              " casing.\n3. **Repair:** Replace RG-204 Gearpack."
          ),
      }
    else:
      return {
          "summary": (
              "**[Mode Cadangan] Diagnosis Utama:** Terdeteksi gesekan"
              " mekanis berlebih pada *Gearbox Servo* (Stasiun #3)."
          ),
          "parameters": [
              (
                  f"- **Getaran RMS ({vib} mm/s):** Melampaui batas normal"
                  " operasional."
              ),
              (
                  f"- **Suhu Komponen ({temp} °C):** Panas berlebih akibat"
                  " friksi."
              ),
              (
                  f"- **Arus Listrik ({curr} A):** Motor bekerja terlalu berat."
              ),
          ],
          "steps": (
              "1. **Emergency Stop:** Matikan power.\n2. **Inspeksi:** Buka"
              " casing.\n3. **Perbaikan:** Ganti Gearpack RG-204."
          ),
      }
