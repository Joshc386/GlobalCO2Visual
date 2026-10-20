"""Rebuild the dashboard's data files from the original CO2 dataset.

Usage (from the repository root):
    pip install pandas pycountry pycountry-convert
    python scripts/prepare_data.py path/to/visualizing_global_co2_data.csv

Writes data/country_emissions.csv, data/continent_emissions.csv and
data/country_continents.csv. data/country_shapes.json (country outlines) is
not rebuilt here: it comes from Natural Earth 1:50m via world-atlas 2.0.2,
projected to Equal Earth with d3-geo.
"""
import sys
from pathlib import Path

import pandas as pd
import pycountry
import pycountry_convert as pcc

CONTINENTS = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]
CODE_TO_NAME = {"AF": "Africa", "AS": "Asia", "EU": "Europe", "NA": "North America",
                "SA": "South America", "OC": "Oceania"}
# Codes the converter doesn't know, set by hand
MANUAL = {"OWID_KOS": "Europe", "TLS": "Asia", "SXM": "North America", "BES": "North America",
          "CUW": "North America", "ESH": "Africa", "VAT": "Europe", "ANT": "North America",
          "CXR": "Asia", "ATA": None}


def continent_for(iso: str):
    if iso in MANUAL:
        return MANUAL[iso]
    try:
        alpha2 = pycountry.countries.get(alpha_3=iso).alpha_2
        return CODE_TO_NAME.get(pcc.country_alpha2_to_continent_code(alpha2))
    except (AttributeError, KeyError):
        return None


def main(src: str) -> None:
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    df = pd.read_csv(src)

    # Kosovo has no ISO code in the source; give it Our World in Data's code so it maps
    df.loc[df["country"] == "Kosovo", "iso_code"] = "OWID_KOS"

    countries = df[df["iso_code"].notna() & df["co2"].notna()][
        ["country", "iso_code", "year", "population", "co2", "co2_per_capita",
         "share_global_co2", "cumulative_co2"]
    ].copy()
    countries["population"] = countries["population"].round(0).astype("Int64")
    countries.to_csv(out / "country_emissions.csv", index=False)

    continents = df[df["country"].isin(CONTINENTS)][["country", "year", "co2"]]
    continents.rename(columns={"country": "continent"}).to_csv(out / "continent_emissions.csv", index=False)

    lookup = countries.drop_duplicates("iso_code")[["iso_code", "country"]].copy()
    lookup["continent"] = lookup["iso_code"].map(continent_for)
    lookup = lookup[lookup["continent"].notna()]
    lookup.to_csv(out / "country_continents.csv", index=False)

    # Sanity check: country sums by continent should match the file's continent rows
    merged = countries.merge(lookup[["iso_code", "continent"]], on="iso_code")
    latest = int(continents["year"].max())
    ours = merged[merged["year"] == latest].groupby("continent")["co2"].sum()
    theirs = continents[continents["year"] == latest].set_index("country")["co2"]
    print(f"{len(countries):,} country rows, {lookup.shape[0]} countries with a continent")
    print(f"Country sums vs continent rows in {latest}:")
    print((ours / theirs).round(3).to_string())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/prepare_data.py path/to/visualizing_global_co2_data.csv")
    main(sys.argv[1])
