# Générateur de CV avec RenderCV — Données sécurisées

Ce promet permet de générer un CV au format PDF basé sur **RenderCV**. Il permet de conserver le code source et la structure sur GitHub tout en gardant certaines données confidentielles (email, téléphone, photo) en local.

---

## 📁 Architecture du projet

.
├── cv.yaml               # CV public
├── config/
│   ├── design.yaml       # Style visuel (polices, marges, couleurs)
│   ├── locale.yaml       # Langue des intitulés
│   └── settings.yaml     # Paramètres de build (dossier de sortie)
├── private/              # 🔒 Dossier ignoré par Git (Données strictement locales)
│   ├── secrets.yaml      # Champs privées (email, téléphone)
│   └── photo.jpg         # Photo personnelle
├── build/                # Artefacts générés (PDF, LaTeX)
├── create_cv.py         # Script Python de fusion et de compilation
├── .gitignore            # Masque les dossier private/ et build/
└── README.md


🔒 Configuration du fichier private/secrets.yaml

Pour ajouter ou masquer uniquement vos coordonnées personnelles, créez le fichier private/secrets.yaml :

cv:
  email: mon.email.prive@example.com
  phone: "+33 6 12 34 56 78"
  location: Paris, France
  photo: private/photo.jpg


Toutes les clés spécifiées dans ce fichier remplaceront automatiquement les valeurs correspondantes de cv.yaml lors de l'exécution de generer_cv.py.

⚙️ Exécution en local

python create_cv.py


Le fichier PDF final sera compilé et enregistré dans le dossier build/.
