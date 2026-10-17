"""Nettoie des notebooks Colab avant publication sur GitHub.

Supprime les métadonnées qui contiennent des informations personnelles
(nom d'affichage Google, identifiant utilisateur) ou qui empêchent
GitHub d'afficher le notebook. Les sorties (graphiques, tableaux) sont conservées.

Usage (fonctionne sous Windows, macOS et Linux) :
    python scripts/clean_notebooks.py notebooks/*.ipynb
"""
import glob
import json
import sys
from pathlib import Path


def clean(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    nb.get("metadata", {}).pop("colab", None)
    nb.get("metadata", {}).pop("widgets", None)
    for cell in nb.get("cells", []):
        meta = cell.get("metadata", {})
        meta.pop("executionInfo", None)
        meta.pop("colab", None)
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Nettoyé : {path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage : python scripts/clean_notebooks.py notebooks/*.ipynb")
    # Windows ne développe pas les jokers (*) : on le fait ici.
    files = []
    for arg in sys.argv[1:]:
        files.extend(glob.glob(arg) or [arg])
    for f in files:
        clean(Path(f))
