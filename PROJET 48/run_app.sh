#!/bin/bash

# Script pour lancer l'application Streamlit

echo "=== LANCEMENT DE L'APPLICATION ==="
echo ""

# Vérifier le répertoire courant
echo "Répertoire courant :"
pwd
echo ""

# Vérifier Python
echo "Vérification de Python :"
python3 --version
echo ""

# Vérifier Streamlit
echo "Vérification de Streamlit :"
python3 -m pip show streamlit
echo ""

# Lancer l'application simple
echo "Lancement de l'application simple..."
echo ""
python3 -m streamlit run app/simple_app.py
