import marimo

__generated_with = "0.14.6"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""Here we're gonna combine the vacant houses data set with real property so we don't have to do it on deploy. Too much memory!""")
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl

    data_path = mo.notebook_location() / "raw-data"
    vacant_building_notices_df = pl.read_csv(str(data_path / "vacant_building_notices.csv"))
    real_property_data_df = pl.read_csv(
        str(data_path / "real_property_data.csv"),
        infer_schema_length=10000
    )
    vacant_houses_with_owners_df = vacant_building_notices_df.join(
        real_property_data_df,
        on="BLOCKLOT",
        how="left"
    )

    vacant_houses_with_owners_df.write_csv(str(data_path / "vacant_houses_with_owners.csv"), separator=",")
    return (mo,)


if __name__ == "__main__":
    app.run()
