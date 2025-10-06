import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import os
from datetime import datetime
import openpyxl

def get_script_directory():
    """Get the directory where the script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def scrape_flipkart_laptops():
    # Initialize lists to store data
    Product_name = []
    Brand_name = []
    Price_rp = []
    price_sp = []
    Discount = []
    Rating = []
    Reviews = []
    Image_Url = []
    
    page = 1
    max_pages = 100  
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.flipkart.com/'
    }
    
    while page <= max_pages:
        print(f"Scraping page {page}...")
        
        # URL with proper pagination
        url = f"https://www.flipkart.com/search?q=laptops&page={page}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors for product names
            names = (soup.find_all("div", class_="KzDlHZ") or 
                    soup.find_all("a", class_="wjcEIp") or
                    soup.find_all("div", class_="_4rR01T") or
                    soup.find_all("a", class_="CGtC98") or
                    soup.find_all("div", class_="KzDlHZ"))
            
            if not names:
                print("No products found on this page. Ending scraping.")
                break
            
            print(f"Found {len(names)} products on page {page}")
            
            # Extract all data for current page
            for i in range(len(names)):
                try:
                    # Product Name
                    name = names[i].get_text().strip()
                    Product_name.append(name)
                    
                    # Brand Name (first word of product name)
                    brand = name.split()[0] if name else 'N/A'
                    Brand_name.append(brand)
                    
                    # Prices
                    price_selectors = ["yRaY8j", "_30jeq3", "_1_WHN1"]
                    regular_price = 'N/A'
                    for selector in price_selectors:
                        prices = soup.find_all("div", class_=selector)
                        if prices and i < len(prices):
                            regular_price = prices[i].get_text().strip()
                            break
                    Price_rp.append(regular_price)
                    
                    # Special Price
                    sp_selectors = ["Nx9bqj", "_3I9_wc"]
                    special_price = 'N/A'
                    for selector in sp_selectors:
                        sp_prices = soup.find_all("div", class_=selector)
                        if sp_prices and i < len(sp_prices):
                            special_price = sp_prices[i].get_text().strip()
                            break
                    price_sp.append(special_price)
                    
                    # Discount
                    discount_selectors = ["UkUFwK", "_3Ay6Sb"]
                    discount = 'N/A'
                    for selector in discount_selectors:
                        discounts = soup.find_all("div", class_=selector)
                        if discounts and i < len(discounts):
                            discount = discounts[i].get_text().strip()
                            break
                    Discount.append(discount)
                    
                    # Rating
                    rating_selectors = ["XQDdHH", "_3LWZlK"]
                    rating = 'N/A'
                    for selector in rating_selectors:
                        ratings = soup.find_all("div", class_=selector)
                        if ratings and i < len(ratings):
                            rating = ratings[i].get_text().strip()
                            break
                    Rating.append(rating)
                    
                    # Reviews
                    review_selectors = ["Wphh3N", "_2_R_DZ"]
                    review = 'N/A'
                    for selector in review_selectors:
                        reviews = soup.find_all("span", class_=selector)
                        if reviews and i < len(reviews):
                            review_text = reviews[i].get_text().strip()
                            review = review_text.strip('()') if review_text else 'N/A'
                            break
                    Reviews.append(review)
                    
                    # Image URL
                    img_selectors = ["DByuf4", "_396cs4"]
                    img_url = 'N/A'
                    for selector in img_selectors:
                        imgs = soup.find_all("img", class_=selector)
                        if imgs and i < len(imgs) and imgs[i].has_attr('src'):
                            img_url = imgs[i]['src']
                            if img_url.startswith('//'):
                                img_url = 'https:' + img_url
                            break
                    Image_Url.append(img_url)
                    
                    print(f"Product {i+1}: {name}")
                    
                except Exception as e:
                    print(f"Error processing product {i+1} on page {page}: {e}")
                    # Append placeholder values
                    Product_name.append('Error')
                    Brand_name.append('Error')
                    Price_rp.append('Error')
                    price_sp.append('Error')
                    Discount.append('Error')
                    Rating.append('Error')
                    Reviews.append('Error')
                    Image_Url.append('Error')
            
            # Check for next page
            next_button = (soup.find("a", class_="_9QVEpD") or 
                          soup.find("span", string="Next"))
            
            if not next_button:
                print("No more pages found. Ending scraping.")
                break
            
            page += 1
            time.sleep(random.uniform(2, 3))
            
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break
    
    return Product_name, Brand_name, Price_rp, price_sp, Discount, Rating, Reviews, Image_Url

def save_data_to_file(data):
    """Save scraped data to Excel file in the script directory"""
    
    # Get the script directory
    script_dir = get_script_directory()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"flipkart_laptops_{timestamp}.xlsx"
    csv_filename = f"flipkart_laptops_{timestamp}.csv"
    
    excel_filepath = os.path.join(script_dir, excel_filename)
    csv_filepath = os.path.join(script_dir, csv_filename)
    
    df = pd.DataFrame({
        'Product Name': data[0],
        'Brand Name': data[1],
        'Regular Price': data[2],
        'Special Price': data[3],
        'Discount': data[4],
        'Rating': data[5],
        'Reviews': data[6],
        'Image URL': data[7]
    })
    
    # Remove rows with error markers
    df = df[df['Product Name'] != 'Error']
    
    if len(df) == 0:
        print("No valid data to save.")
        return None
    
    # Try to save as Excel first
    try:
        df.to_excel(excel_filepath, index=False, engine='openpyxl')
        print(f"✅ Excel file saved: {excel_filepath}")
        print(f"📊 Total products scraped: {len(df)}")
        return excel_filepath
    except Exception as e:
        print(f"❌ Excel save failed: {e}")
        print("🔄 Trying to save as CSV...")
    
    # Fallback to CSV
    try:
        df.to_csv(csv_filepath, index=False)
        print(f"✅ CSV file saved: {csv_filepath}")
        print(f"📊 Total products scraped: {len(df)}")
        return csv_filepath
    except Exception as e:
        print(f"❌ CSV save also failed: {e}")
        return None

def show_file_location(filepath):
    """Show where the file was saved"""
    if filepath and os.path.exists(filepath):
        print(f"\n🎉 File successfully created at:")
        print(f"📍 Location: {filepath}")
        print(f"📁 Folder: {os.path.dirname(filepath)}")
        print(f"💾 File size: {os.path.getsize(filepath)} bytes")
        
        # Show file contents preview
        df = pd.read_excel(filepath) if filepath.endswith('.xlsx') else pd.read_csv(filepath)
        print(f"\n📋 First 3 rows preview:")
        print(df.head(3))
    else:
        print("❌ File was not created successfully")

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Flipkart laptop scraping...")
    print(f"📁 Script location: {get_script_directory()}")
    
    # Check and install required packages
    try:
        import openpyxl
    except ModuleNotFoundError:
        print("📦 Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        import openpyxl
    
    # Scrape all data
    scraped_data = scrape_flipkart_laptops()
    
    # Save data to file
    if scraped_data and len(scraped_data[0]) > 0:
        saved_file_path = save_data_to_file(scraped_data)
        show_file_location(saved_file_path)
    else:
        print("❌ No data was scraped. Possible reasons:")
        print("   - Website structure changed")
        print("   - IP blocked by Flipkart")
        print("   - Network issues")
        print("   - Anti-bot protection")
        
        # Create a sample file to verify the location
        sample_data = {
            'Product Name': ['Sample Laptop 1', 'Sample Laptop 2'],
            'Brand Name': ['Sample', 'Sample'],
            'Regular Price': ['₹50,000', '₹60,000'],
            'Special Price': ['₹45,000', '₹55,000'],
            'Discount': ['10% off', '8% off'],
            'Rating': ['4.2', '4.5'],
            'Reviews': ['120', '150'],
            'Image URL': ['N/A', 'N/A']
        }
        sample_df = pd.DataFrame(sample_data)
        sample_path = os.path.join(get_script_directory(), "sample_file_location_check.xlsx")
        sample_df.to_excel(sample_path, index=False)
        print(f"\n📝 Sample file created at: {sample_path}")
        print("   This confirms the file location for when real data is scraped.")