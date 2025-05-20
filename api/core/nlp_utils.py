import spacy
import difflib

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> list:
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return tokens

def extract_player_name(text: str, all_players: list[str]) -> str:
    text = text.lower()
    doc = nlp(text)

    # 1. Entité nommée (Lionel Messi, Kevin De Bruyne, etc.)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            match = find_closest_player(ent.text, all_players)
            if match:
                return match

    # 2. Recherche exacte ou sous-chaîne dans un nom
    for player in all_players:
        name = player.lower()
        if name in text:
            return player
        last = name.split()[-1]
        if last in text:
            return player

    # 3. Recherche par mots proches
    words = [t.text for t in doc if t.is_alpha]
    for word in words:
        match = find_closest_player(word, all_players)
        if match:
            return match

    return ""

def find_closest_player(fragment: str, all_players: list[str]) -> str:
    matches = difflib.get_close_matches(fragment, all_players, n=1, cutoff=0.7)
    return matches[0] if matches else ""

ligue_aliases = {
    "ligue 1": ["ligue 1", "league 1", "france", "championnat de france","championnat français"],
    "premier league": ["premier league", "angleterre", "epl", "championnat anglais"],
    "bundesliga": ["bundesliga", "allemagne", "championnat allemand"],
    "la liga": ["la liga", "liga", "espagne", "championnat espagnol", "ligue a"],
    "serie a": ["serie a", "série a", "italie", "championnat italien"]
}

def extract_league(text: str) -> str:
    text = text.lower()
    for league, aliases in ligue_aliases.items():
        for alias in aliases:
            if alias in text:
                return league
    return ""

def extract_stat_type(text: str) -> str:
    text = text.lower()
    if "but" in text or "goal" in text:
        return "goals"
    if "passe" in text or "assist" in text or "caviar" in text:
        return "assists"
    return ""
