import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Nastavení stránky
st.set_page_config(page_title="AI Analýza recenzí", layout="wide")
st.title("📊 AI Analýza recenzí")

# 2. Nahrávání souboru uživatelem
uploaded_file = st.file_uploader("Nahrajte svůj CSV soubor (oddělený středníkem)", type=["csv"])

# 3. Zpracování dat a analýza
if uploaded_file is not None:
    # Načtení dat ze nahraného souboru
    df = pd.read_csv(uploaded_file, sep=";")
    st.write("### Vaše nahraná data:")
    st.dataframe(df)

    # Tlačítko pro analýzu
    if st.button("🚀 Spustit analýzu sentimentu"):
        if "OPENAI_API_KEY" in st.secrets:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            with st.spinner("AI právě analyzuje recenze..."):
                # Analýza první recenze (lze rozšířit na všechny)
                text = df["recenze"].iloc[0]
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Jsi analytik. Urči sentiment recenze (pozitivní/negativní) a stručně vysvětli proč."},
                        {"role": "user", "content": f"Analyzuj tuto recenzi: {text}"}
                    ]
                )
                
                st.subheader("Výsledek analýzy první recenze:")
                st.success(response.choices[0].message.content)
        else:
            st.error("API klíč nebyl nalezen v Secrets.")
else:
    st.info("Prosím, nahrajte CSV soubor pro zahájení analýzy.")