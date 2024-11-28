import polars as pl
import altair as alt
import streamlit as st

data_name = "earnings-clean.csv"

df = pl.read_csv(data_name)


st.write("Laboratorio 9")
st.write(df)

# Conversione delle colonne necessarie
df = df.with_columns([
    pl.col("earnings").cast(pl.Float64),  # Assicuriamo che earnings sia numerico
    pl.col("year").cast(pl.Int32)         # Assicuriamo che year sia intero
])

# Filtraggio per rimuovere eventuali valori mancanti
df = df.filter(~pl.col("earnings").is_null())

# Aggregazione dei dati: media del reddito per anno e sesso
yearly_earnings = (
    df.group_by(["year", "sex"])
    .agg(pl.col("earnings").mean().alias("average_earnings"))
    .sort("year")
    .to_pandas()  # Altair richiede Pandas
)

# Creazione del grafico Altair
chart = alt.Chart(yearly_earnings).mark_line(point=True).encode(
    x=alt.X("year:O", title="Anno"),
    y=alt.Y("average_earnings:Q", title="Reddito medio"),
    color=alt.Color("sex:N", title="Sesso",scale=alt.Scale(domain=["Female", "Male"], range=["red", "blue"])),
    tooltip=["year", "sex", "average_earnings"]
).properties(
    title="Andamento del reddito medio per sesso negli anni",
    width=700,
    height=400
)

# App Streamlit
st.title("Analisi del Reddito Medio per Sesso negli Anni")
st.altair_chart(chart, use_container_width=True)
