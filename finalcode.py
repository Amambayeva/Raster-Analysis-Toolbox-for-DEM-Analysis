import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import os

# Step 1: Load the DEM raster
dem_path = r"C:\Users\Lenovo\Desktop\dataIP\Merge_file.tif"  # Replace with your DEM file path
with rasterio.open(dem_path) as src:
    dem = src.read(1)  # Read the first band
    profile = src.profile  # Save the metadata (profile) for later use

# Output directory for saving maps
output_dir =r"C:\Users\Lenovo\Desktop\dataIP\Output_Maps"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Function to save maps with layouts, legends, and titles
def save_map(data, title, cmap, output_path, label="Value", vmin=None, vmax=None):
    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(label=label, shrink=0.7)
    cbar.ax.tick_params(labelsize=12)  # Adjust colorbar font size
    plt.title(title, fontsize=16, pad=20)  # Add title with padding
    plt.axis("off")  # Hide axes
    plt.tight_layout()  # Adjust layout
    plt.savefig(output_path, dpi=300, bbox_inches="tight")  # Save as high-resolution image
    plt.close()

# Step 2: Visualize and save DEM map
save_map(dem, "Digital Elevation Model (DEM)", "terrain", os.path.join(output_dir, "DEM.png"), label="Elevation (m)")

# Step 3: Calculate Slope
def calculate_slope(dem, cell_size):
    x, y = np.gradient(dem, cell_size, cell_size)
    slope = np.degrees(np.arctan(np.sqrt(x**2 + y**2)))
    return slope

cell_size = 30  # Adjust based on your DEM resolution
slope = calculate_slope(dem, cell_size)

# Save Slope map
save_map(slope, "Slope Map", "viridis", os.path.join(output_dir, "Slope.png"), label="Slope (degrees)", vmin=0, vmax=90)

# Step 4: Calculate Aspect
def calculate_aspect(dem, cell_size):
    x, y = np.gradient(dem, cell_size, cell_size)
    aspect = np.degrees(np.arctan2(-y, x))
    aspect = (aspect + 360) % 360  # Convert to 0-360 degrees
    return aspect

aspect = calculate_aspect(dem, cell_size)

# Save Aspect map
save_map(aspect, "Aspect Map", "hsv", os.path.join(output_dir, "Aspect.png"), label="Aspect (degrees)", vmin=0, vmax=360)

# Step 5: Calculate Hillshade
def calculate_hillshade(dem, cell_size, azimuth=315, altitude=45):
    x, y = np.gradient(dem, cell_size, cell_size)
    azimuth_rad = np.radians(azimuth)
    altitude_rad = np.radians(altitude)
    hillshade = (np.cos(altitude_rad) * np.cos(np.arctan(np.sqrt(x**2 + y**2)))) + \
                (np.sin(altitude_rad) * np.sin(np.arctan(np.sqrt(x**2 + y**2))) * \
                 np.cos(azimuth_rad - np.arctan2(-y, x)))
    hillshade = 255 * (hillshade + 1) / 2  # Scale to 0-255
    return hillshade

hillshade = calculate_hillshade(dem, cell_size)

# Save Hillshade map
save_map(hillshade, "Hillshade Map", "gray", os.path.join(output_dir, "Hillshade.png"), label="Hillshade")

# Step 6: Extract Contours
def extract_contours(dem, interval=50):
    contours = plt.contour(dem, levels=np.arange(dem.min(), dem.max(), interval), colors="black")
    return contours

# Save Contour map
plt.figure(figsize=(10, 8))
plt.imshow(dem, cmap="terrain")
contours = extract_contours(dem)
plt.colorbar(label="Elevation (m)", shrink=0.7)
plt.title("Contour Map", fontsize=16, pad=20)
plt.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Contour.png"), dpi=300, bbox_inches="tight")
plt.close()

# Step 7: Save Slope, Aspect, and Hillshade as GeoTIFF
def save_raster(data, profile, output_path):
    profile.update(dtype=data.dtype, count=1)
    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(data, 1)

save_raster(slope, profile, os.path.join(output_dir, "slope.tif"))  # Save slope
save_raster(aspect, profile, os.path.join(output_dir, "aspect.tif"))  # Save aspect
save_raster(hillshade, profile, os.path.join(output_dir, "hillshade.tif"))  # Save hillshade

print(r"All results saved to "C:\Users\Lenovo\Desktop\dataIP\Output_Maps"!")  # Use raw string for file path
