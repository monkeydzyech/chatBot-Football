from api.core.nlp_utils import extract_league, ligue_aliases
from api.core.intent_model import predict_intent

def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    mots_buteur = [
        "meilleur buteur", "top buteur", "plus de buts", "plus grand buteur", "but marqué",
        "marqué le plus de buts", "celui qui a marqué le plus", "nombre de buts", "top scoreur",
        "buteur"
    ]

    mots_passeur = [
        "meilleur passeur", "top passeur", "plus de passes", "passe décisive", "assist",
        "passes réussies", "nombre de passes", "plus grand passeur",
        "celui qui a fait le plus de passes", "passeur"
    ]

    mots_stats = [
        "stat", "stats", "statistique", "statistiques", "performance", "performances",
        "carrière", "infos joueur"
    ]

    contient_ligue = any(
        any(alias in text for alias in aliases)
        for aliases in ligue_aliases.values()
    )

    # 1. Cas simples avec mots-clés
    if any(m in text for m in mots_buteur):
        return "topscorer_by_league" if contient_ligue else "topscorer"

    if any(m in text for m in mots_passeur):
        return "topassist_by_league" if contient_ligue else "topassist"

    if any(m in text for m in mots_stats):
        return "player_stats"

    # 2. Sinon on laisse le modèle ML décider
    return predict_intent(user_input)
