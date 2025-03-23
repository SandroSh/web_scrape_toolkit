from typing import Dict, Optional
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context
from error_handler import handle_http_error

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

class SSLAdapter(HTTPAdapter):
    """
        Adapter for secure SSL configuration
    """
    
    def __init__(self, ssl_version = ssl.PROTOCOL_TLSv1_2):
        self.ssl_version = ssl_version
        super().__init__()
        
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ssl_version=self.ssl_version)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        kwargs['ssl_context'] = context
        return PoolManager(*args, **kwargs)
    
        
def get_request(url:str, auth_token: Optional[str] = None, custom_headers: Optional[Dict] = None, timeout: int = 10) -> str:
    """
    Fetch web content from a given URL using a GET request with headers.
    Args:
        url (str)
        auth_token (str, optional)
        custom_headers (dict, optional)
        timeout (int): maximum amount of waiting time 
    Returns:
        str: The raw content 
    Raises:
        requests.RequestException
    """
    
    try:
        
        session = requests.Session()
        session.mount('https://', SSLAdapter())
        
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        # Add authentication if it is provided
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        # Add custom headers if they are provided
        if custom_headers:
            headers.update(custom_headers)
        
        response =  session.get(url, headers=headers,timeout=timeout, verify=True)
        response.raise_for_status()
        return response.text
    
    except requests.RequestException as e:
       error_message = handle_http_error(e)
       raise requests.RequestException(error_message)
    finally:
        session.close()


def post_request(url:str, data:Dict, auth_token:Optional[str] = None, custom_headers:Optional[Dict] = None, timeout: int = 10) -> str:
   
    """
    Send a POST request to a given URL with the provided data and headers.
    
    Args:
        url (str): The URL to send the POST request to
        data (dict): The data to send in the POST request
        auth_token (str, optional): Authentication token for Bearer auth
        custom_headers (dict, optional): Custom headers to add to the request
        timeout (int): maximum amount of waiting time 
    Returns:
        str: The raw content
        
    Raises:
        requests.RequestException
    """
    
    try:
        
        session = requests.Session()
        session.mount('https://', SSLAdapter())
        
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*"
        }

        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        if custom_headers:
            headers.update(custom_headers)
        
        response = requests.post(url, data=data, headers=headers, timeout=timeout, verify=True)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
       error_message = handle_http_error(e)
       raise requests.RequestException(error_message)
    finally:
        session.close()
    
    
def put_request(url: str, data: Dict, auth_token: Optional[str] = None, custom_headers: Optional[Dict] = None, timeout: int = 10) -> str:
    """
    Args:
        url (str): The URL to send the PUT request to
        data (dict): Data to update the resource with
        auth_token (str, optional): Authentication token for Bearer auth
        custom_headers (dict, optional): Custom headers to add to the request
        timeout (int): maximum amount of waiting time 
    Returns:
        str: The response content from the server
    Raises:
        requests.RequestException
    """
    try:
        session = requests.Session()
        session.mount('https', SSLAdapter())
        
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*"
        }

        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        if custom_headers:
            headers.update(custom_headers)
            
        response = session.put(url, data = data, headers=headers, timeout= timeout,verify=True)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
       error_message = handle_http_error(e)
       raise requests.RequestException(error_message)
    finally:
        session.close()
    

def delete_request(url: str, auth_token: Optional[str] = None, custom_headers: Optional[Dict] = None, timeout: int = 10) -> str:
    """
    Args:
        url (str): The URL to send the DELETE request to
        auth_token (str, optional): Authentication token for Bearer auth
        custom_headers (dict, optional): Custom headers to add to the request
        timeout (int): maximum amount of waiting time 
    Returns:
        str: The response content from the server
    Raises:
        requests.RequestException
    """
    try:
        session = requests.Session()
        session.mount('https://', SSLAdapter())
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "*/*"
        }

        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        if custom_headers:
            headers.update(custom_headers)
        response = session.delete(url, headers=headers, timeout= timeout, verify= True)
        response.raise_for_status()
        return response.text()
    except requests.RequestException as e:
       error_message = handle_http_error(e)
       raise requests.RequestException(error_message)
    finally:
        session.close()