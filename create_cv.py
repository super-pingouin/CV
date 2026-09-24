import yaml
import subprocess

# Charger le contenu principal du CV
with open("cv.yaml", "r", encoding="utf-8") as f:
    full_data = yaml.safe_load(f)

# Charge et injecte design.yaml sous la clé 'design'
with open("design.yaml", "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Charge et injecte locale.yaml sous la clé 'locale'
with open("locale.yaml", "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Charge et injecte settings.yaml sous la clé 'settings'
with open("settings.yaml", "r", encoding="utf-8") as f:
    full_data |= yaml.safe_load(f)

# Sauvegarde dans un fichier unique fusionné
with open("full_cv.yaml", "w", encoding="utf-8") as f:
    yaml.dump(full_data, f, allow_unicode=True, sort_keys=False)

# Exécuter RenderCV sur le fichier unifié
subprocess.run(["rendercv", "render", "full_cv.yaml"])