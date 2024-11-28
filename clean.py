import polars as pl

"""
Data source: https://ec.europa.eu/eurostat/databrowser/view/earn_ses_hourly/default/table?lang=en&category=labour.earn.earn_ses_main
"""

odd_col = "freq,nace_r2,isco08,worktime,age,sex,indic_se,geo\\TIME_PERIOD"
fields = odd_col.replace("\\TIME_PERIOD", "").split(",")

url = "earnings.tsv.gz"
data = (
    pl.read_csv(url, null_values=": ", separator="\t")
    .select(
        pl.col(odd_col).str.split(",").list.to_struct(fields=fields).alias("tmp"),
        pl.col("*").exclude(odd_col)
    )
    .unnest("tmp")
    .unpivot(index=fields, variable_name="year", value_name="earnings")
    .with_columns(
        pl.col("earnings").str.strip_chars_end(" becs:").cast(pl.Float64, strict=False),
        pl.col("year").str.strip_chars_end(" ").cast(pl.Int32),
    )
    .filter(pl.col("sex") != "T")
    .filter(pl.col("age").is_in(["TOTAL", "Y_GE50", "Y_30-49", "Y_LT30", "UNK"]).not_())
    .filter(pl.col("isco08").is_in(["TOTAL", "OC1-5", "OC6-8", "OC7-9"]).not_())
    .filter(pl.col("indic_se") == "MEAN_E_EUR")
    .select(pl.exclude("indic_se", "nace_r2", "freq"))
    .filter(pl.col("worktime") != "TOTAL")
    .select(
        pl.col("worktime").replace({"PT": "Part time", "FT": "Full time"}),
        pl.col("sex").replace({"M": "Male", "F": "Female"}),
        pl.col("isco08").replace({
            "OC1": "Managers",
            "OC2": "Professionals",
            "OC3": "Technicians",
            "OC4": "Clerical support workers",
            "OC5": "Service and sales workers",
            "OC6": "Skilled agricultural, forestry and fishery workers",
            "OC7": "Craft and related trades workers",
            "OC8": "Plant and machine operators and assemblers",
            "OC9": "Elementary occupations",
            "OC0": "Armed forces occupations"
        }).alias("occupation"),
        pl.col("earnings", "year", "geo", "age")
    )
)

data.write_csv("earnings-clean.csv")

