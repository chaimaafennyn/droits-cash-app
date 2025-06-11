from fpdf import FPDF
from io import BytesIO

def generer_pdf(situation, revenu, logement, enfants, aides):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Dossier - Droits+Cash", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Situation : {situation}", ln=True)
    pdf.cell(200, 10, txt=f"Revenu mensuel : {revenu} €", ln=True)
    pdf.cell(200, 10, txt=f"Logement : {logement}", ln=True)
    pdf.cell(200, 10, txt=f"Enfants : {enfants}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Aides estimées :", ln=True)
    
    for aide, montant in aides.items():
        pdf.cell(200, 10, txt=f"- {aide} : {montant} €/mois", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
