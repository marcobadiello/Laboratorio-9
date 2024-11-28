import altair as alt
import polars as pl
from Tools import df


# Assicurati che la colonna "earnings" sia numerica
df = df.with_columns(pl.col("earnings").cast(pl.Float64))

# Aggregazione: calcolo della media dei guadagni per sesso
gender_earnings = (
    df.group_by("sex")
    .agg(pl.col("earnings").mean().alias("average_earnings"))
    .to_pandas()  # Altair richiede un DataFrame Pandas per il grafico
)

# Creazione del grafico
chart = alt.Chart(gender_earnings).mark_bar().encode(
    x=alt.X('sex', title='Sesso'),
    y=alt.Y('average_earnings', title='Guadagno medio'),
    color='sex'
).properties(
    title='Confronto del guadagno medio per sesso'
)

chart.show()