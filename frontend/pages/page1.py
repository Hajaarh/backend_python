import streamlit as st
import requests
import pandas as pd
import altair as alt

st.title("Tableau de bord eCommerce")

st.header("Nombre de commandes par client")

response = requests.get("http://127.0.0.1:8000/kpi/orders-per-customer")
if response.status_code == 200:
    data = response.json()["data"]
    df = pd.DataFrame(data)

    if not df.empty:
        df['_id'] = df['_id'].astype(str)
        st.bar_chart(df.set_index('_id')['total_orders'])
    else:
        st.write("Aucune donnée disponible pour les commandes par client.")
else:
    st.error("Erreur lors du chargement des données pour les commandes par client.")

st.header("Données enrichies des commandes")

response_detailed = requests.get("http://127.0.0.1:8000/kpi/orders-detailed")
if response_detailed.status_code == 200:
    detailed_data = response_detailed.json()["data"]
    detailed_df = pd.DataFrame(detailed_data)

    if not detailed_df.empty:
        detailed_df['_id'] = detailed_df['_id'].astype(str)
        detailed_df['customer_name'] = detailed_df['customer_name'].astype(str)
        detailed_df['location'] = detailed_df['location'].astype(str)

        st.dataframe(detailed_df)

        st.subheader("Graphique des commandes par client")
        chart = alt.Chart(detailed_df).mark_bar().encode(
            x='customer_name:N',
            y='total_orders:Q',
            color='location:N'
        ).properties(
            title="Nombre de commandes par client",
            width=800
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Graphique des produits commandés par client")
        product_chart = alt.Chart(detailed_df).mark_bar().encode(
            x='customer_name:N',
            y='product_count:Q',
            color='location:N'
        ).properties(
            title="Nombre de produits commandés par client",
            width=800
        )
        st.altair_chart(product_chart, use_container_width=True)
    else:
        st.write("Aucune donnée enrichie disponible.")
else:
    st.error("Erreur lors du chargement des données détaillées.")
