from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import numpy as np
import concurrent.futures

class Scraper:
    """
    A class that scrapes ebay for phones based on provided brand, condition and number of items

    ...

    Attributes
    ----------
    brand : string
        name of the brand that you want scraped, example: 'Apple'

    number_of_items : int
        number of phones to be scraped
    
    condition_name : string
        condition of the phones to be scraped, 'used' or 'new'


    Methods
    -------
    get_condition():
        returns a code for used or new condition to be used in the url
    
    get_brand_id():
        returns a code for a given brand to be used in the url

    get_num_of_pages():
        returns number of pages to be used in the url

    get_phones_url():
        returns urls from the main page of ebay and stores the specific model url in a list

    get_single_phone():
        scrapes the single model phone from get_phones_url list, returns a list of features

    scrape_phones():
        main method of the class, creates a csv file in the main directory
    """
    def __init__(self, brand: str, number_of_items: int, condition_name: str):
        """
        Constructs a default state of attributes.
        
        Args:
            brand: (string)
                Name of the brand that will be scraped
            number_of_items: (int)
                Number of items that will be scraped
            condition_name: (str)
                Condition type that will be scraped
        """
        self.__brand = brand
        self.__number_of_items = number_of_items
        self.__condition_name = condition_name
    
    def get_condition(self) -> int:
        """Function is checking condition_name state in order to assign a correct value code for the url to be scraped

        Raises:
            KeyError: if condition is not 'used' or 'new'

        Returns:
            int: specific code for a given condition
        """
        condition_code = {"new": 1000, "used": 3000}

        try:
            return condition_code[self.__condition_name] 
        except KeyError:
            raise KeyError("condition_name must be a string 'new' or 'used'") 

    def get_brand_id(self) -> int:
        """Function is checking brand state in order to assign a correct value code for the url to be scraped

        Raises:
            KeyError: if brand is not 'Apple', 'LG', 'Huawei', 'Samsung'

        Returns:
            int: specific code for a given brand
        """
        brand_id_codes = {
            "Apple": 319682, 
            "LG": 353985, 
            "Huawei": 349965, 
            "Samsung": 352130}

        try:
            return brand_id_codes[self.__brand]
        except KeyError:
            raise KeyError("brand must be 'Apple', 'LG', 'Huawei' or 'Samsung'")

    def get_num_of_pages(self) -> int:
        """Calculates number of pages that will be scraped based on number of items user wants to get.
            By default, each page has 48 items.

        Returns:
            int: number of pages that will be scraped
        """
        try:
            return int(round(self.__number_of_items / 48))
        except ValueError:
            raise ValueError("number_of_items must be of int type")

    def get_phones_url(self) -> list:
        """Extracts url from each item on the main page of ebay, returns a list of urls.

        Returns:
            list: list of single phones
        """
        urls = []
        number_of_pages = self.get_num_of_pages()
        condition_code = self.get_condition()
        brand_id = self.get_brand_id()
        user_agent = UserAgent()

        for page_number in range(number_of_pages):
            url = f"https://www.ebay.com/b/{self.__brand}-Cell-Phones-Smartphones/9355/bn_{brand_id}?LH_ItemCondition={condition_code}&LH_PrefLoc=5&LH_Sold=1&rt=nc&_pgn={page_number}"
            page = requests.get(url, headers={"User-Agent": user_agent.google})
            soup = BeautifulSoup(page.content, "html.parser")

            urls.extend([links.get('href', np.nan) for links in soup.find_all('a', class_="s-item__link")])
        
        return urls

    def get_single_phone(self, url: str) -> list:
        """ It accepts a url, scrapes the url, assigns scraped data to a list, returns a list

        Args:
            url (str): url to be scraped

        Returns:
            list: list of scraped items
        """
        user_agent = UserAgent()
        page = requests.get(url, headers={"User-Agent": user_agent.google})
        soup = BeautifulSoup(page.content, "html.parser")

        temp_price = np.nan
        temp_model = np.nan
        temp_ram = np.nan
        temp_storage = np.nan
        temp_processor = np.nan
        temp_camera = np.nan

        if soup.find(class_="display-price"):
            temp_price = soup.find(class_="display-price").get_text()

        for item in soup.find_all('div', class_='s-name'):
            if item.get_text() == "Model": temp_model = item.next_sibling.get_text() 
            if item.get_text() == "RAM": temp_ram = item.next_sibling.get_text()
            if item.get_text() == "Storage Capacity": temp_storage = item.next_sibling.get_text() 
            if item.get_text() == "Processor": temp_processor = item.next_sibling.get_text() 
            if item.get_text() == "Camera Resolution": temp_camera = item.next_sibling.get_text() 
        
        return [temp_price, temp_model, temp_ram, temp_storage, temp_processor, temp_camera]

    def scrape_phones(self) -> None:
        """Main function of the package. Scrapes the data with other functions, creates a dataframe,
        exports the dataframe as csv file.

        Returns:
            csv_file: exports csv file in the main directory with scraped data
        """

        phone_model, phone_ram, phone_storage, phone_processor, phone_camera, phone_price = ([] for i in range(6))
        phones_url = self.get_phones_url()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.get_single_phone(), phones_url)
            
            for result in results:
                phone_price.append(result[0])
                phone_model.append(result[1])
                phone_ram.append(result[2])
                phone_storage.append(result[3])
                phone_processor.append(result[4])
                phone_camera.append(result[5]) 

        df = pd.DataFrame(
            data=zip(
                phone_price, 
                phone_model, 
                phone_ram, 
                phone_storage, 
                phone_processor, 
                phone_camera),
            columns=['price', 'model', 'ram', 'storage', 'processor', 'camera']
            )

        df['brand'] = self.__brand
        df['condition'] = self.__condition_name

        return df.to_csv(f"{self.__brand}_{self.__condition_name}_data.csv", index=False)