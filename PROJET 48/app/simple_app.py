"""Simple Streamlit app with callbacks."""

import streamlit as st

# Initialize session state
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.title("Test Streamlit - Projet 48")
st.write("Si vous voyez ce message, Streamlit fonctionne !")

st.header("Test 1 : Affichage")
st.write("✅ Test d'affichage simple")

st.header("Test 2 : Bouton avec callback")

def increment_counter():
    """Callback pour le bouton."""
    st.session_state.counter += 1
    st.rerun()

st.button("Cliquez ici", on_click=increment_counter)
st.write(f"Nombre de clics : {st.session_state.counter}")

st.header("Test 3 : Entrée de texte")

def handle_text_input():
    """Callback pour l'entrée de texte."""
    st.rerun()

text_input = st.text_input("Entrez du texte", on_change=handle_text_input)
if text_input:
    st.success(f"Vous avez entré : {text_input}")

st.header("Test 4 : Sélection")

def handle_selectbox():
    """Callback pour la sélection."""
    st.rerun()

option = st.selectbox("Choisissez une option", ["Option 1", "Option 2", "Option 3"], on_change=handle_selectbox)
st.write(f"Option sélectionnée : {option}")

st.header("Test 5 : Checkbox")

def handle_checkbox():
    """Callback pour la checkbox."""
    st.rerun()

checked = st.checkbox("Cochez cette case", on_change=handle_checkbox)
if checked:
    st.success("✅ Case cochée !")

st.header("Test 6 : Slider")

def handle_slider():
    """Callback pour le slider."""
    st.rerun()

value = st.slider("Valeur", 0, 100, 50, on_change=handle_slider)
st.write(f"Valeur du slider : {value}")

st.divider()
st.success("🎉 Tous les tests sont fonctionnels !")
