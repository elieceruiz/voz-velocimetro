import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Velocímetro con voz", page_icon="🛴", layout="centered")

st.title("🛴 Velocímetro con voz – Penélope")
st.write("Esta App usa el GPS del teléfono y te habla cada 2 segundos con la velocidad actual.")

st.session_state.setdefault("running", False)

col1, col2 = st.columns(2)
if col1.button("▶️ Iniciar"):
    st.session_state.running = True
if col2.button("⏹️ Detener"):
    st.session_state.running = False

if st.session_state.running:
    components.html("""
    <script>
    let watchId = null;
    let synth = window.speechSynthesis;
    let lastSpokenTime = 0;
    let currentSpeed = 0;

    function speak(text) {
        if (!synth.speaking) {
            let utter = new SpeechSynthesisUtterance(text);
            utter.rate = 1;
            utter.pitch = 1;
            synth.speak(utter);
        }
    }

    function startTracking() {
        if (navigator.geolocation) {
            watchId = navigator.geolocation.watchPosition(
                function(pos) {
                    let speed_m_s = pos.coords.speed;
                    if (speed_m_s === null) {
                        document.getElementById("velocidad").innerText = "Sin señal GPS";
                        return;
                    }
                    currentSpeed = (speed_m_s * 3.6).toFixed(1);
                    document.getElementById("velocidad").innerText = currentSpeed + " km/h";
                },
                function(err) {
                    speak("Error al obtener la ubicación");
                },
                {
                    enableHighAccuracy: true,
                    maximumAge: 1000
                }
            );
        } else {
            speak("Tu dispositivo no soporta GPS");
        }
    }

    function announceSpeed() {
        let now = Date.now();
        if (now - lastSpokenTime >= 2000) {  // cada 2 segundos
            lastSpokenTime = now;
            if (currentSpeed === 0 || isNaN(currentSpeed)) {
                speak("Velocidad actual cero kilómetros por hora");
            } else {
                speak("Velocidad actual " + currentSpeed + " kilómetros por hora");
            }
        }
    }

    startTracking();
    setInterval(announceSpeed, 1000); // revisa cada segundo si toca hablar
    </script>

    <h3 id="velocidad" style="font-size:48px;text-align:center;margin-top:30px;">0 km/h</h3>
    """, height=400)

else:
    st.info("Presiona **Iniciar** para comenzar la lectura de velocidad con voz en tiempo real.")
