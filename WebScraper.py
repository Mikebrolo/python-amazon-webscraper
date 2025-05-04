import requests
from bs4 import BeautifulSoup
import time
from colorama import Fore, Style, init
import os

script_directory = os.path.dirname(__file__)
save_file_dir = os.path.join(script_directory, "Product.txt")

fullProduct = ""

class stripWeb:
    
    def invalidResponse(self):
        print(Fore.RED + Style.BRIGHT + "----------Not a valid url, try again----------" + Style.RESET_ALL)
        time.sleep(1)
        startStrip()

    def __init__(self):
        # Allow users to customize this later
        print("Type EXIT to quit the program...")
        print("Input your amazon url here : ")
        url = input(": ")
        
        if url.lower() == "exit": 
            print("Exiting the program....")
            exit()

        if url.__contains__("amazon"):
            pass
        else: self.invalidResponse()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url)
        except: self.invalidResponse()
            
        html = response.text # All the html elements

        # Parse with Bs4
        self.soup = BeautifulSoup(html, 'html.parser')

    # Gets product price
    def findPrice(self):
        classes = ["a-price-symbol", "a-price-whole", "a-price-fraction"]
        price = ""    

        for _class in classes:
            string = self.soup.find("span", class_=_class)
            price += str(string.text)
    
        return price

    #Finds descriptions
    def findDesc(self):
        _ul = self.soup.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
        desc = ""    

        if _ul:
            _liList = _ul.find_all("li")
            if _liList:
                for _li in _liList:
                    item = _li.find("span", class_="a-list-item")
                    desc += f"\n{str(item.text)}"
        return desc

    #Find product details
    def findProductDetails(self, _id):
        _table = self.soup.find("table", id=_id)
        _details = ""
    
        if _table:
            _trList = _table.find_all("tr")
            if _trList:
                for _tr in _trList:
                    _th = _tr.find("th")
                    _td = _tr.find("td")
                    _details += f"\n{_th.text.strip()} : {_td.text.strip()}"
    
        return _details
                

    def displayInfo(self):
        
        global fullProduct
        
        productTitle = self.soup.find("h1", id="title")
        if productTitle == None:
            print(Fore.RED + Style.BRIGHT + "\n----------Webpage does not allow stripping----------\n")
            time.sleep(0.5)
            print(Fore.RED + Style.BRIGHT + "----------Please import another URL-----------\n" + Style.RESET_ALL)
            time.sleep(1)
            return startStrip()

        print(Fore.BLUE + Style.BRIGHT + f"Product Title: {productTitle.text.strip()}\n")
        print(Fore.GREEN + f"Price: {self.findPrice()}\n")
        print(Fore.CYAN + f"Description: {self.findDesc()}\n")

        # Checks if section two is availabe, if not does the first section
        if self.findProductDetails("productDetails_techSpec_section_2"):
            print(Fore.MAGENTA + f"Product Details: {self.findProductDetails('productDetails_techSpec_section_2')}\n" + Style.RESET_ALL)
        else: print(Fore.MAGENTA + f"Product Details: {self.findProductDetails('productDetails_detailBullets_sections1')}\n" + Style.RESET_ALL)
        
        
        fullProduct = ["-" * 150,
                         f"\nProduct Title: {productTitle.text.strip()}\n",
                         f"\nPrice: {self.findPrice()}\n",
                         f"\nDescription: {self.findDesc()}\n",
                         f"\nProduct Details: {self.findProductDetails('productDetails_detailBullets_sections1')}\n",
        ]
        
        if self.findProductDetails("productDetails_techSpec_section_2"):
            fullProduct.append(f"Product Details: {self.findProductDetails('productDetails_techSpec_section_2')}\n")

        time.sleep(2)
        askForSave()
    
    

def startStrip():
    stripper = stripWeb()
    stripper.displayInfo()
    
def askForSave():
    print("----------Would you like to save the product to a file?----------")
    answer = input("y/n : ")
    
    if answer == "y": saveFile()
    elif answer == "n": startStrip()
    else: 
        print(Fore.RED + Style.BRIGHT + "Not a valid input, try again" + Style.RESET_ALL) 
        time.sleep(1)
        askForSave()

def saveFile():
    with open(save_file_dir, "a", encoding="utf-8") as file:
        for line in fullProduct:
            file.writelines(line)
    print(Fore.YELLOW + "Saving File....")
    time.sleep(2)
    print(Fore.GREEN + "Saved File!!")
    time.sleep(1)
    lookAgain()

def lookAgain():
    print("----------Do you want to check another URL?----------")
    choice = input("y/n : ")
    
    if choice == "y": startStrip()
    elif choice == "n": exit()
    else: 
        print(Fore.RED + Style.BRIGHT + "Not a valid input, try again" + Style.RESET_ALL) 
        time.sleep(1)
        lookAgain()
    

startStrip()