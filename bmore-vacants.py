import marimo

__generated_with = "0.14.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Who owns the vacant homes in Baltimore?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    There are about 12,500 vacant homes in Baltimore City, according to the Mayor's office. 

    City, state, and federal entities own about 1,000 of those houses. So who owns the rest?

    Thanks to Open Baltimore data, we can filter the [Vacant Building Notices](https://data.baltimorecity.gov/datasets/691d65a5f85640e6aaa46930bd9dc102_1/explore?location=39.296383%2C-76.620458%2C11.51&showTable=true) (VBNs) dataset with the city's [Real Property Information](https://data.baltimorecity.gov/datasets/baltimore::real-property-information-2/explore?location=39.294088%2C-76.628072%2C14.18&showTable=true) to gather mailing addresses on file for all vacant homes.
    """
    )
    return


@app.cell
def _(mo):
    vacant_houses = mo.sql(
        f"""
        select * from 'raw-data/vacant_building_notices.csv'
        """,
        output=False
    )
    return (vacant_houses,)


@app.cell
def _(mo):
    real_property_data = mo.sql(
        f"""
        select * from 'raw-data/real_property_data.csv'
        """,
        output=False
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
        """,
        output=False
    )
    return (vacant_houses_with_owners,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Data Collection and Wrangling

    I downloaded the VBNs and Real Property data as CSVs to make my life easier, and because those datasets aren't updated that often. I downloaded them both on 6/27/2025. 

    The real property data is very wide (~200 columns, I think?), so I only kept the mailing address and block lot columns; the block lot is shared between datasets and allows me to connect a vacant home to an owner (or at least a mailbox where someone can reach the owner).

    In the above 3 cells, I read the two CSVs into DuckDB tables and join them on the `BLOCKLOT` column.
    """
    )
    return


@app.cell
def _(mo, vacant_houses_with_owners):
    bmore_vacant_owners = mo.sql(
        f"""
        select 
            "NoticeNum",
            "MAILTOADD",
            substr("MAILTOADD", -5) as mailingZip,
            regexp_matches(vacant_houses_with_owners."MAILTOADD", 'P.*\\s*O.*\\s*BOX') as poBox
        from vacant_houses_with_owners
        where
            poBox = false
            and mailingZip in (
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
            '21298'
            )
        """,
        output=False
    )
    return (bmore_vacant_owners,)


@app.cell
def _(bmore_vacant_owners, vacant_houses_with_owners):
    total_vacant_owners_count = vacant_houses_with_owners.shape[0]
    bmore_vacant_owners_count = bmore_vacant_owners.shape[0]
    non_bmore_vacant_owners_count = total_vacant_owners_count - bmore_vacant_owners_count
    local_ownership_rate = round((bmore_vacant_owners_count / total_vacant_owners_count) * 100, 2)
    return bmore_vacant_owners_count, local_ownership_rate


@app.cell
def _(bmore_vacant_owners_count, local_ownership_rate, mo):
    mo.md(
        rf"""
    ## Analysis

    I grabbed Baltimore area zip codes from [Zip Codes.com](https://www.zip-codes.com/city/md-baltimore.asp). Now this will technically pull some county addresses, but I'm just trying to see who may own these vacants and is still in the area so I'm good with that for now.

    Next, I extracted the zip code from the mailing address listed for each vacant home by pulling the last five values in each address string. I eyeballed the data and it looked like that was always the zip code.

    Finally, I checked if the mailing address zip code lived in our Baltimore area zip code list and attempted to filter out PO Boxes with a regular expression.

    **So by my count, {bmore_vacant_owners_count} vacant houses in Baltimore are owned by an entity with a mailing address nearby.**

    **That's {local_ownership_rate}% of vacant houses citywide.**

    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Discussion

    ### That's a lot of locals!
    I mean don't get me wrong, Baltimore has struggled with population loss and vacant housing for most of my life and it is not great that more than a third of the vacant houses aren't even owned by people who live 'round here.

    But, it's almost worse that most the people sitting on thoses houses *are* from 'round here! Can y'all help us out??

    ### How accurate are these mailing addresses?
    I do not know how the city adds these addresses to the real property records. It is possible that out of town developers are using someone local to hide the fact that they are doing nothing with houses that could use some love. I know for a fact that when homeowners die, it can take the city and state a *very* long to update the owner and point of contact for a property if it is no longet, owner occupied. But, vacants may have a more stringent process and I did try to eliminate PO Boxes.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Futher reading on vacant homes in Baltimore
    - [Addressing Baltimore's Vacant Properties at Scale](https://storymaps.arcgis.com/stories/19ae8270476740408f3ec603a3c6e92d)
    - [Baltimore City's Vacant Housing Dashboard](https://app.powerbigov.us/view?r=eyJrIjoiOThlNTVkNGEtMWYyOC00Y2FlLTg0ODEtMDRhODEzNTFjMWJmIiwidCI6IjMxMmNiMTI2LWM2YWUtNGZjMi04MDBkLTMxOGU2NzljZTZjNyJ9&pageName=ReportSection)
    - [Whole Blocks, Whole City: Reclaiming Vacant Property Throughout Baltimore](https://rebuildmetro.com/wp-content/uploads/2024/05/ReBUILD-Metro_Whole-Blocks-Whole-City-sml.pdf)
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
