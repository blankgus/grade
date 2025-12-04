# ler_pdf_bruto.py
import pdfplumber

caminho = "Professores_Manha.pdf"

print("=== Conteúdo bruto do PDF ===")
with pdfplumber.open(caminho) as pdf:
    for i, pagina in enumerate(pdf.pages):
        print(f"\n--- Página {i+1} ---")
        texto = pagina.extract_text()
        if texto:
            print(texto[:1000])  # Mostra os primeiros 1000 caracteres
        else:
            print("(Página sem texto)")

        print("\n--- Tabelas encontradas ---")
        tabelas = pagina.extract_tables()
        if tabelas:
            for j, tabela in enumerate(tabelas):
                print(f"Tabela {j+1}:")
                for linha in tabela[:5]:  # Mostra as 5 primeiras linhas
                    print(linha)
        else:
            print("Nenhuma tabela encontrada nesta página.")