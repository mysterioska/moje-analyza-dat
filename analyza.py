import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Analýza recenzí", layout="wide")
st.title("📊 AI Analýza recenzí")

uploaded_file = st.file_uploader("Nahrajte svůj CSV soubor (oddělený středníkem)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";")
    st.write("### Vaše nahraná data:")
    st.dataframe(df)

    if st.button("🚀 Spustit hromadnou analýzu"):
        if "OPENAI_API_KEY" in st.secrets:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            results = []

            with st.spinner("AI analyzuje všechny recenze..."):
                for index, row in df.iterrows():
                    text = row["recenze"]
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Jsi analytik. Vrať výsledek v tomto formátu: Sentiment (Pozitivní/Negativní), Téma, Shrnutí. Odděluj čárkou."},
                            {"role": "user", "content": f"Analyzuj: {text}"}
                        ]
                    )
                    results.append(response.choices[0].message.content)

                # Přidání výsledků do tabulky
                df["Analýza"] = results
                st.subheader("Výsledky analýzy:")
                st.dataframe(df)
                
                # Možnost stažení výsledků
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Stáhnout výsledky jako CSV", csv, "analyza_vysledky.csv", "text/csv")
        else:
            st.error("API klíč nebyl nalezen v Secrets.")
else:
    st.info("Prosím, nahrajte CSV soubor.")