from pathlib import Path

DOSSIER_RACINE = Path(__file__).resolve().parents[2]

DOSSIER_DONNEES = DOSSIER_RACINE / "data"
DOSSIER_RAW_LOGS = DOSSIER_RACINE / "raw_logs"
DOSSIER_SORTIE = DOSSIER_RACINE / "output"
DOSSIER_ARCHIVE = DOSSIER_RACINE / "archive"
