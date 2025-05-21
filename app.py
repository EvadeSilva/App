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
    peso = st.selectbox("Peso (kg)", options=[round(x * 0.5, 1) for x in range(60, 601)])
with col2:
    altura = st.selectbox("Altura (cm)", options=[round(x * 0.5, 1) for x in range(200, 501)])
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
    ejercicios = []
    preferencias = tipo_entrenamiento
    for i in range(7):
        if "Fuerza" in preferencias:
            ejercicios.append("Fuerza: Sentadillas (3x15), Flexiones (3x12), Peso muerto (3x10)")
        elif "HIIT" in preferencias:
            ejercicios.append("HIIT: 5 rounds - 40s trabajo/20s descanso: burpees, jumping jacks, mountain climbers")
        elif "Yoga / Movilidad" in preferencias:
            ejercicios.append("Yoga/Movilidad: secuencia básica + estiramientos de espalda y piernas")
        elif "Funcional" in preferencias:
            ejercicios.append("Funcional: sentadilla + empuje, estocada + curl, plancha con toques (3x12 cada uno)")
        elif "Cardio" in preferencias:
            ejercicios.append("Cardio: Caminata o bicicleta 30-45 minutos a ritmo moderado")
        else:
            ejercicios.append("Rutina general: Caminata + abdominales + estiramientos")

    pdf.set_fill_color(240, 244, 255)
    pdf.set_text_color(40, 40, 40)
    pdf.set_draw_color(200, 200, 200)
    pdf.set_font("OpenSans", '', 11)
    pdf.cell(40, 10, limpiar_texto("Día"), 1, 0, 'C', 1)
    pdf.cell(150, 10, limpiar_texto("Rutina detallada"), 1, 1, 'C', 1)
    pdf.set_font("OpenSans", size=10)
    for dia, ejercicio in zip(dias, ejercicios):
        pdf.cell(40, 10, limpiar_texto(dia), 1, 0, 'C')
        pdf.multi_cell(150, 10, limpiar_texto(ejercicio), 1)

# --- MEJORAS DE ESTILO GLOBAL ---
# (Aplicadas en cada sección dentro del botón de generación de PDF)
# Usa OpenSans en todo, colores suaves y líneas divisorias

if st.button("📋 Generar plan personalizado"):
    st.subheader("📊 Resumen de tu estado")
    imc, clasificacion = calcular_imc(peso, altura)
    st.write(f"**Edad:** {edad} años | **Peso:** {peso} kg | **Altura:** {altura} cm")
    st.write(f"**IMC:** {imc:.1f} ({clasificacion})")
    st.caption("El IMC es una herramienta estimativa, no diagnóstica. Consulta a un profesional si tienes dudas.")
    st.write(f"**Nivel de actividad:** {nivel}")

    # Generación del PDF
    pdf = FPDF()
    pdf.add_font('OpenSans', '', 'OpenSans-Regular.ttf', uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('OpenSans', size=12)

    pdf.add_page()
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 51, 102)
    pdf.set_font("OpenSans", '', 22)
    pdf.ln(80)
    pdf.cell(0, 20, limpiar_texto("PLAN PERSONALIZADO DE FITNESS"), ln=True, align='C')
    pdf.set_font("OpenSans", '', 14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, limpiar_texto(f"Edad: {edad} | Objetivo: {objetivo}"), ln=True, align='C')
    pdf.cell(0, 10, limpiar_texto(f"Fecha: {date.today().strftime('%d/%m/%Y')}"), ln=True, align='C')

    pdf.add_page()
    pdf.set_font("OpenSans", '', 16)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(200, 12, txt=limpiar_texto("Plan personalizado de fitness"), ln=True, align="C", fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("OpenSans", size=12)
    pdf.cell(200, 10, txt=limpiar_texto(f"Edad: {edad} | Peso: {peso} kg | Altura: {altura} cm | IMC: {imc:.1f} ({clasificacion})"), ln=True)
    pdf.cell(200, 10, txt=limpiar_texto(f"Objetivo: {objetivo} | Nivel de actividad: {nivel}"), ln=True)
    pdf.ln(10)

    pdf.set_draw_color(180, 180, 180)
    pdf.set_fill_color(50, 90, 160)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("OpenSans", "B", 12)
    pdf.cell(200, 10, limpiar_texto("🔥 Tu rutina semanal"), ln=True, fill=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    generar_tabla_entrenamiento(pdf)

    nombre_archivo = "plan_fitness.pdf"
    try:
        pdf.output(nombre_archivo)
        with open(nombre_archivo, "rb") as file:
            st.download_button("📥 Descargar plan en PDF", file, file_name=nombre_archivo)
        os.remove(nombre_archivo)
    except Exception as e:
        st.error(f"Ocurrió un error al generar el PDF: {e}")

# Resto del código ya integra estilo visual y fuente moderna
# Asegúrate de tener el archivo OpenSans-Regular.ttf en el mismo directorio
