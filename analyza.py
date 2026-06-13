import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Nastavení stránky
st.set_page_config(page_title="AI Analýza recenzí", layout="wide")
st.title("📊 AI Analýza recenzí")

# 2. Načtení dat
# Používáme sep=";" protože v českém textu se často vyskytují čárky
try:
    df = pd.read_csv("recenze.csv", sep=";")
    st.write("### Vaše data:")
    st.dataframe(df)
except FileNotFoundError:
    st.error("Soubor 'recenze.csv' nebyl nalezen. Ujistěte se, že je ve stejné složce jako analyza.py.")
    st.stop()

# 3. Analýza pomocí AI
if st.button("🚀 Spustit analýzu sentimentu"):
    # Kontrola, zda máme klíč v nastavení Streamlitu
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        with st.spinner("AI právě analyzuje recenze..."):
            # Analýza první recenze z tabulky
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
        st.error("API klíč nebyl nalezen. Vložte ho v nastavení aplikace (Secrets) na Streamlitu.")