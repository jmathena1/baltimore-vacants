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
    return (vacant_houses_with_owners,)


@app.cell
def _(mo, vacant_houses_with_owners):
    bmore_vacant_owners = mo.sql(
        f"""
        select 
            "NoticeNum",
            "MAILTOADD",
            substr("MAILTOADD", -5) as mailingZip
        from vacant_houses_with_owners
        where mailingZip in (
        '21201',
        '21202',
        '21203',
        '21204',
        '21205',
        '21206',
        '21207',
        '21208',
        '21209',
        '21210',
        '21211',
        '21212',
        '21213',
        '21214',
        '21215',
        '21216',
        '21217',
        '21218',
        '21219',
        '21220',
        '21221',
        '21222',
        '21223',
        '21224',
        '21225',
        '21226',
        '21227',
        '21228',
        '21229',
        '21230',
        '21231',
        '21233',
        '21234',
        '21235',
        '21236',
        '21237',
        '21239',
        '21240',
        '21241',
        '21244',
        '21250',
        '21251',
        '21252',
        '21263',
        '21264',
        '21270',
        '21273',
        '21275',
        '21278',
        '21279',
        '21281',
        '21282',
        '21284',
        '21285',
        '21286',
        '21287',
        '21289',
        '21290',
        '21297',
        '21298')
        """
    )
    return (bmore_vacant_owners,)


@app.cell
def _(bmore_vacant_owners, vacant_houses_with_owners):
    total_vacant_owners_count = vacant_houses_with_owners.shape[0]
    bmore_vacant_owners_count = bmore_vacant_owners.shape[0]
    non_bmore_vacant_owners_count = total_vacant_owners_count - bmore_vacant_owners_count
    local_ownership_rate = (non_bmore_vacant_owners_count / total_vacant_owners_count) * 100

    print(f"""
    {non_bmore_vacant_owners_count} vacant houses in Baltimore are owned by an entity not receiving mail in the city.
    That's {local_ownership_rate} of vacant houses citywide.
    """
    )
    return


if __name__ == "__main__":
    app.run()
