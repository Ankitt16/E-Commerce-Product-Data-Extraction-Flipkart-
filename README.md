# 💻 E-Commerce Product Data Extraction (Flipkart)

A **Python-based web scraping automation project** that collects real-time **laptop data** (brand, price, discount, ratings, reviews, and images) from [Flipkart](https://www.flipkart.com).  
The script extracts product details, cleans the data, and exports it into **Excel** and **CSV** formats for further analysis or visualization.

---

## 🚀 Features

- 🔍 Scrapes laptop details such as **brand, name, price, discount, rating, reviews, and image URLs**.  
- 🌐 Uses **BeautifulSoup** and **Requests** for HTML parsing and dynamic content handling.  
- 📄 Supports **pagination** — scrapes up to 100+ pages automatically.  
- ⚙️ Includes **robust error handling** and **retry logic** to manage inconsistent HTML and network issues.  
- 📊 Exports cleaned data to **Excel (.xlsx)** and **CSV**, using **Pandas + OpenPyXL**, with **timestamped filenames**.  
- 🗂️ Adds a **file validation and preview system** showing saved file paths, sizes, and sample rows.  
- 🧩 Fully modular code — easy to extend for other Flipkart categories (mobiles, TVs, etc.).

---

## 🧠 Tech Stack

- **Language:** Python  
- **Libraries:** `requests`, `beautifulsoup4`, `pandas`, `openpyxl`, `time`, `os`, `random`, `datetime`

---

## 📦 Installation

```bash
# Clone this repository
git clone:- Ankitt16/E-Commerce-Product-Data-Extraction-Flipkart-.git

# Navigate to the project folder
cd E-Commerce Product Data Extraction (Flipkart)

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate     # for Windows
source venv/bin/activate  # for Mac/Linux

# Install required packages
pip install -r requirements.txt

Usage
# Run the scraper
python flipkart_Webscraping.py

#Output files are saved as:

flipkart_laptops_YYYYMMDD_HHMMSS.xlsx
flipkart_laptops_YYYYMMDD_HHMMSS.csv

#⚠️ Notes

The script is for educational and research purposes only.
Frequent or aggressive scraping may trigger Flipkart’s anti-bot protection.
Respect robots.txt and website terms of service.

#🧩 Future Enhancements

Add support for other product categories (mobiles, TVs, etc.).
Store data into a MySQL or SQLite database.
Schedule automatic runs using Cron or Windows Task Scheduler.
Integrate visual dashboards (Power BI, Plotly, or Streamlit).

#👨‍💻 Author

Ankit Kumar
📍 Noida, India
📧 ankitkumar2716@gmail.com
🔗 LinkedIn Profile:-- www.linkedin.com/in/ankit-kumar-80888a245/
