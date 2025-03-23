from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup, Tag
import re



class HTMLParser:
    """
        A class to parse and extract structured data from HTML content
    """
    
    def __init__(self, html_content:str):
        """
            Initialize parser with HTML 

            Args:
                html_content (str): Raw HTML content to parse
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
    
    def get_by_css_selector(self, selector:str) -> List[Tag]:
        """
        Extract elements using CSS selectors
        
        Args:
            selector (str): ('.class', '#id', 'tag' ...)
        
        Returns:
            List[Tag]: List of matching BeautifulSoup Tag objects
        """
        return self.soup.select(selector = selector)
    
    def get_by_xpath(self, xpath: str) -> List[Tag]:
        """
        Extract elements using XPath queries
        Note: BeautifulSoup doesn't natively support XPath, 
        this is a simplified implementation
        Args:
            xpath (str)
        Returns:
            List[Tag]: List of matching elements
        """
        if xpath.startswith('//'):
            xpath = xpath[2:]
            
        xpath = xpath.replace('/', ' ')
        xpath = xpath.replace('[@class=]', '.')
        xpath = xpath.replace(']','')
        
        return self.soup.select(xpath = xpath)
    
    
    
    
    