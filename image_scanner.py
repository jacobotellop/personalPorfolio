#!/usr/bin/env python3
"""
Image Resolution Scanner
Scans all images in the 'images' folder and displays their resolutions
"""

import os
from PIL import Image
import sys

def get_image_resolutions(folder_path="images"):
    """
    Scan all images in the specified folder and return their resolutions
    
    Args:
        folder_path (str): Path to the images folder
    
    Returns:
        list: List of tuples containing (filename, width, height, file_size)
    """
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic'}
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found!")
        print("Please create an 'images' folder and place your images there.")
        return []
    
    image_data = []
    
    # Get all files in the folder
    files = os.listdir(folder_path)
    image_files = [f for f in files if os.path.splitext(f.lower())[1] in supported_formats]
    
    if not image_files:
        print(f"No supported image files found in '{folder_path}' folder.")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return []
    
    print(f"Scanning {len(image_files)} image files...\n")
    
    for filename in sorted(image_files):
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
    """Display the image resolution results in a formatted table"""
    if not image_data:
        return
    
    print("=" * 80)
    print("IMAGE RESOLUTION REPORT")
    print("=" * 80)
    print(f"{'Filename':<35} {'Width':<8} {'Height':<8} {'Size (MB)':<10} {'Aspect Ratio'}")
    print("-" * 80)
    
    total_files = len(image_data)
    total_size = 0
    
    for filename, width, height, file_size in image_data:
        # Calculate aspect ratio
        aspect_ratio = round(width / height, 2) if height != 0 else 0
        
        print(f"{filename:<35} {width:<8} {height:<8} {file_size:<10.2f} {aspect_ratio}")
        total_size += file_size
    
    print("-" * 80)
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size:.2f} MB")
    
    # Find largest and smallest images
    if image_data:
        largest = max(image_data, key=lambda x: x[1] * x[2])
        smallest = min(image_data, key=lambda x: x[1] * x[2])
        
        print(f"\nLargest image: {largest[0]} ({largest[1]}x{largest[2]})")
        print(f"Smallest image: {smallest[0]} ({smallest[1]}x{smallest[2]})")

def create_csv_report(image_data, output_file="image_resolutions.csv"):
    """Create a CSV file with the image data"""
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
    """Main function to run the image resolution scanner"""
    print("Image Resolution Scanner")
    print("=" * 50)
    
    # Check if custom folder path is provided
    folder_path = "images"
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    
    print(f"Scanning folder: {folder_path}")
    
    # Get image data
    image_data = get_image_resolutions(folder_path)
    
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
