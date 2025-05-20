import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# Entraînement simple du modèle d'intention
training_sentences = [
    "Qui est le meilleur buteur ?",
    "Donne moi les stats de Messi",
    "Top passeur de Ligue 1",
    "Je veux les performances de Ronaldo",
    "Nombre de buts en Serie A",
    "Statistiques joueur Neymar",
    "Quel est le meilleur passeur en Ligue 1 ?",
    "Qui a marqué le plus de buts en Liga ?",
    "Stat joueur Mbappe",
    "Je veux les stats de Haaland",
    "But en Bundesliga",
    "Assist en Premier League",
    "Carrière de Messi",
    "Le meilleur buteur du championnat allemand",
    "Infos joueur Benzema",
    "Qui a délivré le plus de caviar en Ligue 1 ?",
    "Le meilleur en caviars en Premier League",
    "Top caviar en Bundesliga",
    "Nombre de caviars en Serie A",
    "mets à jour les buts de Messi à 25",
    "change les passes de Neymar à 10",
    "modifie les stats de Mbappe",
    "modifie les buts de Haaland à 32",
    "mets à jour les buts de Neymar à 18",
    "change les buts de Mbappe à 12",
    "modifie les passes de Messi à 15",
    "ajuste les buts de Ronaldo à 25",
    "modifie le nombre de buts de Haaland à 30",
    "update les passes de Griezmann à 5",
    "mets les buts de Neymar à 10",
    "mets les passes de Neymar à 12",
    "mets à jour les stats de Neymar",
    "mets à jour les performances de Mbappé",
    "mets les statistiques de Haaland à jour",
    "modifie les buts de Lewandowski à 20",
    "change les performances de Messi",
    "Qui a marqué le plus de buts en Espagne",
    "Le meilleur buteur en Espagne",
    "Nombre de buts marqués en Espagne",
    "Top buteur en Espagne",
    "qui a distribué le plus de caviar en espagne"



]

training_labels = [
    "topscorer",
    "player_stats",
    "topassist_by_league",
    "player_stats",
    "topscorer_by_league",
    "player_stats",
    "topassist_by_league",
    "topscorer_by_league",
    "player_stats",
    "player_stats",
    "topscorer_by_league",
    "topassist_by_league",
    "player_stats",
    "topscorer_by_league",
    "player_stats",
    "topassist_by_league",
    "topassist_by_league",
    "topassist_by_league",
    "topassist_by_league",
    "update_goals",
    "update_assists",
    "update_stats",
    "update_goals",
    "update_goals",
    "update_goals",
    "update_assists",
    "update_goals",
    "update_goals",
    "update_assists",
    "update_goals",
    "update_assists",
    "update_stats",
    "update_stats",
    "update_stats",
    "update_goals",
    "update_stats",
    "topscorer_by_league",
    "topscorer_by_league",
    "topscorer_by_league",
    "topscorer_by_league",
    "topassist_by_league"




]

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

# Modèle de classification
model = LogisticRegression()
model.fit(X, training_labels)

# Dossier pour enregistrer
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/tfidf.joblib")
joblib.dump(model, "models/intent_classifier.joblib")

# Fonction de prédiction
def predict_intent(text: str) -> str:
    vec = joblib.load("models/tfidf.joblib")
    clf = joblib.load("models/intent_classifier.joblib")
    x = vec.transform([text])
    return clf.predict(x)[0]
