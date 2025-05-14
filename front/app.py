import streamlit as st
import requests

st.set_page_config(page_title="Chatbot - Performances des Joueurs", layout="centered")

st.title("🤖 Chatbot - Performances des Joueurs")
st.markdown("Pose ta question *(ex: stats de Messi en 2021)*")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("", placeholder="Ex: Qui est le meilleur buteur ?", label_visibility="collapsed")

if user_input:
    response = requests.get("http://localhost:8000/chat", params={"q": user_input})
    result = response.json()
    st.session_state.history.insert(0, (user_input, result))

# 💬 Historique
st.markdown("### 💬 Historique du Chat")
for question, answer in st.session_state.history:
    st.markdown(f"**👤 {question}**")

    if "error" in answer:
        st.warning(answer["error"])
    elif "message" in answer:
        st.info(answer["message"])
    elif isinstance(answer, dict):
        st.success("🎯 Voici ce que j’ai trouvé :")
        for key, value in answer.items():
            st.markdown(f"- **{key}** : {value}")
    elif isinstance(answer, list) and len(answer) > 0:
        player = answer[0]
        st.success(f"🎯 Voici ce que j’ai trouvé pour **{player.get('player_name', 'ce joueur')}** pour sa carrière enregistrée :")
        if "goals" in player:
            st.markdown(f"- ⚽ **Buts marqués** : {int(player['goals'])}")
        if "assists" in player:
            st.markdown(f"- 🎯 **Passes décisives** : {int(player['assists'])}")
        if "games" in player:
            st.markdown(f"- 🕹️ **Matchs joués** : {int(player['games'])}")
        if "team_title" in player:
            st.markdown(f"- 🏟️ **Équipe** : {player['team_title']}")
        if "league" in player:
            st.markdown(f"- 🌍 **Championnat** : {player['league']}")
    else:
        st.warning("🤖 Désolé, je n’ai pas compris votre demande.")

if st.button("🗑️ Effacer l'historique"):
    st.session_state.history = []
