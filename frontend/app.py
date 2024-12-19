import streamlit as st
from st_pages import get_nav_from_toml, add_page_title

st.set_page_config(page_title="Page d'Accueil")
st.title("Test")

# st.set_page_config(layout="wide")
# nav = get_nav_from_toml(".streamlit/pages_sections.toml")
# pg = st.navigation(nav)
# add_page_title(pg)
# pg.run()

# nav = get_nav_from_toml(".streamlit/pages_sections.toml")

# if not nav:
#     st.error("Aucune page trouvée dans la configuration de navigation.")
# else:
#     pg = st.navigation(nav)
#     add_page_title(pg)
#     pg.run()