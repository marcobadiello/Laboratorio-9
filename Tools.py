import polars as pl

df = pl.read_csv("earnings-clean.csv")
print(df)