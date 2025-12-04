# importador_excel.py
import pandas as pd
from models import Turma, Professor, Disciplina, Sala
import database

def importar_tudo_do_excel(caminho="prodis.xlsx"):
    # Ler as abas do Excel
    try:
        df_professores = pd.read_excel(caminho, sheet_name="Professores")
    except ValueError:
        print("❌ Aba 'Professores' não encontrada no Excel.")
        df_professores = pd.DataFrame()  # DataFrame vazio
    except FileNotFoundError:
        print("❌ Arquivo Excel não encontrado!")
        return

    try:
        df_disciplinas = pd.read_excel(caminho, sheet_name="Disciplinas")
    except ValueError:
        print("❌ Aba 'Disciplinas' não encontrada no Excel.")
        df_disciplinas = pd.DataFrame()

    try:
        df_turmas = pd.read_excel(caminho, sheet_name="Turmas")
    except ValueError:
        print("❌ Aba 'Turmas' não encontrada no Excel.")
        df_turmas = pd.DataFrame()

    try:
        df_salas = pd.read_excel(caminho, sheet_name="Salas")
    except ValueError:
        print("❌ Aba 'Salas' não encontrada no Excel.")
        df_salas = pd.DataFrame()

    # --- Importar Professores ---
    professores = []
    if not df_professores.empty:
        if "nome" not in df_professores.columns or "disciplinas" not in df_professores.columns:
            print("❌ Colunas 'nome' ou 'disciplinas' não encontradas em 'Professores'.")
        else:
            for _, row in df_professores.iterrows():
                nome = row["nome"]
                disciplinas_str = row["disciplinas"]
                if pd.isna(disciplinas_str):
                    print(f"⚠️ Professor '{nome}' tem disciplinas vazias. Pulando...")
                    continue
                disciplinas = [d.strip() for d in str(disciplinas_str).split(",")]

                prof = Professor(
                    nome=nome,
                    disciplinas=disciplinas,
                    disponibilidade_dias={"seg", "ter", "qua", "qui", "sex"},
                    disponibilidade_horarios={1, 2, 3, 5, 6, 7}
                )
                professores.append(prof)

    # --- Importar Disciplinas ---
    disciplinas = []
    if not df_disciplinas.empty:
        if "nome" not in df_disciplinas.columns or "carga_semanal" not in df_disciplinas.columns:
            print("❌ Colunas 'nome' ou 'carga_semanal' não encontradas em 'Disciplinas'.")
        else:
            for _, row in df_disciplinas.iterrows():
                nome = row["nome"]
                carga = row["carga_semanal"]
                tipo = row.get("tipo", "media")  # Se não tiver tipo, assume "media"
                series_str = row.get("series", "6ano,7ano,8ano,9ano")  # Se não tiver, assume EF
                series = [s.strip() for s in series_str.split(",")]

                disc = Disciplina(
                    nome=nome,
                    carga_semanal=int(carga),
                    tipo=tipo,
                    series=series
                )
                disciplinas.append(disc)

    # --- Importar Turmas ---
    turmas = []
    if not df_turmas.empty:
        if "nome" not in df_turmas.columns or "serie" not in df_turmas.columns:
            print("❌ Colunas 'nome' ou 'serie' não encontradas em 'Turmas'.")
        else:
            for _, row in df_turmas.iterrows():
                nome = row["nome"]
                serie = row["serie"]
                turno = row.get("turno", "manha")  # Se não tiver turno, assume "manha"

                t = Turma(
                    nome=nome,
                    serie=serie,
                    turno=turno
                )
                turmas.append(t)

    # --- Importar Salas ---
    salas = []
    if not df_salas.empty:
        if "nome" not in df_salas.columns or "capacidade" not in df_salas.columns:
            print("❌ Colunas 'nome' ou 'capacidade' não encontradas em 'Salas'.")
        else:
            for _, row in df_salas.iterrows():
                nome = row["nome"]
                cap = row["capacidade"]
                tipo = row.get("tipo", "normal")  # Se não tiver tipo, assume "normal"

                s = Sala(
                    nome=nome,
                    capacidade=int(cap),
                    tipo=tipo
                )
                salas.append(s)

    # --- Salvar no banco ---
    if professores:
        database.salvar_professores(professores)
        print(f"✅ {len(professores)} professores importados e salvos.")
    else:
        print("⚠️ Nenhum professor foi importado.")

    if disciplinas:
        database.salvar_disciplinas(disciplinas)
        print(f"✅ {len(disciplinas)} disciplinas importadas e salvas.")
    else:
        print("⚠️ Nenhuma disciplina foi importada.")

    if turmas:
        database.salvar_turmas(turmas)
        print(f"✅ {len(turmas)} turmas importadas e salvas.")
    else:
        print("⚠️ Nenhuma turma foi importada.")

    if salas:
        database.salvar_salas(salas)
        print(f"✅ {len(salas)} salas importadas e salvas.")
    else:
        print("⚠️ Nenhuma sala foi importada.")

if __name__ == "__main__":
    importar_tudo_do_excel()