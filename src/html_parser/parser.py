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
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text content
        Args:
            text (str)
        Returns:
            str: Cleaned text
        """
        
        if not text:
            return ""
        
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)
        return cleaned
    
    
    def extract_text(self, selector:str) -> List[str]:
        """
        Extract cleaned text from elements matching a CSS selector
        
        Args:
            selector (str): CSS selector
        
        Returns:
            List[str]: List of cleaned text content
        """
        elements = self.get_by_css_selector(selector = selector)
        return [self.clean_text(element.get_text()) for element in elements]
    
    def get_attributes(self, selector:str, attribute:str) -> List[Optional[str]]:
        """
        Extract specific attributes from elements
        
        Args:
            selector (str): CSS selector
            attribute (str): Attribute name to extract
        
        Returns:
            List[Optional[str]]: List of attribute values
        """
        elements = self.get_by_css_selector(selector)
        return [element.get(attribute) for element in elements]

    def navigate_parent(self, element: Tag) -> Optional[Tag]:
        """
        Navigate to parent element
        
        Args:
            element (Tag): Starting element
        
        Returns:
            Optional[Tag]: Parent element or None
        """
        return element.parent
    
    def navigate_children(self, element: Tag) -> List[Tag]:
        """
        Navigate to children
        
        Args:
            element (Tag): Starting element
        
        Returns:
            List[Tag]: List of children elements
        """
        return list(element.children)
    
    def find_all(self, tag: str, attrs: Optional[Dict[str, str]] = None) -> List[Tag]:
        """
            Find all elements matching tag name and attributes
            
            Args:
                tag(str): HTML tag name
                attrs(Dict[str,str], Optional): Dictionary of attributes to match
            Returns:
                List[Tag]: Matching elements
            
        """
        
        return self.soup.find_all(tag, attrs = attrs)
    
    