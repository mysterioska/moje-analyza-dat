import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Nastavení vzhledu stránky
st.set_page_config(page_title="Analýza recenzí AI", layout="wide")
st.title("📊 AI Analýza recenzí")

# 2. Načtení dat
# Ujistěte se, že soubor recenze.csv je ve stejné složce jako analyza.py
try:
    df = pd.read_csv("recenze.csv")
    st.write("### Vaše data:")
    st.dataframe(df)
except FileNotFoundError:
    st.error("Soubor 'recenze.csv' nebyl nalezen. Nahrajte ho do složky projektu.")
    st.stop() # Zastaví vykonávání kódu, pokud data chybí

# 3. Analýza pomocí AI
if st.button("🚀 Spustit analýzu sentimentu"):
    # Kontrola, zda máme klíč v Secrets (v nastavení Streamlitu)
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        with st.spinner("AI právě analyzuje recenze..."):
            # Vezmeme první recenzi jako příklad
            text = df["recenze"].iloc[0]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Jsi analytik. Urči sentiment recenze a stručně vysvětli proč."},
                    {"role": "user", "content": f"Analyzuj tuto recenzi: {text}"}
                ]
            )
            
            st.subheader("Výsledek analýzy:")
            st.success(response.choices[0].message.content)
    else:
        st.error("Chybí API klíč v Secrets. Vložte ho v nastavení aplikace na Streamlitu.")