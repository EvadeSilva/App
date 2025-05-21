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
        "Cardio moderado + abdominales",
        "Entrenamiento de fuerza (piernas)",
        "HIIT 20 min + estiramientos",
        "Entrenamiento de fuerza (superior)",
        "Movilidad y core",
        "Actividad libre: caminata larga, yoga, bici",
        "Descanso activo o yoga"
    ]
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(95, 10, limpiar_texto("Día"), 1, 0, 'C', 1)
    pdf.cell(95, 10, limpiar_texto("Ejercicio recomendado"), 1, 1, 'C', 1)
    pdf.set_font("Arial", size=11)
    for dia, ejercicio in zip(dias, ejercicios):
        pdf.cell(95, 10, limpiar_texto(dia), 1, 0, 'C')
        pdf.cell(95, 10, limpiar_texto(ejercicio), 1, 1)

def agregar_pagina_explicativa(pdf):
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
    pdf.cell(200, 10, limpiar_texto("Tabla de rutina semanal sugerida"), ln=True)
    pdf.ln(5)
    generar_tabla_entrenamiento(pdf)
    agregar_pagina_explicativa(pdf)

    nombre_archivo = "plan_fitness.pdf"
    try:
        pdf.output(nombre_archivo)
        with open(nombre_archivo, "rb") as file:
            st.download_button("📥 Descargar plan en PDF", file, file_name=nombre_archivo)
        os.remove(nombre_archivo)
    except Exception as e:
        st.error(f"Ocurrió un error al generar el PDF: {e}")
