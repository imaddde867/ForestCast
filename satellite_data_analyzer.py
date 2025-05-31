import earthaccess
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class SatelliteDataAnalyzer:
    """
    This class helps us understand the structure and characteristics of 
    satellite imagery. Think of each satellite image like a multi-layered 
    cake - each layer captures different types of light.
    """
    
    def __init__(self):
        earthaccess.login(strategy="guest")
        
    def understand_landsat_bands(self):
        """
        Landsat doesn't just take regular photos. It captures multiple 
        'bands' of light - including invisible light that plants reflect 
        differently when they're healthy vs stressed.
        
        This is like having super-vision that can see plant health!
        """
        print("Understanding Landsat Spectral Bands...")
        
        landsat_bands = {
            'Band 1 (Coastal/Aerosol)': 'Helps with atmospheric correction',
            'Band 2 (Blue)': 'Water detection, atmospheric scattering',
            'Band 3 (Green)': 'Peak vegetation sensitivity', 
            'Band 4 (Red)': 'Chlorophyll absorption (healthy plants absorb red light)',
            'Band 5 (Near-IR)': 'Vegetation health (healthy plants reflect near-infrared)',
            'Band 6 (SWIR-1)': 'Moisture content in soil and vegetation',
            'Band 7 (SWIR-2)': 'Rock/mineral identification, fires'
        }
        
        print("\nEach Landsat image contains these information layers:")
        for band, purpose in landsat_bands.items():
            print(f"  • {band}: {purpose}")
            
        print("\n💡 Key insight for ML: The magic happens when we combine bands!")
        print("   NDVI = (Near-IR - Red) / (Near-IR + Red)")
        print("   This formula reveals vegetation health that human eyes can't see.")
        
    def download_and_analyze_sample(self):
        """
        Let's download one small satellite image and examine its structure.
        This teaches us how to handle the data format we'll be working with.
        """
        print("\n📥 Downloading sample Landsat scene for analysis...")
        
        # Search for a recent, clear image over a known forest area
        results = earthaccess.search_data(
            short_name="LANDSAT_8_C2_L2",
            bounding_box=(-60.2, -9.2, -60.0, -9.0),  # Small Amazon area
            temporal=("2023-06-01", "2023-08-31"),     # Dry season (less clouds)
            cloud_cover=(0, 10),  # Very clear images only
            count=1
        )
        
        if not results:
            print("❌ No clear images found. Try expanding the search area or time range.")
            return
            
        print(f"✅ Found {len(results)} suitable images")
        
        # Download the first result
        downloaded_files = earthaccess.download(results, "./data/sample/")
        
        if downloaded_files:
            self._analyze_downloaded_image(downloaded_files[0])
    
    def _analyze_downloaded_image(self, filepath):
        """
        This is where data engineering meets remote sensing. We're learning
        how to read and interpret the raw satellite data files.
        """
        print(f"\n🔬 Analyzing downloaded image: {filepath}")
        
        try:
            with rasterio.open(filepath) as src:
                print(f"Image dimensions: {src.width} x {src.height} pixels")
                print(f"Number of bands: {src.count}")
                print(f"Coordinate system: {src.crs}")
                print(f"Pixel resolution: {src.res} (degrees)")
                
                # Convert to meters (approximately)
                meters_per_pixel = src.res[0] * 111000  # Rough conversion
                print(f"Approximate resolution: {meters_per_pixel:.0f} meters per pixel")
                
                # Read a small subset to understand data values
                # Reading just a 100x100 pixel area to keep things manageable
                sample_data = src.read(window=((0, 100), (0, 100)))
                
                print(f"\nData value ranges (this tells us about data quality):")
                for band_idx in range(min(4, src.count)):  # Just show first 4 bands
                    band_data = sample_data[band_idx]
                    print(f"  Band {band_idx + 1}: {band_data.min():.0f} to {band_data.max():.0f}")
                    
                # Calculate NDVI for this sample area
                if src.count >= 5:  # Need at least 5 bands for NDVI
                    self._calculate_sample_ndvi(sample_data)
                    
        except Exception as e:
            print(f"❌ Error analyzing image: {e}")
    
    def _calculate_sample_ndvi(self, sample_data):
        """
        NDVI (Normalized Difference Vegetation Index) is our first ML feature!
        This shows how to transform raw satellite data into meaningful information.
        """
        print("\n🌿 Calculating NDVI (Vegetation Health Index)...")
        
        # For Landsat 8 Surface Reflectance:
        # Band 4 = Red, Band 5 = Near-Infrared
        red_band = sample_data[3].astype(float)    # Band 4 (index 3)
        nir_band = sample_data[4].astype(float)    # Band 5 (index 4)
        
        # Avoid division by zero
        denominator = nir_band + red_band
        ndvi = np.where(denominator != 0, 
                       (nir_band - red_band) / denominator, 
                       0)
        
        print(f"NDVI range: {ndvi.min():.3f} to {ndvi.max():.3f}")
        print("NDVI interpretation:")
        print("  • -1.0 to 0.1: Water, bare soil, rocks")
        print("  • 0.1 to 0.3: Sparse vegetation, grassland")  
        print("  • 0.3 to 0.8: Dense vegetation, healthy forest")
        
        # This NDVI calculation will become a core feature in our ML model
        avg_ndvi = np.mean(ndvi[ndvi > -1])  # Exclude invalid pixels
        print(f"Average NDVI for this area: {avg_ndvi:.3f}")
        
        if avg_ndvi > 0.5:
            print("✅ This appears to be healthy forest!")
        elif avg_ndvi > 0.3:
            print("🌾 This appears to be moderate vegetation")
        else:
            print("🏜️ This appears to be sparse vegetation or non-vegetated")