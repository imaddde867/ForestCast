import ee
import ee.mapclient
import os
import requests

# Initialize the Earth Engine library.
ee.Initialize(project='forestcast')

# Define the area of interest (AOI) as a rectangle over the Amazon.
aoi = ee.Geometry.Rectangle([-60, -10, -50, 0])

# Define the grid size.
grid_size = 8

# Get the coordinates of the AOI.
coords = aoi.coordinates().get(0).getInfo()
min_lon, min_lat = coords[0]
max_lon, max_lat = coords[2]

# Calculate the size of each grid cell.
lon_step = (max_lon - min_lon) / grid_size
lat_step = (max_lat - min_lat) / grid_size

# Create a directory to store the data.
if not os.path.exists('data'):
    os.makedirs('data')

# Loop through the grid and download the images.
for i in range(grid_size):
    for j in range(grid_size):
        # Define the cell AOI.
        cell_min_lon = min_lon + i * lon_step
        cell_max_lon = min_lon + (i + 1) * lon_step
        cell_min_lat = min_lat + j * lat_step
        cell_max_lat = min_lat + (j + 1) * lat_step
        cell_aoi = ee.Geometry.Rectangle([cell_min_lon, cell_min_lat, cell_max_lon, cell_max_lat])

        # Load the Landsat 8 image collection.
        landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')

        # Filter the collection by date and location.
        image = landsat.filterBounds(cell_aoi) \
                       .filterDate('2019-01-01', '2019-12-31') \
                       .sort('CLOUD_COVER') \
                       .first()

        # Select the RGB and NIR bands.
        bands = ['SR_B4', 'SR_B3', 'SR_B2', 'SR_B5']
        image = image.select(bands)

        # Clip the image to the cell AOI.
        image = image.clip(cell_aoi)

        # Create a URL to download the image.
        url = image.getDownloadURL({
            'scale': 100,
            'crs': 'EPSG:4326',
            'region': cell_aoi.toGeoJSONString()
        })

        # Download the image data.
        response = requests.get(url)

        # Save the image to a file.
        with open(f'data/amazon_image_{i}_{j}.zip', 'wb') as f:
            f.write(response.content)

        print(f"Image for cell ({i}, {j}) downloaded successfully.")
