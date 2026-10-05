import argparse
import subprocess
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps


def deep_merge(target, source) :
    """
    Fusionne récursivement le dictionnaire `source` dans `target`.
    Permet de modifier certaines clés privés (ex: cv.phone, cv.email)
    sans écraser l'ensemble du bloc ou des sous-dictionnaires.
    """
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


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


def generer_cv(lang: str, base_dir: Path, build_dir: Path):
    """ Génère un cv dans le dossier build_dir en fonction de la langue choisie 
    à partir des documents présents dans base_dir."""

    full_cv_path = build_dir / f"full_cv_{lang}.yaml"

    # Fichiers YAML à charger et fusionner selon la langue choisie
    files_to_merge = [
        base_dir / f"{lang}_cv.yaml",
        base_dir / "config" / f"{lang}_design.yaml",
        base_dir / "config" / f"{lang}_locale.yaml",
        base_dir / "config" / f"{lang}_settings.yaml",
    ]

    full_data = {}

    # Chargement et fusion des fichiers YAML publics
    for file_path in files_to_merge:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                full_data |= yaml.safe_load(f) or {}

    # Fusion du fichier yaml unifié avec les données secrètes dans secrets.yaml s'il y en a
    secrets_path = base_dir / "private" / "secrets.yaml"
    if secrets_path.exists():
        with open(secrets_path, "r", encoding="utf-8") as f:
            secrets_data = yaml.safe_load(f) or {}
            deep_merge(full_data, secrets_data)

    # Si on met une photo, on utilise l'image recentrée de la photo
    cv = full_data.get("cv", {})
    original_photo = cv.get("photo")
    if original_photo:
        src = base_dir / original_photo
        if src.exists():
            dst = build_dir / f"{src.stem}_carre.png"
            cv["photo"] = str(prepare_photo(src, dst).resolve())

    # Sauvegarde dans le dossier build
    with open(full_cv_path, "w", encoding="utf-8") as f:
        yaml.dump(full_data, f, allow_unicode=True, sort_keys=False)

    # Exécute RenderCV depuis le répertoire build_dir
    subprocess.run(["rendercv", "render", str(full_cv_path)], cwd=build_dir, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de CV multilingue")
    parser.add_argument("--lang", choices=["fr", "en"], default="fr", help="Langue à générer")
    parser.add_argument("--all", action="store_true", help="Générer FR et EN")
    args = parser.parse_args()

    # Répertoires dynamiques
    base_dir = Path(__file__).resolve().parent
    build_dir = base_dir / "build"
    build_dir.mkdir(exist_ok=True)

    if args.all:
        for l in ["fr", "en"]:
            generer_cv(l, base_dir, build_dir)
    else:
        generer_cv(args.lang, base_dir, build_dir)