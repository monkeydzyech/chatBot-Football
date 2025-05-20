# 📊 Football Stats Chatbot

Un projet complet de chatbot intelligent capable de répondre à des questions en langage naturel sur les performances de joueurs de football.

---

## 🚀 Fonctionnalités principales

- 💬 Chatbot interactif via Streamlit
- 📡 API REST via FastAPI
- 🧠 Détection d’intentions via mots-clés + modèle Machine Learning (LogisticRegression)
- 🧾 Extraction intelligente de noms de joueurs et de ligues avec spaCy
- 🗄️ Connexion à une base de données SQLite
-    mise a jour des buts et passes decisive via la ch at
- ➕ ➖ ✏️ Ajout / Suppression / Modification de joueurs via API

---

## 🛠️ Technologies utilisées

- **FastAPI** pour l’API REST
- **Streamlit** pour l’interface utilisateur
- **SQLite + pandas** pour le stockage des données
- **spaCy** pour le NLP (lemmatisation, entités nommées)
- **scikit-learn** pour le modèle ML (TF-IDF + Logistic Regression)
- **joblib** pour sauvegarder le modèle
- **Postman** pour tester les routes API

---

## 📁 Structure du projet

Le projet est organisé en plusieurs répertoires :

- `api/`: contient la logique backend avec FastAPI
- `api/core/`: les modules NLP et ML (chatbot, tf-idf, etc.)
- `data/`: base de données SQLite + script d'import
- `front/`: l'interface utilisateur en Streamlit
- `models/`: fichiers `.joblib` du modèle TF-IDF
- `requirements.txt`: dépendances Python

---

## ⚙️ Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone <lien_du_repo>
cd football-stats-chatbot
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Charger la base de données (si vide)

```bash
python data/load_to_db.py
```

---

## ▶️ Lancer l’application

### Lancer l’API

```bash
uvicorn api.main:app --reload
```

### Lancer le front Streamlit

```bash
streamlit run front/app.py
```

---

## 🔁 Exemples de requêtes testables

- `Qui est le meilleur buteur ?`
- `Donne les stats de Neymar`
- `Meilleur passeur en Bundesliga`
- `Top buteur en Ligue 1`
- `Je veux les performances de Messi`
- `Ajoute un joueur` (via POST avec Postman)
- `Supprime le joueur X` (via DELETE)

---

## 🔍 API CRUD (tests via Postman)

### ➕ Ajouter un joueur

- **Méthode** : POST  
- **URL** : `http://localhost:8000/player`
- **Body (JSON)** :

```json
{
  "player_name": "Elias Frik",
  "games": 20,
  "goals": 15,
  "assists": 7,
  "team_title": "PSG",
  "league": "Ligue 1"
}
```

---

### ✏️ Modifier un joueur

- **Méthode** : PUT  
- **URL** : `http://localhost:8000/player?name=Yassine Driss`  
- **Body (JSON)** :

```json
{
  "goals": 18
}
```

---

### 🗑️ Supprimer un joueur

- **Méthode** : DELETE  
- **URL** : `http://localhost:8000/player?name=Elias Frik`

---

## ✅ Conformité au cahier des charges

- ✔️ Problématique NLP réelle (questions football)
- ✔️ Utilisation de spaCy + TF-IDF
- ✔️ Modèle ML simple avec Logistic Regression
- ✔️ API REST complète (GET, POST, PUT, DELETE)
- ✔️ Chatbot utilisable via interface Streamlit
- ✔️ Architecture modulaire, claire et séparée

---

## 🧠 Bonus / pistes d’amélioration

- Meilleure gestion des fautes de frappe
- Top 3 joueurs d’une catégorie
- Requêtes vocales
- Dockerisation du projet

---

## 👨‍💻 Auteur

Elias Frik
Rafael Nakache

