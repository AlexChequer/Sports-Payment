from datetime import datetime


def minimal_pdf_bytes(text: str) -> bytes:
    # PDF mínimo (não perfeito, apenas para demo)
    # Para produção, use reportlab ou weasyprint.
    content = f"Invoice generated at {datetime.utcnow().isoformat()}\n{text}\n"
    # Cria um PDF super simples como bytes (fake)
    return ("%PDF-1.4\n%âãÏÓ\n1 0 obj<<>>endobj\n" # cabeçalho
    "2 0 obj<<>>endobj\n" # objeto vazio
    "trailer<<>>\n%%EOF").encode()