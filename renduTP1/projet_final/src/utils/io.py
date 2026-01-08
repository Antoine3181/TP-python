from datetime import datetime

import pandas as pd

from .paths import (
    DOSSIER_DONNEES,
    DOSSIER_RAW_LOGS,
    DOSSIER_SORTIE,
    DOSSIER_ARCHIVE,
)


def nettoyer_csv():
    chemin_donnees = DOSSIER_DONNEES / "data.csv"
    DOSSIER_SORTIE.mkdir(exist_ok=True)
    chemin_sortie = DOSSIER_SORTIE / "clean_data.csv"

    tableau = pd.read_csv(
        chemin_donnees,
        sep=";",
        encoding="utf-8",
        dtype=str,
        keep_default_na=False,
        engine="python",
        on_bad_lines="skip",  #si une ligne n'est pas conforme on la saute
    )

    tableau.columns = [
        nom.strip().lower().replace(" ", "_")
        for nom in tableau.columns
    ]

    tableau = tableau.replace({"": None})
    tableau = tableau.dropna(how="all")

    if "id_client" in tableau.columns:
        tableau["id_client"] = pd.to_numeric(
            tableau["id_client"], errors="coerce"
        )

    if "age" in tableau.columns:
        tableau["age"] = pd.to_numeric(
            tableau["age"], errors="coerce"
        )

    if "montant_total_eur" in tableau.columns:
        tableau["montant_total_eur"] = (
            tableau["montant_total_eur"]
            .str.replace(" ", "")
            .str.replace(",", ".")
        )
        tableau["montant_total_eur"] = pd.to_numeric(
            tableau["montant_total_eur"], errors="coerce"
        )

    tableau.to_csv(chemin_sortie, index=False, encoding="utf-8")
    print(f"data clean : {chemin_sortie}")


def collecter_erreurs():
    DOSSIER_RAW_LOGS.mkdir(exist_ok=True)
    DOSSIER_ARCHIVE.mkdir(exist_ok=True)
    DOSSIER_SORTIE.mkdir(exist_ok=True)

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier_erreurs = DOSSIER_SORTIE / f"errors_{horodatage}.log"

    total_erreurs = 0

    with fichier_erreurs.open("w", encoding="utf-8") as sortie:
        for fichier_log in DOSSIER_RAW_LOGS.glob("*.log"):
            lignes = fichier_log.read_text(encoding="utf-8").splitlines()

            for ligne in lignes:
                if "ERROR" in ligne:
                    sortie.write(f"{fichier_log.name}: {ligne}\n")
                    total_erreurs += 1

            fichier_log.rename(DOSSIER_ARCHIVE / fichier_log.name)

    print(f"Fichier d'erreurs créé : {fichier_erreurs}")
    print(f"Nombre de lignes contenant une erreur : {total_erreurs}")
