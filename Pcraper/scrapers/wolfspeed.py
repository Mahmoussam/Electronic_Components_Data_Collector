from .common_imports import *
logger = logging.getLogger(__name__)

class WolfSpeed(WebScraper):
    def __init__(self):
        self.__cookie_button_xpath = "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cookie settings' )]"
        self.__data_table_xpath = "//table[@class='css-3xrayo eq5psfl6']"
    def __handle_cookie_button(self , driver , wtime = 60) -> bool:
        ''' waits for  "Accept Cookies Button" for a definite time wtime in seconds
            Then tries to click it
            Returns True if button found and clicked successfully
            Else False
        '''
        wait = WebDriverWait(driver, wtime)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, self.__cookie_button_xpath)))
            logging.info("trying to click")
            time.sleep(1)
            btn = driver.find_element(By.XPATH , self.__cookie_button_xpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            btn.click()
            logging.info('clicked')
        except Exception as ex:
            logger.exception("cookie not clicked!!")
            return False
        return True
    def load_page(self,driver , url):
        '''
        load url and handle necessary setup
        '''
        driver.get(url)
    
    def __scrap_table(self,driver , table_element):
        '''
        scrapes table data ,given table web element and driver object
        '''
        pass

    def __locate_main_table(self,driver):
        '''
        locates main table of components data..
        '''
        table = driver.find_element(By.XPATH , self.__data_table_xpath)
        return table
    def __wait_until_linkable(self,driver, element, timeout=10):
        """
        Waits until the given WebElement is both visible and enabled.
        Returns the element once clickable, or raises TimeoutException.
        """
        return WebDriverWait(driver, timeout).until(
            lambda d: 'download' in element.get_attribute("href").lower()
        )
    def scrap_data(self,driver ,url , writer):
        '''
        scraps web page for data
        '''
        self.load_page(driver , url)
        logging.info('Handling cookie:')
        self.__handle_cookie_button(driver)
        driver.fullscreen_window()# try to evade button stale problem 
        self.__handle_cookie_button(driver , 2)
        logging.info('Done handling cookie')

        time.sleep(1)
        table = self.__locate_main_table(driver)
        

        #scrap headers first..
        header_elements = table.find_elements(By.XPATH , "(//tr)[1]//span")
        header = [span.text for span in header_elements]
        header = [header[0]] + header[5:]
        writer.write_row(header)

        rows = table.find_elements(By.XPATH ,'(//tbody)[1]//tr' )
        tot = len(rows)
        
        links = []

        for i in range(tot):
            row = table.find_elements(By.XPATH ,'(//tbody)[1]//tr' )[i]
            download_element = None
            try:
                download_element = row.find_elements(By.TAG_NAME , 'td')[3].find_element(By.TAG_NAME , 'a')
            except:
                #nott good  ,terrible practice ,, mashy 7alak for now..
                pass
            #print(download_element.get_attribute("outerHTML"))
            
            url = None
            if download_element is not None:
                try:
                    self.__wait_until_linkable(driver, download_element)
                except:
                    self.__handle_cookie_button(driver , 2)
                    self.__wait_until_linkable(driver, download_element)
                #print(len(download_element) , '#')
                url = download_element.get_attribute("href")
                print(url) #download_element.text
            if row.text == '':
                if self.__handle_cookie_button(driver , 2):
                    table = self.__locate_main_table(driver)
                    row = table.find_elements(By.XPATH ,'//tr' )[i]
            content = row.text.split('\n')
            #print(content)
            links.append([content[0] , url])
            writer.write_row(content)
        return links
        #writer.close() 
#selenium.common.exceptions.StaleElementReferenceException
    
if __name__ == '__main__':
    
    pass
