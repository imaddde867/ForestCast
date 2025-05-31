import earthaccess
import pandas as pd
from datetime import datetime
import json

class DataExplorer:
    """
    This class helps us understand what data is available before we commit 
    to downloading gigabytes of satellite imagery. Think of it as our 
    reconnaissance mission.
    """
    
    def __init__(self):
        # Login as guest 
        print("🚀 Connecting to NASA Earthdata...")
        earthaccess.login(strategy="guest")
        print("✅ Connected successfully!")
    
    def explore_landsat_collections(self):
        """
        Landsat satellites have been taking pictures of Earth since the 1970s.
        Different Landsat missions have different capabilities and time periods.
        We need to understand which one gives us the best bang for our buck.
        """
        print("\n📡 Exploring Landsat Collections...")
        
        # These are the main Landsat collections we care about
        landsat_collections = [
            "LANDSAT_7_C2_L2",  # 1999-present, some data gaps due to sensor issues
            "LANDSAT_8_C2_L2",  # 2013-present, excellent quality
            "LANDSAT_9_C2_L2"   # 2021-present, newest and best
        ]
        
        for collection_name in landsat_collections:
            print(f"\n--- Investigating {collection_name} ---")
            
            # Let's search for a small area to understand data availability
            # Using a known deforestation hotspot in the Amazon for testing
            test_bbox = (-60.5, -9.5, -60.0, -9.0)  # Small 0.5x0.5 degree box
            
            try:
                # Search for recent data in this area
                results = earthaccess.search_data(
                    short_name=collection_name,
                    bounding_box=test_bbox,
                    temporal=("2020-01-01", "2023-12-31"),
                    cloud_cover=(0, 30),  # Only scenes with <30% cloud cover
                    count=5  # Just get 5 examples to examine
                )
                
                print(f"Found {len(results)} scenes with <30% cloud cover")
                
                if results:
                    # Examine the first result to understand metadata structure
                    sample = results[0]
                    self._analyze_sample_metadata(sample, collection_name)
                    
            except Exception as e:
                print(f"❌ Error accessing {collection_name}: {e}")
        
    def _analyze_sample_metadata(self, sample, collection_name):
        """
        This is crucial for data engineers - understanding metadata structure
        helps us know what features we can extract later for our ML model.
        """
        print(f"🔍 Sample metadata analysis for {collection_name}:")
        
        # Key metadata fields that will become features in our ML model
        important_fields = {
            'temporal': 'When was this image taken?',
            'cloud_cover': 'How much of the image is blocked by clouds?',
            'size': 'How big is this file?',
            'producer_granule_id': 'Unique identifier for this scene'
        }
        
        for field, description in important_fields.items():
            value = sample.get(field, 'Not available')
            print(f"  • {field}: {value} ({description})")