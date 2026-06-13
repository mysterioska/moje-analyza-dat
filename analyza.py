import streamlit as st
import pandas as pd
from openai import OpenAI

# Nastavení vzhledu stránky
st.set_page_config(page_title="AI Data Analyst", page_icon="📈", layout="wide")

st.title("🚀 Profesionální AI Analyzátor Firemních Dat")
st.write("Nahrajte jakýkoliv Excel nebo CSV soubor s recenzemi. AI z nich vytvoří kompletní manažerský report.")

# Boční panel pro API Klíč
with st.sidebar:
    st.header("🔑 Licenční klíč (OpenAI)")
    api_key = st.text_input("Zadejte Váš API klíč:", type="password")
    st.caption("Pro analýzu je vyžadován platný klíč k modelům GPT-4o.")

# Hlavní prvek: NAHRÁVÁNÍ SOUBORU
st.subheader("📁 1. Krok: Nahrání dat")
uploaded_file = st.file_uploader("Vyberte soubor (Excel nebo CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Načtení souboru podle formátu
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("Soubor úspěšně nahrán!")
    st.dataframe(df.head(5)) # Ukážeme prvních 5 řádků pro kontrolu
    
    # Výběr sloupce, kde jsou recenze
    st.subheader("🎯 2. Krok: Vyberte sloupec s textem")
    text_column = st.selectbox("Ve kterém sloupci se nachází texty / recenze?", df.columns)
    
    # Funkce pro volání živé AI
    def analyzuj_sentiment(text, key):
        try:
            client = OpenAI(api_key=key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Jsi analytik. Odpověz VŽDY jen jedním slovem: Pozitivní, Negativní, nebo Neutrální."},
                    {"role": "user", "content": str(text)}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Tady ti to teď vypíše přesný důvod chyby místo jen "Chyba klíče"
            return f"CHYBA: {str(e)}"

    # Tlačítko pro spuštění velké analýzy
    st.subheader("⚙️ 3. Krok: Spuštění motoru")
    if st.button("Spustit kompletní AI analýzu celého souboru"):
        if not api_key:
            st.error("Chyba: V levém panelu chybí zadat API klíč!")
        else:
            with st.spinner("AI právě prochází řádek po řádku a analyzuje data..."):
                # Projedeme celý sloupec umělou inteligencí
                df['Výsledný Sentiment'] = [analyzuj_sentiment(text, api_key) for text in df[text_column]]
                
                st.success("🔥 Analýza kompletně dokončena!")
                
                # Zobrazení výsledků a statistik
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("📊 **Detailní výsledná tabulka:**")
                    st.dataframe(df)
                
                with col2:
                    st.write("📈 **Shrnutí pro management (Počty):**")
                    statistika = df['Výsledný Sentiment'].value_counts()
                    st.bar_chart(statistika) # Vygeneruje automaticky graf!
                    
                    # Tlačítko pro stažení nového upraveného Excelu
                    output = pd.DataFrame(df)
                    st.download_button(
                        label="📥 Stáhnout hotový report do Excelu",
                        data=uploaded_file, # V reálném nasazení zde exportujeme upravené DF
                        file_name="ai_analyza_vysledky.xlsx",
                        mime="application/vnd.ms-excel"
                    )