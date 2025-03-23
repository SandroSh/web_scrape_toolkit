from typing import List, Dict, Optional
import os
import requests
from bs4 import Tag
from urllib.parse import urljoin
from .logger_config import setup_logger
from .utils import save_to_json, save_to_csv, ProductSelectors
from html_parser import HTMLParser
from  http_handler import get_request


class ProductScraper:
    """Scraper for collecting product data from e-commerce websites"""
    
    def __init__(self, base_url:str, selectors = ProductSelectors, output_dir:str = 'downloads' ) -> None:
        self.base_url = base_url
        self.output_dir = output_dir
        self.logger = setup_logger('productScraper')
        self.selectors = selectors
        os.makedirs(output_dir, exist_ok=True)
        
    def fetch_page(self,url:str) -> Optional[str]:
        
        try:
            html = get_request(url)
            self.logger.info(f"Successfully fethed: {url}")
            return html
        except requests.RequestException as e:
            self.logger.error(f"An error occurred: {e}")
            return None

    def extract_product_data(self, parser:HTMLParser,) -> Dict:
        
        products = []
            
        products_container = parser.get_by_css_selector(self.selectors['product'])
        
        for container in products_container:
            
            try:
                name = ( 
                    parser.clean_text(container.select_one(self.selectors["name"]).get_text())
                    if container.select_one(self.selectors['name']) 
                    else 'N/A' 
                )
                price = ( 
                    parser.clean_text(container.select_one(self.selectors["price"]).get_text())
                    if container.select_one(self.selectors['price']) 
                    else 'N/A' 
                )
                image_url = ( 
                    parser.clean_text(container.select_one(self.selectors["image"]).get('src'))
                    if container.select_one(self.selectors['image']) 
                    else None 
                )
                rating = ( 
                    parser.clean_text(container.select_one(self.selectors['rating']).get_text())
                    if container.select_one(self.selectors['rating']) 
                    else 'N/A' 
                )
                product = {
                    'name': name,
                    'price': price,
                    'image_url': image_url,
                    'rating': rating
                }
                
                products.append(product)
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
        return products

    def download_image(self, image_url:str, product_name:str) -> Optional [str]:
        
        try:
            
            if not image_url:
                return None
            
            full_url = urljoin(self.base_url, image_url)
            
            response = get_request(full_url , stream=True)
            response.raise_for_status()
            
            safe_name = ''.join(c for c in product_name if c.isalnum() or c in ' _-')
            filename = f"{safe_name}.jpg"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.logger.info(f"Image downloaded: {filename}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to download iamge {image_url}: {e}")
            return None
    
    def get_next_page(self, parser:HTMLParser) -> Optional[str]:
        """ Pagination logic by finding next page Url"""
        
        next_link = parser.get_by_css_selector(self.selectors['next_page'])
        
        if next_link and next_link[0].get('href'):
            return urljoin(self.base_url, next_link[0].get('href'))
        return None
    
    
        
            
        