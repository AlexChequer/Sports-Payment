
from app.utils.pdf import minimal_pdf_bytes

def test_minimal_pdf_bytes_output():
    result = minimal_pdf_bytes("Teste de Fatura")
    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")
    assert b"%%EOF" in result
