##import socket
from pathlib import Path
import subprocess
import os
import platform
from PIL import Image
from io import StringIO
from PIL import Image
from io import BytesIO
from io import BytesIO
from pathlib import Path
import sys
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
try:
    import pyautogui
except:
    pass
import time
import sys
from python_supporter import logging
import getpass
import traceback

def get_chrome_web_browser_path():
    if platform.system() == 'Darwin': #맥
        return "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
    elif platform.system() == 'Windows': #윈도우
        #windows 7
        path1 = "C:\Program Files\Google\Chrome\Application\\chrome.exe"
        path2 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        #windows 10
        home = str(Path.home())
        #print(home) #C:\Users\hello
        path3 = home + "\\AppData\\Local\\Google\\Chrome\Application\\chrome.exe"
        if os.path.exists(path1):
            return path1
        elif os.path.exists(path2):
            return path2
        elif os.path.exists(path3):
            return path3
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        return ""

def kill_all_chrome_web_browser_processes():
    if platform.system() == 'Darwin': #맥
        pass
    elif platform.system() == 'Windows': #윈도우
        #https://stackoverflow.com/questions/57792469/kill-certain-chrome-process-in-python-not-all
        subprocess.call("TASKKILL /f /IM CHROME.EXE")
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        pass

def kill_all_chrome_web_browser_driver_processes():
    if platform.system() == 'Darwin': #맥
        pass
    elif platform.system() == 'Windows': #윈도우
        subprocess.call("TASKKILL /f /IM CHROMEDRIVER.EXE")
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        pass

def open_chrome_web_browser(url=None, user_data_dir=None, proxy_server=None):
    chrome_web_browser_path = get_chrome_web_browser_path()
    #https://not-to-be-reset.tistory.com/454
    user_data_dir_option = ""
    if user_data_dir:
        user_data_dir_option = f"--user-data-dir={user_data_dir}"
    #https://www.chromium.org/developers/design-documents/network-stack/socks-proxy/
    proxy_server_option = ""
    if proxy_server:
        proxy_server_option = f"--proxy-server={proxy_server}"
    if not url:
        url = ""
    if platform.system() == 'Darwin': #맥
        subprocess.Popen(f"{chrome_web_browser_path} {url} {user_data_dir_option} {proxy_server_option}  --disk-cache-dir=null --disk-cache-size=0", shell=True)
    elif platform.system() == 'Windows': #윈도우   
        subprocess.Popen(f"\"{chrome_web_browser_path}\" {url} {user_data_dir_option} {proxy_server_option}  --disk-cache-dir=null --disk-cache-size=0", shell=True) 
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        pass

def open_chrome_web_browser_with_remote_debugging_mode(remote_debugging_port, remote_debugging_address, user_data_dir=None, proxy_server=None, headless=False):
    chrome_web_browser_path = get_chrome_web_browser_path()
    #https://not-to-be-reset.tistory.com/454
    user_data_dir_option = ""
    if user_data_dir:
        user_data_dir_option = f"--user-data-dir={user_data_dir}"
    #https://www.chromium.org/developers/design-documents/network-stack/socks-proxy/
    proxy_server_option = ""
    if proxy_server:
        proxy_server_option = f"--proxy-server={proxy_server}"
    headless_option = ""
    if headless:
        headless_option = f"--headless={headless}"
    if platform.system() == 'Darwin': #맥
        #print(f"{chrome_web_browser_path} --remote-debugging-port={remote_debugging_port} --remote-debugging-address={remote_debugging_address} {user_data_dir_option} {proxy_server_option} {headless_option} --disk-cache-dir=null --disk-cache-size=0 &")
        subprocess.Popen(f"{chrome_web_browser_path} --remote-debugging-port={remote_debugging_port} --remote-debugging-address={remote_debugging_address} {user_data_dir_option} {proxy_server_option} {headless_option} --disk-cache-dir=null --disk-cache-size=0 &", shell=True)
    elif platform.system() == 'Windows': #윈도우   
        #print(f"\"{chrome_web_browser_path}\" --remote-debugging-port={remote_debugging_port} --remote-debugging-address={remote_debugging_address} {user_data_dir_option} {proxy_server_option} {headless_option} --disk-cache-dir=null --disk-cache-size=0")
        subprocess.Popen(f"\"{chrome_web_browser_path}\" --remote-debugging-port={remote_debugging_port} --remote-debugging-address={remote_debugging_address} {user_data_dir_option} {proxy_server_option} {headless_option} --disk-cache-dir=null --disk-cache-size=0", shell=True) 
    elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        pass
    
def save_partial_screenshot(element, image_file):
    #'''
    png = element.screenshot_as_png
    with open(image_file, "wb") as f:
        f.write(png)
    #'''
    '''
    #https://www.tutorialspoint.com/how-to-take-partial-screenshot-with-selenium-webdriver-in-python
    captcha_image_element.screenshot(image_file)
    '''

def save_full_screenshot(driver, image_file):     
    driver.save_screenshot(image_file)

def save_full_screenshot_with_scroll(driver, image_file): 
    # initiate value

    #image_file = image_file.with_suffix(".png") if not image_file.match("*.png") else image_file
    img_li = []  # to store image fragment
    offset = 0  # where to start

    # js to get height
    height = driver.execute_script("return Math.max(" "document.documentElement.clientHeight, window.innerHeight);")

    # js to get the maximum scroll height
    # Ref--> https://stackoverflow.com/questions/17688595/finding-the-maximum-scroll-position-of-a-page
    max_window_height = driver.execute_script(
        "return Math.max("
        "document.body.scrollHeight, "
        "document.body.offsetHeight, "
        "document.documentElement.clientHeight, "
        "document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )

    # looping from top to bottom, append to img list
    # Ref--> https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
    while offset < max_window_height:
        # Scroll to height
        driver.execute_script(f"window.scrollTo(0, {offset});")

        # === uncomment the line and edit id to hide persistent elements when scrolling ===
        # driver.execute_script("document.getElementById('navbar').innerHTML = '';")

        img = Image.open(BytesIO((driver.get_screenshot_as_png())))
        img_li.append(img)
        offset += height

    # In case it is not a perfect fit, the last image contains extra at the top.
    # Crop the screenshot at the top of last image.
    extra_height = offset - max_window_height
    if extra_height > 0 and len(img_li) > 1:
        pixel_ratio = driver.execute_script("return window.devicePixelRatio;")
        extra_height *= pixel_ratio
        last_image = img_li[-1]
        width, height = last_image.size
        box = (0, extra_height, width, height)
        img_li[-1] = last_image.crop(box)

    # Stitch image into one
    # Set up the full screen frame
    img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
    img_frame = Image.new("RGB", (img_li[0].size[0], img_frame_height))
    offset = 0
    for img_frag in img_li:
        img_frame.paste(img_frag, (0, offset))
        offset += img_frag.size[1]
    img_frame.save(image_file)

def save_partial_screenshot_with_scroll(driver, partial_element, image_file):
    save_full_screenshot_with_scroll(driver, image_file)

    #https://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python
    location = partial_element.location
    size = partial_element.size
    from PIL import Image
    from io import StringIO
    image = Image.open(image_file)
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    image = image.crop((int(left), int(top), int(right), int(bottom)))
    image.save(image_file)
    
def set_value(driver, element, value):
    driver.execute_script(f"""
    arguments[0].value='{value}';
    """, element)

def set_value_send_keys(driver, element, value):
    element.send_keys(value)

def set_attribute(driver, element, attribute, value):
    driver.execute_script(f"""
    arguments[0].setAttribute('{attribute}', '{value}')
    """, element)

def remove_element(driver, element):
    #https://stackoverflow.com/questions/22515012/python-selenium-how-can-i-delete-an-element
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, element)

def remove_x_scrollbar(driver):
    #https://stackoverflow.com/questions/22515012/python-selenium-how-can-i-delete-an-element
    driver.execute_script("""
    document.getElementsByTagName("body")[0].style.overflowX = "hidden";
    """)

'''
def click(driver, element):
    #element.click()
    #from selenium.webdriver.common.keys import Keys
    #button_element.send_keys(Keys.ENTER)
    driver.execute_script("arguments[0].click();", element)
'''

def click(element):
    element.click()
    
#def send_keys_click(driver, element):    
#    element.send_keys(Keys.ENTER)
def click_send_keys(driver, element):    
    element.send_keys(Keys.ENTER)

#def javascript_click(driver, element):
#    driver.execute_script("arguments[0].click();", element)
def click_javascript(driver, element):
    driver.execute_script("arguments[0].click();", element)

def scroll_down_to_bottom(driver):
    #https://www.codeit.kr/community/questions/UXVlc3Rpb246NjIyNDU3ZDAzNDJiOGU3ZGNkMDJhZTM0
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1.5) 

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
                
if __name__ == "__main__":
    level = logging.DEBUG
    #level = logging.INFO
    #level = logging.ERROR
    logging.basic_config(level)

    #chrome_debugger_address = "127.0.0.1:9222"
    #proxy_server = "45.159.155.25:61302"
    #chrome_driver = ChromeDriver(chrome_debugger_address, "C:\\Users\\hello\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
    #chrome_driver = ChromeDriver(chrome_debugger_address, "C:\\Users\\hello\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    ##chrome_driver = ChromeDriver(chrome_debugger_address, "C:\\Users\\hello\\AppData\\Local\\Google\\Chrome\\User Data")
    #
    #chrome_driver = ChromeDriver(chrome_debugger_address)
    chrome_driver = ChromeDriver()

    '''
    url = "http://www.naver.com"
    proxy_username = "run"
    proxy_password = "FS1484rs"
    chrome_driver.get_with_proxy_username_and_password(url, proxy_username, proxy_password)
    '''
    #'''
    chrome_driver.get("https://www.naver.com")
    save_full_screenshot_with_scroll(chrome_driver.get_driver(), 'test.png')
    #'''
