import streamlit as st
from datetime import date

st.set_page_config(page_title="Fitness Plan Generator", layout="centered")

st.title("🏋️‍♂️ Fitness Plan Generator")
st.markdown("Responde algunas preguntas para obtener un plan personalizado de entrenamiento y alimentación.")

# --- ESTADO ACTUAL ---
st.header("1. Tu estado actual")

col1, col2 = st.columns(2)
with col1:
    edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, step=0.5)
with col2:
    altura = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, step=0.5)
    nivel = st.selectbox("Nivel de actividad física", ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"])

condiciones = st.text_area("¿Tienes alguna condición de salud o lesión a considerar?", placeholder="Ejemplo: asma, rodilla operada...")

# --- OBJETIVOS ---
st.header("2. Tus objetivos")
objetivo = st.selectbox("¿Cuál es tu objetivo principal?", ["Perder grasa", "Ganar músculo", "Mantenerme en forma", "Mejorar resistencia", "Otro"])
tiempo = st.selectbox("¿Cuántos días puedes entrenar a la semana?", ["1-2 días", "3-4 días", "5 o más días"])
tipo_entrenamiento = st.multiselect("¿Qué tipo de entrenamiento prefieres?", ["Cardio", "Fuerza", "HIIT", "Yoga / Movilidad", "Funcional"])
alimentos = st.text_area("¿Tienes alguna preferencia o restricción alimentaria?", placeholder="Ejemplo: vegetariano, sin gluten...")

# --- GENERAR PLAN ---
if st.button("📋 Generar mi plan"):
    imc = peso / ((altura / 100) ** 2)

    st.subheader("📊 Resumen de tu estado")
    st.write(f"**Edad:** {edad} años | **Peso:** {peso} kg | **Altura:** {altura} cm | **IMC:** {imc:.1f}")
    st.write(f"**Nivel de actividad:** {nivel}")
    if condiciones:
        st.write(f"**Condiciones de salud:** {condiciones}")

    # PLAN DE ENTRENAMIENTO
    st.subheader("🏃‍♀️ Plan de entrenamiento sugerido")
    if objetivo == "Perder grasa":
        st.markdown("- 3-4 sesiones de cardio semanales (30-45 min)")
        st.markdown("- 2 sesiones de fuerza para mantener masa muscular")
        st.markdown("- HIIT opcional 1-2 veces")
    elif objetivo == "Ganar músculo":
        st.markdown("- 3-5 sesiones de fuerza (enfocadas en ejercicios compuestos)")
        st.markdown("- Cardio ligero 1-2 veces por semana")
    elif objetivo == "Mantenerme en forma":
        st.markdown("- Rutina mixta: 2 cardio, 2 fuerza, 1 movilidad")
    elif objetivo == "Mejorar resistencia":
        st.markdown("- Cardio 4-5 veces por semana, progresivo")
        st.markdown("- 1-2 sesiones de fuerza de soporte")
    else:
        st.markdown("- Plan mixto adaptado a tus preferencias")

    # PLAN DE DIETA
    st.subheader("🍎 Recomendaciones de alimentación")
    if objetivo == "Perder grasa":
        st.markdown("- Déficit calórico ligero y sostenido")
        st.markdown("- Alto consumo de proteína magra y vegetales")
    elif objetivo == "Ganar músculo":
        st.markdown("- Superávit calórico controlado con buena proteína")
        st.markdown("- 4-5 comidas diarias bien distribuidas")
    else:
        st.markdown("- Alimentación balanceada con variedad y moderación")

    if alimentos:
        st.write(f"**Preferencias alimentarias:** {alimentos}")

    # RECOMENDACIONES FINALES
    st.subheader("📝 Recomendaciones finales")
    st.markdown("- Hidrátate bien (2-3 L de agua diarios)")
    st.markdown("- Duerme 7-8 horas cada noche")
    st.markdown("- Ajusta el plan según tus sensaciones y progreso")
    st.markdown("- Consulta a un profesional antes de cambios importantes")
