from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import numpy as np

def check_brandId(brand: str) -> int:
    """All brands have unique code that needs to be passed to the ebay url. 
        This function assigns a unique code based on the brand name.
    Args:
        brand (str): name of the brand, example: Apple

    Raises:
        ValueError: Informs the user what is accepted as parametars

    Returns:
        int: unique brand code, that will be used for a page url
    """
    brandId: int
    if brand == "Apple":
        brandId = 319682
    elif brand == "LG":
        brandId = 353985
    elif brand == "Huawei":
        brandId = 349965
    elif brand == "Samsung":
        brandId = 352130
    else:
        raise ValueError("Function only supports Apple, LG, Huawei or Samsung brand")

    return brandId

def calculate_number_of_pages(number_of_items: int) -> int:
    """Calculates number of pages that will be scraped based on number of items user wants to get.
        By default, each page has 48 items.

    Args:
        number_of_items (int): number of items user wants to scrape

    Returns:
        int: number of pages that will be scraped
    """
    return int(round(number_of_items / 48)) 
   

def get_phones_url(number_of_pages: int, brand: str, brandId: int, user_agent: UserAgent) -> list:
    """Extracts url from each item on the main page of ebay, returns a list of urls.

    Args:
        number_of_pages (int): previously calculated number of pages, used in the url
        brand (str): given brand, used in the url
        brandId (int): unique brand code, used in the url
        user_agent (UserAgent): tells ebay what browser we are using

    Returns:
        list: list of single phones
    """
    urls = []
    
    for page_number in range(number_of_pages):
        url = f"https://www.ebay.com/b/{brand}-Cell-Phones-Smartphones/9355/bn_{brandId}?LH_ItemCondition=1000|3000&LH_PrefLoc=5&LH_Sold=1&rt=nc&_pgn={page_number}"
        page = requests.get(url, headers={"User-Agent": user_agent.google})
        soup = BeautifulSoup(page.content, "html.parser")

        urls.extend([links.get('href', np.nan) for links in soup.find_all('a', class_="s-item__link")])

    return urls

def create_dataframe(
    brand: str, 
    phone_price: list, 
    phone_model: list, 
    phone_ram: list, 
    phone_storage: list, 
    phone_processor: list, 
    phone_camera: list) -> pd.DataFrame:
    """creates a dataframe from passed lists, returns the created dataframe

    Args:
        brand (str): name of the brand we scraped
        phone_price (list): price of each phone
        phone_model (list): model of each phone
        phone_ram (list): ram memory of each phone
        phone_storage (list): storage room of each phone
        phone_processor (list): processor of each phone
        phone_camera (list): camera resolution of each phone

    Returns:
        pd.DataFrame: pandas dataframe for further analysis
    """
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
    df['brand'] = brand
    return df

def export_csv_file(df: pd.DataFrame, brand: str) -> None:
    """accepts a dataframe, exports a csv file to the main directory

    Args:
        df (pd.DataFrame): generated dataframe
    """
    df.to_csv(f"{brand}_data.csv", index=False)

def scrape_phones(brand: str, number_of_items: int) -> None:
    """Main function of the package. Accepts a name of the brand, number of items wished to scrape.
    Checks for unique brand code, calculates number of pages,
    scrapes each page for phones: Model, Storage, Price, Camera, Processor, Ram.
    If something is missing from the page replaces it with NaN,
    Creates a dataframe, and exports a csv file

    Helper Functions Used:
        check_brandId(),
        calculate_number_of_pages(),
        get_phones_url(),
        create_dataframe(),
        export_csv_file()

    Args:
        brand (str): Type of phone brand to be scraped
        number_of_items (int): How many items needed to be scraped
    """
    brandId = check_brandId(brand)
    number_of_pages = calculate_number_of_pages(number_of_items)
    user_agent = UserAgent()

    phone_model, phone_ram, phone_storage, phone_processor, phone_camera, phone_price = ([] for i in range(6))
    
    single_phone_urls = get_phones_url(number_of_pages, brand, brandId, user_agent)

    for single_phone_url in single_phone_urls:
        url = single_phone_url
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

            if item.get_text() == "Model":
                temp_model = item.next_sibling.get_text()

            if item.get_text() == "RAM":
                temp_ram = item.next_sibling.get_text()

            if item.get_text() == "Storage Capacity":
                temp_storage = item.next_sibling.get_text()

            if item.get_text() == "Processor":
                temp_processor = item.next_sibling.get_text()

            if item.get_text() == "Camera Resolution":
                temp_camera = item.next_sibling.get_text()
        
        phone_price.append(temp_price)
        phone_model.append(temp_model)
        phone_ram.append(temp_ram)
        phone_storage.append(temp_storage)
        phone_processor.append(temp_processor)
        phone_camera.append(temp_camera)

    phone_df = create_dataframe(
        brand=brand,
        phone_price=phone_price,
        phone_model=phone_model,
        phone_ram=phone_ram,
        phone_storage=phone_storage,
        phone_processor=phone_processor,
        phone_camera=phone_camera)
    
    export_csv_file(phone_df, brand)