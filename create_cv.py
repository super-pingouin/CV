import yaml
import subprocess
from pathlib import Path


# On construit les chemins des fichiers dynamiquement
BASE_DIR = Path(__file__).resolve().parent
FULL_CV_PATH = BASE_DIR / "full_cv.yaml"

# Fichiers YAML à charger et fusionner dans l'ordre
FILES_TO_MERGE = [
    BASE_DIR / "cv.yaml",
    BASE_DIR / "config" / "design.yaml",
    BASE_DIR / "config" / "locale.yaml",
    BASE_DIR / "config" / "settings.yaml",
]

full_data = {}

# Chargement et fusion des fichiers YAML
for file_path in FILES_TO_MERGE:
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            full_data |= yaml.safe_load(f) or {}

# Sauvegarde dans un fichier unifié
with open(FULL_CV_PATH, "w", encoding="utf-8") as f:
    yaml.dump(full_data, f, allow_unicode=True, sort_keys=False)

# Exécute RenderCV depuis le chemin BASE_DIR
subprocess.run(["rendercv", "render", FULL_CV_PATH], cwd=BASE_DIR)