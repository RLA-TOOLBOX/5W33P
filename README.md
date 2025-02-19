# Web Vulnerability Scanner

## 📌 Overview
The **Web Vulnerability Scanner** is a security tool designed to **identify and exploit vulnerabilities** in web applications for educational and ethical penetration testing purposes.  

🔹 **What it does**:  
- Scans web applications for **Cross-Site Scripting (XSS), Open Redirects, and Defacement vulnerabilities**.  
- Uses **custom payloads** to test potential security flaws.  
- Automates the detection of exploitable **security weaknesses**.  

⚠️ **WARNING**: Unauthorized use of this tool is illegal. Always have **explicit permission** from the target website owner before running tests.

---

## ⚙️ Features
- **Automated Scanning**: Sends payloads to web applications and analyzes responses.
- **Multiple Attack Vectors**:
  - **Cross-Site Scripting (XSS)**: Tests for JavaScript injection vulnerabilities.
  - **Open Redirects**: Detects if a website can be manipulated to redirect users.
  - **Defacement Testing**: Evaluates security weaknesses that allow UI modification.
- **Custom Payload Support**: Allows users to supply their own payloads for testing.
- **Logging & Reporting**: Saves scan results for analysis.

---

## 🛠 Installation
```
git clone https://github.com/AnonCatalyst/5W33P
cd 5W33P
pip install -r requirements.txt --break-system-packages
```

## **USAGE**: python3 5w33p.py [-h] [-f FILE] [urls]

Test for XSS, Defacement, Open Redirect, Clickjacking, and HTTP Parameter Pollution vulnerabilities.

positional arguments:
  urls                  A single URL to test.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File containing a list of URLs to test.

