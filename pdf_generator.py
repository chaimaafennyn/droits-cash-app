# pdf_generator.py
from fpdf import FPDF
from io import BytesIO
from datetime import date

def generer_pdf(situation, revenu, logement, enfants, aides):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Dossier Droits+Cash")
    pdf.cell(200, 10, txt="Dossier Droits+Cash", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Date de simulation : {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Informations personnelles :", ln=True)
    pdf.cell(200, 10, txt=f"- Situation : {situation}", ln=True)
    pdf.cell(200, 10, txt=f"- Revenu mensuel : {revenu} €", ln=True)
    pdf.cell(200, 10, txt=f"- Logement : {logement}", ln=True)
    pdf.cell(200, 10, txt=f"- Nombre d'enfants : {enfants}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Aides estimées :", ln=True)
    if not aides:
        pdf.cell(200, 10, txt="- Aucune aide détectée", ln=True)
    else:
        for aide, montant in aides.items():
            pdf.cell(200, 10, txt=f"- {aide} : {montant} €/mois", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
