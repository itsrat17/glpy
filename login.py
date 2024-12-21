import requests
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME=os.getenv("UNAME")
PASSWORD=os.getenv("PWORD")

# Base URL for GL Bajaj login
login_url = "https://glbg.servergi.com:8072/ISIMGLB/Login"

def save_captcha_image(session, soup):
    image_tag = soup.find('img', {'id': 'Image1'})
    captcha_image_url = image_tag['src']
    # Get the full URL for the captcha image
    if not captcha_image_url.startswith('http'):
        captcha_image_url = f"https://glbg.servergi.com:8072/ISIMGLB/{captcha_image_url}"
    
    # Use captcha_headers instead of the general headers
    captcha_response = session.get(captcha_image_url)
    
    # Save the image to a file
    if captcha_response.status_code == 200:
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha_response.content)

def get_payload_variables(session):    
    response = session.get(login_url)
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
    viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    captcha_div = soup.find('div', {'id': 'pnlInfo1'})
    captcha_payload_key = captcha_div.find('input')['name']
    
    save_captcha_image(session=session, soup=soup)
    
    return viewstate, eventvalidation, viewstate_generator, captcha_payload_key

def login_and_get_home():
    # Create a session first
    session = requests.Session()
    
    # Pass session to get_initial_viewstate
    viewstate, eventvalidation, viewstate_generator, captcha_payload_key = get_payload_variables(session)
    
    
    captcha_input = input("enter captcha: ")
    # Prepare login payload
    payload = {
        '__LASTFOCUS': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstate_generator,
        '__EVENTVALIDATION': eventvalidation,
        'selector': 'rdoStdudent',
        '__txtUserId100': USERNAME,
        'txtPass': PASSWORD,
        captcha_payload_key: captcha_input,
        'btnLogin_': 'LOGIN',
        'zx1234': USERNAME,
        'hidsetname': 'ok',
        'hdnShowInstruction': '0',
        'txtUserName': '',
        'txtdateofBirth': ''
    }  
    # Perform login POST request with allow_redirects=True
    login_response = session.post(
        login_url,  
        data=payload, 
        allow_redirects=False  # Don't follow redirect automatically
    )
    
    # If login successful (302 status), get home page
    if login_response.status_code == 302:
        home_url = "https://glbg.servergi.com:8072/ISIMGLB/Home"
        home_response = session.get(home_url)
        return home_response.text
    else:
        return f"Login failed with status code: {login_response.status_code}"

# Usage
try:
    home_content = login_and_get_home()
    print(home_content)
except Exception as e:
    print(f"Error occurred: {str(e)}")
