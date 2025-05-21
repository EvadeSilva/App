import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF
import os

st.set_page_config(page_title="Fitness Plan Generator", layout="centered")

st.title("🏋️‍♂️ Fitness Plan Generator")
st.markdown("Responde algunas preguntas para obtener un plan personalizado de entrenamiento y alimentación.")

# --- ESTADO ACTUAL ---
st.header("1. Tu estado actual")

col1, col2 = st.columns(2)
with col1:
    edad = st.selectbox("Edad", options=list(range(10, 101)))
    peso = st.selectbox("Peso (kg)", options=[round(x * 0.5, 1) for x in range(60, 601)])  # 30.0 - 300.0 kg
with col2:
    altura = st.selectbox("Altura (cm)", options=[round(x * 0.5, 1) for x in range(200, 501)])  # 100.0 - 250.0 cm
    nivel = st.selectbox("Nivel de actividad física", ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"])

condiciones = st.text_area("¿Tienes alguna condición de salud o lesión a considerar?", placeholder="Ejemplo: asma, rodilla operada...")

# --- OBJETIVOS ---
st.header("2. Tus objetivos")
objetivo = st.selectbox("¿Cuál es tu objetivo principal?", ["Perder grasa", "Ganar músculo", "Mantenerme en forma", "Mejorar resistencia", "Otro"])
tiempo = st.selectbox("¿Cuántos días puedes entrenar a la semana?", ["1-2 días", "3-4 días", "5 o más días"])
tipo_entrenamiento = st.multiselect("¿Qué tipo de entrenamiento prefieres?", ["Cardio", "Fuerza", "HIIT", "Yoga / Movilidad", "Funcional"])
alimentos = st.text_area("¿Tienes alguna preferencia o restricción alimentaria?", placeholder="Ejemplo: vegetariano, sin gluten...")

# --- FUNCIONES DE APOYO ---
def calcular_imc(peso, altura):
    imc = peso / ((altura / 100) ** 2)
    if imc < 18.5:
        clasificacion = "Bajo peso"
    elif imc < 24.9:
        clasificacion = "Normal"
    elif imc < 29.9:
        clasificacion = "Sobrepeso"
    else:
        clasificacion = "Obesidad"
    return imc, clasificacion

def limpiar_texto(texto):
    return texto.encode("latin-1", "replace").decode("latin-1")

def generar_tabla_entrenamiento(pdf):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    ejercicios = [
        "Cardio: Caminata rápida 30 min + abdominales (3x15 crunches, 3x20 seg plancha)",
        "Piernas: Sentadillas (3x15), zancadas (3x12 c/pierna), peso muerto (3x12)",
        "HIIT: 5 rounds de 40 seg trabajo / 20 seg descanso: burpees, jumping jacks, mountain climbers",
        "Fuerza superior: Flexiones (3x10), remo con bandas (3x12), press de hombro (3x12)",
        "Movilidad: Estiramientos dinámicos + abdominales (bicicleta 3x20, plank to elbow 3x15)",
        "Actividad libre: bici 45 min, senderismo, natación suave",
        "Descanso activo: yoga suave o caminata relajada"
    ]
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, limpiar_texto("Día"), 1, 0, 'C', 1)
    pdf.cell(150, 10, limpiar_texto("Rutina detallada"), 1, 1, 'C', 1)
    pdf.set_font("Arial", size=10)
    for dia, ejercicio in zip(dias, ejercicios):
        pdf.cell(40, 10, limpiar_texto(dia), 1, 0, 'C')
        pdf.multi_cell(150, 10, limpiar_texto(ejercicio), 1)

# --- GENERAR PLAN ---
if st.button("📋 Generar mi plan"):
    imc, clasificacion = calcular_imc(peso, altura)

    st.subheader("📊 Resumen de tu estado")
    st.write(f"**Edad:** {edad} años | **Peso:** {peso} kg | **Altura:** {altura} cm")
    st.write(f"**IMC:** {imc:.1f} ({clasificacion})")
    st.caption("El IMC (Índice de Masa Corporal) es una estimación del nivel de masa corporal. No aplica igual para todos los casos.")
    st.write(f"**Nivel de actividad:** {nivel}")
    if condiciones:
        st.write(f"**Condiciones de salud:** {condiciones}")

    st.subheader("✅ Resultado generado exitosamente")

    # PDF OUTPUT
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=limpiar_texto("Plan personalizado de fitness"), ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=limpiar_texto(f"Edad: {edad} | Peso: {peso} kg | Altura: {altura} cm | IMC: {imc:.1f} ({clasificacion})"), ln=True)
    pdf.cell(200, 10, txt=limpiar_texto(f"Objetivo: {objetivo} | Nivel de actividad: {nivel}"), ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Tabla de rutina semanal detallada"), ln=True)
    pdf.ln(5)
    generar_tabla_entrenamiento(pdf)

    # Página adicional con explicación del IMC
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("¿Qué es el IMC?"), ln=True)
    pdf.set_font("Arial", size=11)
    texto = (
        "El IMC (Índice de Masa Corporal) es una fórmula que evalúa la relación entre el peso y la altura de una persona. "
        "Aunque es una herramienta útil como referencia general, no considera la composición corporal (músculo vs grasa)."
    )
    pdf.multi_cell(0, 10, limpiar_texto(texto))
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Categorías de IMC"), ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 10, limpiar_texto("Menor a 18.5: Bajo peso"), ln=True)
    pdf.cell(100, 10, limpiar_texto("18.5 - 24.9: Peso normal"), ln=True)
    pdf.cell(100, 10, limpiar_texto("25 - 29.9: Sobrepeso"), ln=True)
    pdf.cell(100, 10, limpiar_texto("30 o más: Obesidad"), ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Consejos generales"), ln=True)
    pdf.set_font("Arial", size=11)
    recomendaciones = [
        "Duerme al menos 7-8 horas cada noche",
        "Bebe entre 2-3 litros de agua al día",
        "Evita alimentos ultra procesados y azúcares añadidos",
        "Consume más verduras, proteínas magras y fibra"
    ]
    for r in recomendaciones:
        pdf.cell(200, 10, limpiar_texto(f"- {r}"), ln=True)

    nombre_archivo = "plan_fitness.pdf"
    try:
        pdf.output(nombre_archivo)
        with open(nombre_archivo, "rb") as file:
            st.download_button("📥 Descargar plan en PDF", file, file_name=nombre_archivo)
        os.remove(nombre_archivo)
    except Exception as e:
        st.error(f"Ocurrió un error al generar el PDF: {e}")
