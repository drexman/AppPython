import openpyxl
import webbrowser
import pyautogui
from time import sleep
from urllib.parse import quote
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\samue\\AppData\\Local\\Google\\Chrome\\User Data")
driver=webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
driver.get('https://web.whatsapp.com/')
input("Scan the QR code and press Enter to continue...")
wait=WebDriverWait(driver, 100)    
workbook = openpyxl.load_workbook('clientes.xlsx')
pagina_clientes = workbook['Planilha1']

chat_input = driver.find_element("css selector", "div.copyable-text")
print(chat_input)

