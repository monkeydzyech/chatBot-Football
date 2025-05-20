from fastapi import APIRouter, Query, Body
import pandas as pd
import sqlite3
from api.models import Player
from api.core.chatbot import detect_intent
from api.core.nlp_utils import (
    preprocess_text,
    extract_player_name,
    extract_league,
    extract_stat_type,
)

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
def get_player_stats(name: str = Query(...)):
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

    elif intent in ["update_goals", "update_assists", "update_stats"]:
        if not name:
            return {"error": "❌ Joueur non détecté."}

        import re
        numbers = re.findall(r"\d+", q)
        if not numbers:
            return {"error": "❌ Aucune valeur à mettre à jour trouvée."}
        value = int(numbers[0])

        column = extract_stat_type(q)
        if not column:
            return {"error": "❌ Type de statistique non reconnu (but/passe)."}

        mask = df["player_name"].str.lower() == name.lower()
        if not mask.any():
            return {"error": f"❌ Joueur '{name}' introuvable."}

        df.loc[mask, column] = value
        conn = sqlite3.connect("data/players.db")
        df.to_sql("players", conn, if_exists="replace", index=False)
        conn.close()

        return {"message": f"✏️ {column.capitalize()} de '{name}' mis à jour à {value}."}

    return {"message": "🤖 Désolé, je n’ai pas compris votre demande."}
