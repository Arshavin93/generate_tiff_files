import subprocess
import sys

def run_python_script(script_name):
    """Run the Python script to generate the GeoTIFF file."""
    subprocess.run(['python3', script_name])

def clip_geotiff(input_tif, output_clip_tif):
    """Clip the generated GeoTIFF file using gdalwarp."""
    subprocess.run(['gdalwarp', '-te', '-0.09940', '-0.06140', '1.73860', '1.0486' , input_tif, output_clip_tif]) # , '-tr', '0.003', '0.002'

def compress_geotiff(input_tif, output_compressed_tif):
    """Compress the clipped GeoTIFF file using gdal_translate."""
    subprocess.run(['gdal_translate', '-co', 'COMPRESS=DEFLATE', '-co', 'ZLEVEL=9', input_tif, output_compressed_tif])

def main():
    #if len(sys.argv) < 2:
     #   print("Usage: python script.py <filename.py>")
      #  sys.exit(1)

    # Run the Python script to generate the GeoTIFF file
    #run_python_script(sys.argv[1])

    # Define filenames
    input_tif = 'polynomial_surface_with_bar_modi.tif'
    output_clip_tif = 'polynomial_surface_with_bar_modi_clip.tif'
    output_compressed_tif = 'polynomial_surface_with_bar_modi_compressed.tif'

    # Clip the generated GeoTIFF file
    clip_geotiff(input_tif, output_clip_tif)

    # Compress the clipped GeoTIFF file
    compress_geotiff(output_clip_tif, output_compressed_tif)

if __name__ == "__main__":
    main()
