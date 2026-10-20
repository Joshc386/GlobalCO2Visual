# Global CO₂ Emissions, 1750–2021

An interactive dashboard of annual CO₂ emissions by country and continent, built with D3.js.

**Live dashboard:** https://joshc386.github.io/GlobalCO2Visual/

![Dashboard preview](docs/preview.png)

## What's in it

| Visual | What it shows | Interaction |
|---|---|---|
| Annual emissions map | Each country shaded by its annual CO₂ (log colour scale, fixed across years) | Year slider, play, hover for figures, click to highlight |
| Per person map | CO₂ per person per year | Year slider, play, hover, click to highlight |
| Country rankings | Rank, annual CO₂, share of world, CO₂ per person, 10-year change | Year slider, sort, search, filter out countries under 1 million people |
| Top 20 over time | Animated bar chart race of each country's share of world CO₂ | Play, speed, year slider; bars coloured by continent |
| By continent | Annual CO₂ for six continents | Drag a window to pick the year range, toggle continents |
| Cartogram | Countries as circles sized by CO₂ (Dorling cartogram) | Single year or all years combined, play, rescale |

Clicking a country on a map, a table row, a circle or a bar highlights it across every chart.

## Data

- **Emissions:** CO₂ from fossil fuels and industry, excluding land-use change, 1750–2021. The columns follow Our World in Data's CO₂ dataset (CC BY 4.0).
- **Country outlines:** Natural Earth 1:50m via [world-atlas](https://github.com/topojson/world-atlas), projected to Equal Earth with d3-geo. Antarctica is left out.
- **Continents:** each country is assigned a continent with `pycountry-convert` (plus a few manual codes). Country totals by continent match the dataset's own continent rows to within 0.1%.

`scripts/prepare_data.py` rebuilds the CSVs in `data/` from the original dataset:

```bash
pip install pandas pycountry pycountry-convert
python scripts/prepare_data.py path/to/visualizing_global_co2_data.csv
```

### Things to know when reading the charts

- Colour scales are logarithmic, so each step in shade is a tenfold change.
- Maps use present-day borders throughout.
- Continent totals exclude international aviation and shipping, which the dataset doesn't assign to a continent. "Share of world" is measured against a world total that includes them.
- The per-person colour scale is capped, because a few tiny territories, such as Sint Maarten in the 1950s, have extreme values.

## Run it locally

Browsers block data files opened straight from disk, so serve the folder:

```bash
python -m http.server
```

Then open http://localhost:8000.

## Built with

[D3.js](https://d3js.org) v7 (bundled in `lib/`), plain HTML, CSS and JavaScript. No build step.
