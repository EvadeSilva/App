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

def generar_plan_entrenamiento(objetivo):
    planes = {
        "Perder grasa": [
            "Lunes: 30 min cardio moderado + core (abdominales) 🏃‍♂️",
            "Miércoles: Circuito HIIT 20-30 min 💦",
            "Viernes: Fuerza tren superior (pesas o calistenia) 💪",
            "Sábado: Cardio ligero + movilidad 🧘‍♂️"
        ],
        "Ganar músculo": [
            "Lunes: Fuerza tren superior (pesas) 💪",
            "Martes: Fuerza tren inferior (sentadillas, peso muerto) 🦵",
            "Jueves: Fullbody + core",
            "Sábado: Fuerza aislada o técnica"
        ],
        "Mantenerme en forma": [
            "Lunes: Cardio 30 min + movilidad",
            "Miércoles: Fuerza cuerpo completo",
            "Viernes: Funcional + estiramientos"
        ],
        "Mejorar resistencia": [
            "Lunes: Cardio largo (45+ min) 🏃‍♀️",
            "Miércoles: Intervalos + movilidad",
            "Viernes: Cardio progresivo + técnica",
            "Domingo: Caminata larga o ciclismo"
        ]
    }
    return planes.get(objetivo, ["Personaliza según tus preferencias y disponibilidad."])

def generar_recomendaciones_dieta(objetivo):
    if objetivo == "Perder grasa":
        return [
            "Evita azúcares refinados y ultraprocesados",
            "Consume proteínas magras (pollo, pescado, huevos)",
            "Aumenta verduras y fibra",
            "Bebe agua frecuentemente"
        ]
    elif objetivo == "Ganar músculo":
        return [
            "Incrementa ingesta calórica con proteína de calidad",
            "Come cada 3-4 horas",
            "Incorpora batidos post-entrenamiento si es necesario",
            "Incluye carbohidratos complejos"
        ]
    else:
        return [
            "Alimentación equilibrada",
            "Variedad de grupos alimenticios",
            "Evita excesos y mantén hidratación constante"
        ]

# --- GENERAR PLAN ---
if st.button("📋 Generar mi plan"):
    imc, clasificacion = calcular_imc(peso, altura)
    plan_entrenamiento = generar_plan_entrenamiento(objetivo)
    plan_dieta = generar_recomendaciones_dieta(objetivo)

    st.subheader("📊 Resumen de tu estado")
    st.write(f"**Edad:** {edad} años | **Peso:** {peso} kg | **Altura:** {altura} cm")
    st.write(f"**IMC:** {imc:.1f} ({clasificacion})")
    st.caption("El IMC (Índice de Masa Corporal) es una estimación del nivel de masa corporal. No aplica igual para todos los casos.")
    st.write(f"**Nivel de actividad:** {nivel}")
    if condiciones:
        st.write(f"**Condiciones de salud:** {condiciones}")

    # PLAN DETALLADO
    st.subheader("🏃‍♀️ Plan de entrenamiento semanal")
    for dia in plan_entrenamiento:
        st.markdown(f"- {dia}")

    st.subheader("🍎 Recomendaciones de alimentación")
    for item in plan_dieta:
        st.markdown(f"- {item}")

    if alimentos:
        st.write(f"**Preferencias alimentarias a tener en cuenta:** {alimentos}")

    st.subheader("📝 Recomendaciones generales")
    st.markdown("- Hidratación diaria: 2-3 litros de agua")
    st.markdown("- Sueño: 7-8 horas por noche")
    st.markdown("- Escucha a tu cuerpo y ajusta la rutina si es necesario")
    st.markdown("- Consulta con profesionales ante molestias físicas o dudas médicas")

    # GENERAR PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Plan personalizado de fitness", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Edad: {edad} | Peso: {peso} kg | Altura: {altura} cm | IMC: {imc:.1f} ({clasificacion})", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Objetivo: {objetivo} | Nivel de actividad: {nivel}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Entrenamiento sugerido:", ln=True)
    pdf.set_font("Arial", size=11)
    for line in plan_entrenamiento:
        pdf.cell(200, 8, txt=f"- {line}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Alimentación recomendada:", ln=True)
    pdf.set_font("Arial", size=11)
    for line in plan_dieta:
        pdf.cell(200, 8, txt=f"- {line}", ln=True)
    if alimentos:
        pdf.ln(5)
        pdf.cell(200, 8, txt=f"Preferencias alimentarias: {alimentos}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Recomendaciones generales:", ln=True)
    pdf.set_font("Arial", size=11)
    recomendaciones = [
        "Hidrátate con 2-3 litros de agua al día",
        "Duerme 7-8 horas cada noche",
        "Escucha a tu cuerpo y descansa si lo necesitas",
        "Consulta a especialistas si presentas molestias"
    ]
    for r in recomendaciones:
        pdf.cell(200, 8, txt=f"- {r}", ln=True)

    nombre_archivo = "plan_fitness.pdf"
    pdf.output(nombre_archivo)
    with open(nombre_archivo, "rb") as file:
        st.download_button("📥 Descargar plan en PDF", file, file_name=nombre_archivo)
    os.remove(nombre_archivo)
