import streamlit as st
import requests
import pandas as pd
st.title("Tableau de bord eCommerce")
# Récupérer les KPI depuis l'API
response = requests.get("http://127.0.0.1:8000/kpi/orders-per-customer")
if response.status_code == 200:
    data = response.json()["data"]
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("_id")["total_orders"])
else:
    st.error("Erreur lors du chargement des données")

"""response2 = requests.get("http://127.0.0.1:8000/kpi/orders-per-category")
if response2.status_code == 200:
    data = response2.json()["data"]
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("_id")["total_orders"])
else:
    st.error("Erreur lors du chargement des données")"""