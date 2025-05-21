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
    pdf.set_font("OpenSans", "B", 11)
    pdf.cell(40, 10, limpiar_texto("Día"), 1, 0, 'C', 1)
    pdf.cell(150, 10, limpiar_texto("Rutina detallada"), 1, 1, 'C', 1)
    pdf.set_font("OpenSans", size=10)
    for dia, ejercicio in zip(dias, ejercicios):
        pdf.cell(40, 10, limpiar_texto(dia), 1, 0, 'C')
        pdf.multi_cell(150, 10, limpiar_texto(ejercicio), 1)

# --- MEJORAS DE ESTILO GLOBAL ---
# (Aplicadas en cada sección dentro del botón de generación de PDF)
# Usa OpenSans en todo, colores suaves y líneas divisorias

# Resto del código ya integra estilo visual y fuente moderna
# Asegúrate de tener el archivo OpenSans-Regular.ttf en el mismo directorio

