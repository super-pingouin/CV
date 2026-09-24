import yaml
import subprocess
from pathlib import Path

# On construit les chemins des fichiers dynamiquement
BASE_DIR = Path(__file__).resolve().parent
CV_PATH = BASE_DIR / "cv.yaml"
CONFIG_PATH = BASE_DIR / "config" 
DESIGN_PATH = CONFIG_PATH / "design.yaml"
LOCALE_PATH = CONFIG_PATH / "locale.yaml"
SETTINGS_PATH = CONFIG_PATH / "locale.yaml"
FULL_CV_PATH = BASE_DIR / "full_cv.yaml"

# Charger le contenu principal du CV
with open(CV_PATH, "r", encoding="utf-8") as f:
    full_data = yaml.safe_load(f)

# Charge et ajoute le contenu de design.yaml
with open(DESIGN_PATH, "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Charge et ajoute le contenu de locale.yaml
with open(LOCALE_PATH, "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Charge et ajoute le contenu de settings.yaml
with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Sauvegarde dans un fichier unique fusionné
with open(FULL_CV_PATH, "w", encoding="utf-8") as f:
    yaml.dump(full_data, f, allow_unicode=True, sort_keys=False)

# Exécute RenderCV sur le fichier unifié
subprocess.run(["rendercv", "render", "full_cv.yaml"])