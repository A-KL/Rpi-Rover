from pyvirtualdisplay import Display
from easyprocess import EasyProcess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    path = '/usr/lib/chromium-browser/chromedriver'
    
    with Display(backend="xvnc", size=(800, 600), rfbport=5904) as display:
        print('xvnc ready')
        chrome = Service(path)
        driver = webdriver.Chrome(service=chrome)
        print('webdriver ready')
        driver.get('https://www.google.com')
        with EasyProcess(["xmessage", "hello"]) as proc:
            proc.wait()
            driver.quit()

    # driver.save_screenshot('SeleniumChromiumTest.png')
    # print ('target page loaded adnd screenshot taken')
    # print ('Done')

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--remote-debugging-port=9222')

    # driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=chrome_options)

    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--port')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
    # service = Service(chrome_options)
    # service.start()

    # driver = webdriver.Remote(service.service_url)
    # driver.get("https://www.python.org")
    # print(driver.title)
    # # time.sleep(5) # Let the user actually see something!
    # driver.quit()
    
    # browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    # browser.get('https://automatetheboringstuff.com')
    # display is active
    # disp.stop()
    # display is stopped