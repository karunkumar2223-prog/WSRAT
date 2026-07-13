"""
WSRAT Dynamic PDF Report Generator (Starter)

This version is schema-aware and avoids hardcoded assumptions.
Extend styling as desired.
"""
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

styles = getSampleStyleSheet()

def _heading(elements, text):
    elements.append(Paragraph(f"<b>{text}</b>", styles["Heading2"]))
    elements.append(Spacer(1,8))

def _table(elements, rows):
    t=Table(rows)
    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("BOTTOMPADDING",(0,0),(-1,0),6),
    ]))
    elements.append(t)
    elements.append(Spacer(1,12))

def _render(elements, key, value):
    _heading(elements, key.title())
    if isinstance(value, dict):
        rows=[["Key","Value"]]
        for k,v in value.items():
            if isinstance(v,(dict,list)):
                rows.append([str(k), str(v)])
            else:
                rows.append([str(k), str(v)])
        _table(elements,rows)
    elif isinstance(value,list):
        if not value:
            elements.append(Paragraph("No data.", styles["Normal"]))
            return
        if isinstance(value[0],dict):
            headers=list(value[0].keys())
            rows=[headers]
            for item in value:
                rows.append([str(item.get(h,"")) for h in headers])
            _table(elements,rows)
        else:
            rows=[["Value"]]+[[str(x)] for x in value]
            _table(elements,rows)
    else:
        elements.append(Paragraph(str(value), styles["Normal"]))
        elements.append(Spacer(1,12))

def create_pdf_report(target, results):
    os.makedirs("reports/pdf", exist_ok=True)
    name=target.replace("https://","").replace("http://","").replace("/","_")
    outfile=f"reports/pdf/{name}.pdf"
    doc=SimpleDocTemplate(outfile)
    elements=[]
    elements.append(Paragraph("<b><font size=20>WSRAT Security Assessment Report</font></b>", styles["Title"]))
    elements.append(Spacer(1,16))
    elements.append(Paragraph(f"<b>Target:</b> {target}", styles["Normal"]))
    elements.append(Spacer(1,16))
    for section,data in results.items():
        try:
            _render(elements,section,data)
        except Exception as e:
            _heading(elements,section)
            elements.append(Paragraph(f"Rendering error: {e}", styles["Normal"]))
    doc.build(elements)
    return outfile
