import zipfile, xml.etree.ElementTree as ET, re
from pathlib import Path

def extrair_docx(caminho):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(caminho) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    paragrafos = []
    for p in root.findall(".//w:p", ns):
        partes = [t.text for t in p.findall(".//w:t", ns) if t.text]
        if partes:
            paragrafos.append("".join(partes))
    return "\n".join(paragrafos)

def extrair_odt(caminho):
    with zipfile.ZipFile(caminho) as z:
        root = ET.fromstring(z.read("content.xml"))
    trechos = [el.text.strip() for el in root.iter() if el.text and el.text.strip()]
    return "\n".join(trechos)

docx = extrair_docx(Path("txt/24_09-TrabalhoEmpirico-PauloGiovani-Enajus2026-FINAL-cleuler-corrigido.docx"))
odt  = extrair_odt(Path("txt/limitacoes_experimento_4_JEC_Natal.odt"))

print("=== DOCX (primeiros 3000 chars) ===")
print(docx[:3000])
print("\n\n=== ODT (completo) ===")
print(odt[:5000])
