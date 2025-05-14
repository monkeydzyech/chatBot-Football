from fastapi import APIRouter, Query,Body
import pandas as pd
import sqlite3
from api.core.nlp_utils import extract_player_name, extract_league
from api.models import Player
from api.core.chatbot import detect_intent
from api.core.nlp_utils import preprocess_text, extract_player_name, extract_league
from api.core.intent_model import predict_intent


router = APIRouter()





def load_data_from_db():
    conn = sqlite3.connect("data/players.db")
    df = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()
    return df

@router.get("/")
def welcome():
    return {"message": "Bienvenue sur l'API Football Stats"}

@router.get("/player")
def get_player_stats(name: str = Query(..., description="Nom du joueur")):
    df = load_data_from_db()
    results = df[df['player_name'].str.lower().str.contains(name.lower())]
    if results.empty:
        return {"error": "Aucun joueur trouvé"}
    return results.fillna("").replace([float("inf"), float("-inf")], 0).to_dict(orient="records")


@router.get("/topscorer")
def get_top_scorer():
    df = load_data_from_db()
    top = df.sort_values("goals", ascending=False).iloc[0]
    return {
        "name": top["player_name"],
        "goals": int(top["goals"]),
        "league": top["league"],
        "team": top["team_title"]
    }

@router.get("/topassist")
def get_top_assist():
    df = load_data_from_db()
    top = df.sort_values("assists", ascending=False).iloc[0]
    return {
        "name": top["player_name"],
        "assists": int(top["assists"]),
        "league": top["league"],
        "team": top["team_title"]
    }

@router.get("/chat")
def chatbot_response(q: str):
    intent = detect_intent(q)
    df = load_data_from_db()
    all_players = df["player_name"].dropna().unique().tolist()

    name = extract_player_name(q, all_players)

    if intent == "topscorer":
        top = df.sort_values("goals", ascending=False).iloc[0]
        return {
            "🎖️ Joueur": top["player_name"],
            "⚽ Buts marqués": int(top["goals"]),
            "🏟️ Équipe": top["team_title"],
            "🌍 Championnat": top["league"]
        }

    elif intent == "topassist":
        top = df.sort_values("assists", ascending=False).iloc[0]
        return {
            "🎖️ Joueur": top["player_name"],
            "🎯 Passes décisives": int(top["assists"]),
            "🏟️ Équipe": top["team_title"],
            "🌍 Championnat": top["league"]
        }

    elif intent == "player_stats":
        if not name:
            return {"error": "⚠️ Aucun nom de joueur détecté dans votre requête."}
        results = df[df["player_name"].str.lower() == name.lower()]
        if results.empty:
            return {"error": f"Aucun joueur trouvé pour '{name}'"}
        return results.fillna("").replace([float("inf"), float("-inf")], 0).to_dict(orient="records")


    elif intent == "topscorer_by_league":
        league = extract_league(q)
        if not league:
            return {"error": "❌ Aucun championnat reconnu dans la requête."}
        top = df[df["league"].str.lower() == league.lower()].sort_values("goals", ascending=False).iloc[0]
        return {
            "🎖️ Joueur": top["player_name"],
            "⚽ Buts marqués": int(top["goals"]),
            "🏟️ Équipe": top["team_title"],
            "🌍 Championnat": top["league"]
        }

    elif intent == "topassist_by_league":
        league = extract_league(q)
        if not league:
            return {"error": "❌ Aucun championnat reconnu dans la requête."}
        top = df[df["league"].str.lower() == league.lower()].sort_values("assists", ascending=False).iloc[0]
        return {
            "🎖️ Joueur": top["player_name"],
            "🎯 Passes décisives": int(top["assists"]),
            "🏟️ Équipe": top["team_title"],
            "🌍 Championnat": top["league"]
        }

    return {"message": "🤖 Désolé, je n’ai pas compris votre demande."}



@router.post("/player")
def add_player(player: Player):
    df = load_data_from_db()

    # Vérifie si le joueur existe déjà
    if player.player_name.lower() in df["player_name"].str.lower().tolist():
        return {"error": "❌ Joueur déjà existant."}

    
    new_row = pd.DataFrame([player.dict()])
    df = pd.concat([df, new_row], ignore_index=True)

    conn = sqlite3.connect("data/players.db")
    df.to_sql("players", conn, if_exists="replace", index=False)
    conn.close()

    return {"message": f"✅ Joueur '{player.player_name}' ajouté avec succès."}


@router.delete("/player")
def delete_player(name: str = Query(..., description="Nom du joueur à supprimer")):
    name = name.strip().lower()
    df = load_data_from_db()

    initial_count = len(df)
    df = df[df["player_name"].str.lower().str.strip() != name]

    if len(df) == initial_count:
        return {"error": f"❌ Joueur '{name}' introuvable."}

    conn = sqlite3.connect("data/players.db")
    df.to_sql("players", conn, if_exists="replace", index=False)
    conn.close()

    return {"message": f"🗑️ Joueur '{name}' supprimé avec succès."}


@router.put("/player")
def update_player(name: str = Query(..., description="Nom du joueur à modifier"), updates: dict = Body(...)):
    df = load_data_from_db()
    
    mask = df["player_name"].str.lower() == name.lower()
    
    if not mask.any():
        return {"error": f"❌ Joueur '{name}' introuvable."}
    
    for key, value in updates.items():
        if key in df.columns:
            df.loc[mask, key] = value
        else:
            return {"error": f"⚠️ Colonne '{key}' inexistante."}

    conn = sqlite3.connect("data/players.db")
    df.to_sql("players", conn, if_exists="replace", index=False)
    conn.close()

    return {"message": f"✏️ Joueur '{name}' mis à jour avec succès."}



