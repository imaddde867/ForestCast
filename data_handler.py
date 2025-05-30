from pystac_client import Client
from planetary_computer import sign
import stackstac
import rasterio
import numpy as np

def search_imagery(lat, lon, start_date="2018-01-01", end_date="2023-01-01"):
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=[lon-0.01, lat-0.01, lon+0.01, lat+0.01],
        datetime=f"{start_date}/{end_date}",
        query={"eo:cloud_cover": {"lt": 10}},
        limit=5
    )
    
    items = list(search.items())
    items = [sign(item) for item in items]
    return items

items = search_imagery(
    60.46110618265409, 22.288990538429076,
    start_date="2018-01-01", end_date="2023-01-01"
)

for item in items:
    print(f"ID: {item.id}")
    print(f"Date: {item.datetime}")
    print(f"Cloud Cover: {item.properties.get('eo:cloud_cover', 'N/A')}")
    print(f"Assets: {list(item.assets.keys())}")
    print("-" * 40)