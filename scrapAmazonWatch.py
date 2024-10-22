from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pprint
from selenium.common.exceptions import StaleElementReferenceException
from components.dbOps import *

def scrape_watch_data():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--no-sandbox')  # Necessary for some server environments
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    chrome_options.add_argument('--disable-gpu')  # Disable GPU rendering
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    
    chrome_service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('https://www.amazon.com/s?k=watch')

    watch_data = []
    
    # Find all product links on the search results page
    product_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.s-result-item .a-link-normal.s-no-outline'))
    )
    
    # Extract href attributes before navigating
    product_urls = [link.get_attribute('href') for link in product_links]
    print(len(product_urls))
    
    for c, url in enumerate(product_urls):
        # if c > 10:
        #     break
        try:
            # Navigate to the product page
            driver.get(url)
            
            # Wait for the product details to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )
            
            # Parse the product page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract product details
            title = soup.select_one('#productTitle').text.strip() if soup.select_one('#productTitle') else "None"
            price = soup.select_one('span.a-price-whole').text if soup.select_one('span.a-price-whole') else "00."
            price2 = soup.select_one('span.a-price-fraction').text if soup.select_one('span.a-price-fraction') else "00"
            rating = soup.select_one('span.a-icon-alt').text if soup.select_one('span.a-icon-alt') else "0.0"
            
            # Extract product description
            description = []
            # Try the first format
            about_section = soup.select_one('div#feature-bullets')
            if about_section:
                list_items = about_section.select('ul li:not(.aok-hidden) span.a-list-item')
                for item in list_items:
                    description.append(item.text.strip())
            
            # If the first format didn't work, try the second format
            if not description:
                about_section = soup.select_one('div.a-expander-content')
                if about_section:
                    list_items = about_section.select('ul li span.a-list-item')
                    for item in list_items:
                        description.append(item.text.strip())
            
            # Extract image URL
            img_tag = soup.select_one('#landingImage')
            image_url = None
            if img_tag:
                if img_tag.has_attr('data-a-dynamic-image'):
                    image_urls = json.loads(img_tag['data-a-dynamic-image'])
                    # Get the URL with the highest resolution
                    image_url = max(image_urls.keys(), key=lambda x: image_urls[x][0] * image_urls[x][1])
                elif img_tag.has_attr('src'):
                    image_url = img_tag['src']
                    
            
            price = price.replace(",", '')
            finalPrice = float(f"{price}{price2}")
            finalRating = rating.split(" ")[0]
            watchDataDict = {
                'title': title,
                'price': finalPrice,
                'rating': finalRating,
                'description': description,
                'product_url': url,
                'image_url': image_url
            }
            
            pprint.pprint(watchDataDict)
            query = """
                INSERT INTO watches (title, price, rating, description, product_url, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                watchDataDict['title'],
                watchDataDict['price'],
                watchDataDict['rating'],
                '\n'.join(watchDataDict['description']),  # Join description list into a single string
                watchDataDict['product_url'],
                watchDataDict['image_url']
            )
            
            curID = insert_data(query, values)
            
            reviewDictList = []
            
            catchReview = soup.select_one('.review-views')
            reviews = catchReview.select(".review")
            
            for c, i in enumerate(reviews):
                if c == 5:
                    break
                rName = i.select("span.a-profile-name")[0].text
                rReview = i.select_one("i.review-rating").select("span.a-icon-alt")[0].text
                rDate = i.select("span.review-date")[0].text
                rText = i.select_one(".reviewText").select("span")[0].text

                reviewDict = {
                    'watch_id': int(curID),
                    'reviewer_name': rName,
                    'review_date': rDate,
                    'rating': rReview,
                    'review_text': rText
                }
                print("*"*50)
                pprint.pprint(reviewDict)
                print("*"*50)
                
                query = """
                INSERT INTO review (watch_id, reviewer_name, review_date, rating, review_text)
                    VALUES (%s, %s, %s, %s, %s)
                """
                vals = (
                    reviewDict['watch_id'],
                    reviewDict['reviewer_name'],
                    reviewDict['review_date'],
                    reviewDict['rating'],
                    reviewDict['review_text']
                )
                insert_data(query, vals)
                
            # Optional: Add a small delay to avoid overloading the server
            time.sleep(2)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue
    
    # pprint.pprint(watch_data)
    driver.quit()
    # insert_data(watch_data)

if __name__ == "__main__":
    scrape_watch_data()
    # print("\n\n Data from DB")
    # get_data()