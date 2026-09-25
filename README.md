# Générateur de CV avec RenderCV — Choix des données sécurisées

Ce projet permet de générer un CV au format PDF basé sur **RenderCV**. Il permet de conserver le code source et la structure sur GitHub tout en gardant certaines données confidentielles au choix (email, téléphone, photo) en local. Il permet également de changer la forme de la photo du CV, par défaut la forme est circulaire.

---

## 📁 Architecture du projet

```
.
├── cv.yaml               # CV public
├── config/
│   ├── design.yaml       # Style visuel (polices, marges, couleurs)
│   ├── locale.yaml       # Langue des intitulés
│   └── settings.yaml     # Paramètres de build (dossier de sortie)
├── private/              # 🔒 Dossier ignoré par Git (Données strictement locales)
│   ├── secrets.yaml      # Champs privés (email, téléphone)
│   └── photo.jpg          # Photo personnelle
├── build/                # Artefacts générés (PDF, LaTeX)
├── create_cv.py           # Script Python de fusion et de compilation
├── .gitignore             # Masque les dossiers private/ et build/
└── README.md
```

---

## ✅ Prérequis

- Python 3.9 ou supérieur

## 📦 Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/super-pingouin/CV.git
   cd CV
   ```

2. Créer un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔒 Configuration du fichier `private/secrets.yaml`

Pour ajouter ou masquer uniquement vos coordonnées personnelles, créez le fichier `private/secrets.yaml` :

```yaml
cv:
  email: mon.email.prive@example.com
  phone: "+33 6 12 34 56 78"
  location: Paris, France
  photo: private/photo.jpg
```

Toutes les clés spécifiées dans ce fichier remplaceront automatiquement les valeurs correspondantes de `cv.yaml` lors de l'exécution de `create_cv.py`.

> ⚠️ Ce fichier n'est jamais versionné : il est explicitement listé dans `.gitignore`. Vous pouvez donc versionner `cv.yaml` avec des valeurs génériques ou vides pour ces champs, en toute sécurité.

---

## ⚙️ Exécution en local

```bash
python create_cv.py
```

Le fichier PDF final sera compilé et enregistré dans le dossier `build/render_cv_output`.

---

## 🎨 Personnalisation

| Fichier | Rôle |
|---|---|
| `config/design.yaml` | Polices, marges, couleurs, mise en page générale du CV |
| `config/locale.yaml` | Langue des intitulés (ex. « Expérience », « Formation ») |
| `config/settings.yaml` | Paramètres de build (dossier de sortie, options de compilation) |

Modifiez ces fichiers pour adapter le rendu sans toucher au contenu du CV lui-même (`cv.yaml`).

### 🖼️ Forme de la photo de profil
Le script `create_cv.py` ajuste automatiquement la photo déclarée dans `photo`. Vous pouvez modifier le paramètre `forme` de la fonction `prepare_photo()` directement dans le script pour changer le rendu :
* `"cercle"` *(par défaut)* : découpe la photo en rond.
* `"arrondi"` : conserve un carré aux coins adoucis.
* `"carre"` : conserve l'image au format carré brut.
---
