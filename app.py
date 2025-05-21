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

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 51, 102)
    pdf.set_font("Arial", 'B', 22)
    pdf.ln(80)
    pdf.cell(0, 20, limpiar_texto("PLAN PERSONALIZADO DE FITNESS"), ln=True, align='C')
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, limpiar_texto(f"Generado para edad {edad} años | Objetivo: {objetivo}"), ln=True, align='C')
    pdf.cell(0, 10, limpiar_texto(f"Fecha: {date.today().strftime('%d/%m/%Y')}"), ln=True, align='C')

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(200, 12, txt=limpiar_texto("Plan personalizado de fitness"), ln=True, align="C", fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=limpiar_texto(f"Edad: {edad} | Peso: {peso} kg | Altura: {altura} cm | IMC: {imc:.1f} ({clasificacion})"), ln=True)
    pdf.cell(200, 10, txt=limpiar_texto(f"Objetivo: {objetivo} | Nivel de actividad: {nivel}"), ln=True)
    pdf.ln(10)

    pdf.set_draw_color(180, 180, 180)
    pdf.set_fill_color(50, 90, 160)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Tabla de rutina semanal detallada"), ln=True, fill=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    generar_tabla_entrenamiento(pdf)

    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Requerimientos calóricos estimados"), ln=True)
    pdf.set_font("Arial", size=11)
    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    factores = {"Sedentario": 1.2, "Ligero": 1.375, "Moderado": 1.55, "Activo": 1.725, "Muy activo": 1.9}
    factor = factores.get(nivel, 1.55)
    mantenimiento = round(tmb * factor)
    perdida = round(mantenimiento - 500)
    pdf.cell(200, 10, limpiar_texto(f"Calorías estimadas para mantener tu peso: {mantenimiento} kcal/día"), ln=True)
    pdf.cell(200, 10, limpiar_texto(f"Calorías estimadas para perder peso: {perdida} kcal/día"), ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, limpiar_texto("Ejemplo de alimentación para 1 día"), ln=True)
    pdf.set_font("Arial", size=11)
    if objetivo == "Perder grasa":
        ejemplo = [
            "Desayuno: Avena cocida con fruta y una cucharada de mantequilla de maní",
            "Media mañana: Yogurt natural con semillas",
            "Almuerzo: Pechuga de pollo, arroz integral, ensalada con aceite de oliva",
            "Merienda: Batido de proteína con plátano",
            "Cena: Tortilla de claras con verduras y palta"
        ]
    elif objetivo == "Ganar músculo":
        ejemplo = [
            "Desayuno: Pan integral con huevos, fruta y leche",
            "Media mañana: Batido de avena, plátano y proteína",
            "Almuerzo: Carne magra, papas cocidas y verduras",
            "Merienda: Yogurt griego con nueces",
            "Cena: Arroz con atún, palta y huevo duro"
        ]
    else:
        ejemplo = [
            "Desayuno: Pan integral con queso y fruta",
            "Media mañana: Frutos secos y yogurt",
            "Almuerzo: Pollo al horno con ensalada y quinoa",
            "Merienda: Fruta con mantequilla de maní",
            "Cena: Omelette de verduras y ensalada"
        ]
    for item in ejemplo:
        pdf.cell(200, 10, limpiar_texto(f"- {item}"), ln=True)
    pdf.ln(10)

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
