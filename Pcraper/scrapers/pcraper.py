from abc import ABC , abstractmethod

class WebScraper(ABC):
    '''
    Abstract scraper class for scrapping electronic components
    data off websites..
    '''
    @abstractmethod
    def load_page(self,driver , url):
        '''
        load url and handle necessary setup
        '''
        pass
    @abstractmethod
    def scrap_data(self,driver , writer):
        '''
        scraps web page for data
        '''
        pass
"""
    @abstractmethod
    def __scrap_table(self,driver , table_element):
        '''
        scrapes table data ,given table web element and driver object
        '''
        pass
    @abstractmethod
    def __locate_main_table(self,driver):
        '''
        locates main table of components data..
        '''
        pass
    
"""
