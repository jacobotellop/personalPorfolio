#!/usr/bin/env python3
"""
PNG Resolution Scanner
Scans all PNG files in the current directory and displays their resolutions
"""

import os
from PIL import Image
import sys

def get_png_resolutions(folder_path="."):
    """
    Scan all PNG files in the specified folder and return their resolutions
    
    Args:
        folder_path (str): Path to scan (default: current directory)
    
    Returns:
        list: List of tuples containing (filename, width, height, file_size)
    """
    # Only PNG formats (both cases)
    supported_formats = {'.png', '.PNG'}
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found!")
        return []
    
    image_data = []
    
    # Get all files in the folder
    files = os.listdir(folder_path)
    png_files = [f for f in files if os.path.splitext(f)[1] in supported_formats]
    
    if not png_files:
        print(f"No PNG files found in '{folder_path}' directory.")
        print("Looking for files with .png or .PNG extensions.")
        return []
    
    print(f"Found {len(png_files)} PNG files. Scanning...\n")
    
    for filename in sorted(png_files):
        filepath = os.path.join(folder_path, filename)
        
        try:
            # Open image and get dimensions
            with Image.open(filepath) as img:
                width, height = img.size
                
            # Get file size
            file_size = os.path.getsize(filepath)
            file_size_mb = file_size / (1024 * 1024)  # Convert to MB
            
            image_data.append((filename, width, height, file_size_mb))
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    return image_data

def display_results(image_data):
    """Display the PNG resolution results in a formatted table"""
    if not image_data:
        return
    
    print("=" * 85)
    print("PNG FILES RESOLUTION REPORT")
    print("=" * 85)
    print(f"{'Filename':<40} {'Width':<8} {'Height':<8} {'Size (MB)':<10} {'Aspect Ratio'}")
    print("-" * 85)
    
    total_files = len(image_data)
    total_size = 0
    
    for filename, width, height, file_size in image_data:
        # Calculate aspect ratio
        aspect_ratio = round(width / height, 2) if height != 0 else 0
        
        print(f"{filename:<40} {width:<8} {height:<8} {file_size:<10.2f} {aspect_ratio}")
        total_size += file_size
    
    print("-" * 85)
    print(f"Total PNG files: {total_files}")
    print(f"Total size: {total_size:.2f} MB")
    
    # Find largest and smallest images
    if image_data:
        largest = max(image_data, key=lambda x: x[1] * x[2])
        smallest = min(image_data, key=lambda x: x[1] * x[2])
        
        print(f"\nLargest PNG: {largest[0]} ({largest[1]}x{largest[2]})")
        print(f"Smallest PNG: {smallest[0]} ({smallest[1]}x{smallest[2]})")
        
        # Show which files might need optimization
        large_files = [item for item in image_data if item[3] > 2.0]  # > 2MB
        if large_files:
            print(f"\nLarge files (>2MB): {len(large_files)} files")
            for item in large_files:
                print(f"  - {item[0]}: {item[3]:.2f} MB")

def create_csv_report(image_data, output_file="png_resolutions.csv"):
    """Create a CSV file with the PNG data"""
    if not image_data:
        return
    
    try:
        import csv
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Filename', 'Width', 'Height', 'Size_MB', 'Aspect_Ratio'])
            
            for filename, width, height, file_size in image_data:
                aspect_ratio = round(width / height, 2) if height != 0 else 0
                writer.writerow([filename, width, height, file_size, aspect_ratio])
        
        print(f"\nCSV report saved as: {output_file}")
        
    except Exception as e:
        print(f"Error creating CSV report: {e}")

def main():
    """Main function to run the PNG resolution scanner"""
    print("PNG Resolution Scanner")
    print("=" * 40)
    
    # Check if custom folder path is provided
    folder_path = "."
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    
    print(f"Scanning directory: {os.path.abspath(folder_path)}")
    print("Looking for: .png and .PNG files")
    
    # Get PNG data
    image_data = get_png_resolutions(folder_path)
    
    # Display results
    display_results(image_data)
    
    # Create CSV report
    if image_data:
        create_report = input("\nCreate CSV report? (y/n): ").lower().strip()
        if create_report in ['y', 'yes']:
            create_csv_report(image_data)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
