import subprocess
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps


def prepare_photo(src, dst, taille=600, forme="cercle"):
    """ Recentre la photo original en carré centré et change sa forme en carré, cercle ou arrondi
    dst doit être un .png car les formes "cercle" et "arrondi" utilisent la transparence des pixels :  """

    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        taille = min(taille, *img.size)
        img = ImageOps.fit(img, (taille, taille), Image.Resampling.LANCZOS)
        
        if forme == "carre":
            img.save(dst)
            return dst

        s = taille * 4
        cadre = (8, 8, s - 9, s - 9)  # marge pour éviter des irrégularités au bord
        masque = Image.new("L", (s, s), 0)
        dessin = ImageDraw.Draw(masque)
        if forme == "cercle":
            dessin.ellipse(cadre, fill=255)
        else:
            dessin.rounded_rectangle(cadre, radius=s // 6, fill=255)
        masque = masque.resize((taille, taille), Image.Resampling.BOX)

        sortie = Image.new("RGBA", (taille, taille), (255, 255, 255, 0))
        sortie.paste(img, (0, 0), masque)
        sortie.save(dst)
    return dst

# Répertoires dynamiques
BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "build"
BUILD_DIR.mkdir(exist_ok=True)
FULL_CV_PATH = BUILD_DIR / "full_cv.yaml"

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


# Recentre la photo original et remplace l'image dans le YAML fusionné
cv = full_data.get("cv")
original_photo = cv.get("photo")
if original_photo:
    src = BASE_DIR / original_photo
    dst = BUILD_DIR / f"{src.stem}_carre.png"
    cv["photo"] = str(prepare_photo(src, dst).resolve())

# Sauvegarde dans le dossier build
with open(FULL_CV_PATH, "w", encoding="utf-8") as f:
    yaml.dump(full_data, f, allow_unicode=True, sort_keys=False)

# Exécute RenderCV depuis le répertoire BUILD_DIR
subprocess.run(["rendercv", "render", str(FULL_CV_PATH)], cwd=BUILD_DIR, check=True)