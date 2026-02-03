#!/bin/bash

# Script complet pour lancer l'application Streamlit

echo "=== LANCEMENT DE L'APPLICATION STREAMLIT ==="
echo ""

# Afficher le répertoire courant
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

# Lancer l'application
echo "Lancement de l'application..."
echo ""
python3 -m streamlit run app/app.py

echo ""
echo "=== FIN ==="
