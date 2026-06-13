import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Analýza recenzí", layout="wide")
st.title("📊 Profesionální AI Analýza")

uploaded_file = st.file_uploader("Nahrajte svůj CSV soubor (oddělený středníkem)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";")
    st.dataframe(df)

    if st.button("🚀 Spustit hloubkovou analýzu"):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Příprava seznamů pro nové sloupce
        sentiments, temata, shrnuti, navrhy = [], [], [], []

        with st.spinner("Analýza probíhá..."):
            for text in df["recenze"]:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Jsi analytik. Vrať odpověď POUZE v tomto formátu odděleném svislítkem (|): Sentiment|Téma|Shrnutí|Návrh"},
                        {"role": "user", "content": f"Analyzuj tuto recenzi: {text}"}
                    ]
                )
                # Rozdělení odpovědi podle svislítka
                data = response.choices[0].message.content.split("|")
                if len(data) == 4:
                    sentiments.append(data[0])
                    temata.append(data[1])
                    shrnuti.append(data[2])
                    navrhy.append(data[3])
                else:
                    sentiments.append("Chyba"); temata.append("-"); shrnuti.append("-"); navrhy.append("-")

        # Vytvoření nové tabulky
        df["Sentiment"] = sentiments
        df["Téma"] = temata
        df["Shrnutí"] = shrnuti
        df["Návrh"] = navrhy
        
        st.subheader("Výsledky analýzy:")
        st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Stáhnout výsledky jako CSV", csv, "report.csv", "text/csv")