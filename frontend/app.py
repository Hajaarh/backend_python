import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration générale de la page
st.set_page_config(page_title="Dashboard eCommerce", layout="wide")

# Sidebar: Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Choisir une section:",
    [
        "📊 KPI des ventes",
        "💰 KPI des profits",
        "🏙️ Analyse géographique",
        "📅 Analyse temporelle",
        "🏆 Top produits",
    ],
)

# Fonction pour récupérer des données à partir de l'API
def fetch_data(endpoint):
    response = requests.get(f"http://127.0.0.1:8000{endpoint}")
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        st.error(f"Erreur lors du chargement des données : {response.status_code}")
        return []

# Page : KPI des ventes
if menu == "📊 KPI des ventes":
    st.title("📊 KPI des ventes")

    # Total des ventes globales
    total_sales = fetch_data("/kpi/total-sales")
    if total_sales:
        st.metric(label="💵 Total des ventes globales", value=f"${total_sales[0]['total_sales']:.2f}")

    col1, col2 = st.columns(2)

    # Ventes par État
    sales_by_state = fetch_data("/kpi/sales-by-state")
    if sales_by_state:
        df_state = pd.DataFrame(sales_by_state)
        with col1:
            st.subheader("Ventes par État")
            fig1 = px.bar(
                df_state, x="total_sales", y="_id", orientation="h",
                title="Ventes par État",
                labels={"_id": "État", "total_sales": "Ventes"}
            )
            st.plotly_chart(fig1)

    # Ventes par catégorie
    sales_by_category = fetch_data("/kpi/sales-by-category")
    if sales_by_category:
        df_category = pd.DataFrame(sales_by_category)
        with col2:
            st.subheader("Ventes par catégorie")
            fig2 = px.pie(
                df_category, values="total_sales", names="_id",
                title="Répartition des ventes par catégorie",
                labels={"_id": "Catégorie", "total_sales": "Ventes"}
            )
            st.plotly_chart(fig2)

# Page : KPI des profits
elif menu == "💰 KPI des profits":
    st.title("💰 KPI des profits")

    # Profit total
    total_profit = fetch_data("/kpi/total-profit")
    if total_profit:
        st.metric(label="💵 Profit total global", value=f"${total_profit[0]['total_profit']:.2f}")

    col1, col2 = st.columns(2)

    # Profit par catégorie
    profit_by_category = fetch_data("/kpi/profit-by-category")
    if profit_by_category:
        df_profit_category = pd.DataFrame(profit_by_category)
        with col1:
            st.subheader("Profit par catégorie")
            fig3 = px.bar(
                df_profit_category, x="total_profit", y="_id", orientation="h",
                title="Profit par catégorie",
                labels={"_id": "Catégorie", "total_profit": "Profit"}
            )
            st.plotly_chart(fig3)

    # Top 5 produits les plus profitables
    top_5_products = fetch_data("/kpi/top-5-profitable-products")
    if top_5_products:
        df_top_products = pd.DataFrame(top_5_products)
        with col2:
            st.subheader("Top 5 produits les plus profitables")
            fig4 = px.bar(
                df_top_products, x="total_profit", y="_id", orientation="h",
                title="Top 5 produits les plus profitables",
                labels={"_id": "Produit", "total_profit": "Profit"}
            )
            st.plotly_chart(fig4)

# Page : Analyse géographique
elif menu == "🏙️ Analyse géographique":
    st.title("🏙️ Analyse géographique")

    # Ventes par État et Ville
    sales_by_state_city = fetch_data("/kpi/sales-by-state-city")
    if sales_by_state_city:
        df_state_city = pd.DataFrame(sales_by_state_city)
        st.subheader("Ventes par État et Ville")
        fig5 = px.treemap(
            df_state_city,
            path=["_id.State", "_id.City"],
            values="total_sales",
            title="Ventes par État et Ville",
            labels={"_id.State": "État", "_id.City": "Ville", "total_sales": "Ventes"}
        )
        st.plotly_chart(fig5)

# Page : Analyse temporelle
elif menu == "📅 Analyse temporelle":
    st.title("📅 Analyse temporelle")

    # Ventes par mois
    sales_by_period = fetch_data("/kpi/sales-by-period")
    if sales_by_period:
        df_period = pd.DataFrame(sales_by_period)
        df_period["date"] = pd.to_datetime(df_period["_id"].apply(lambda x: f"{x['year']}-{x['month']}-01"))
        st.subheader("Ventes mensuelles")
        fig6 = px.line(
            df_period, x="date", y="total_sales",
            title="Ventes mensuelles",
            labels={"date": "Date", "total_sales": "Ventes"}
        )
        st.plotly_chart(fig6)

# Page : Top produits
elif menu == "🏆 Top produits":
    st.title("🏆 Top produits")

    col1, col2 = st.columns(2)

    # Top 5 produits par quantité vendue
    top_5_quantity = fetch_data("/kpi/top-5-quantity-products")
    if top_5_quantity:
        df_top_quantity = pd.DataFrame(top_5_quantity)
        with col1:
            st.subheader("Top 5 produits par quantité vendue")
            fig7 = px.bar(
                df_top_quantity, x="total_quantity", y="_id", orientation="h",
                title="Top 5 produits par quantité vendue",
                labels={"_id": "Produit", "total_quantity": "Quantité"}
            )
            st.plotly_chart(fig7)

    # Matrice des ventes par produit et État
    sales_matrix = fetch_data("/kpi/sales-matrix")
    if sales_matrix:
        df_matrix = pd.DataFrame(sales_matrix)
        st.subheader("Matrice des ventes par produit et État")
        fig8 = px.bar(
            df_matrix, x="_id.State", y="total_sales", color="_id.Product",
            title="Ventes par produit et État",
            labels={"_id.State": "État", "total_sales": "Ventes", "_id.Product": "Produit"}
        )
        st.plotly_chart(fig8)

# Footer
st.markdown("---")