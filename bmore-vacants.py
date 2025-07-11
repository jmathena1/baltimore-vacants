import marimo

__generated_with = "0.14.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    vacant_houses = mo.sql(
        f"""
        select * from 'raw-data/vacant_building_notices.csv'
        """
    )
    return (vacant_houses,)


@app.cell
def _(mo):
    real_property_data = mo.sql(
        f"""
        select * from 'raw-data/real_property_data.csv'
        """
    )
    return (real_property_data,)


@app.cell
def _(mo, real_property_data, vacant_houses):
    vacant_houses_with_owners = mo.sql(
        f"""
        select
            v.*,
            r.*
        from vacant_houses as v
        join real_property_data as r on v."BLOCKLOT" = r."BLOCKLOT"
        """
    )
    return


if __name__ == "__main__":
    app.run()
