# GLB Student Portal Login Automation

This Python project allows you to programmatically log in to the **GL Bajaj Institute of Technology and Management (GLB) student portal**. It handles **viewstate, event validation, captcha image download**, and prepares the payload for login using `requests` and `BeautifulSoup`.

> ⚠️ Captcha still requires **manual input** for login. Fully automated captcha solving is not implemented.

---

## Features

- Retrieves necessary payload values (`__VIEWSTATE`, `__EVENTVALIDATION`, `__VIEWSTATEGENERATOR`) dynamically.
- Downloads and saves captcha image for manual input.
- Performs login using provided credentials stored in `.env`.
- Handles redirections and fetches the student homepage content after login.
- Securely manages sensitive data (username and password) using environment variables.

---

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `python-dotenv`

Install dependencies using pip:

```bash
pip install requests beautifulsoup4 python-dotenv
