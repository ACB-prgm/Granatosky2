import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

BASE_URL = "https://www.featherbase.info"
name_str = "[\"names\"].latin"
DF_dict = {
    "Species" : [],
    "Feather Number" : [],
    "Feather Type" : [],
    "Feather Length (cm)" : []
}


def main():
    birds_info = []
    driver = create_driver()
    driver.get(BASE_URL + "/uk/species/")

    content = driver.page_source.encode("utf-8").strip()
    soup = bs(content, "lxml")

    links = soup.find("div", class_="ui container segment").ul
    links = links.find_all("a")
    link_num = 0
    links_num = len(links)
    
    for link in links:
        link_num += 1
        print(link_num, "/", links_num)
        try:
            link = BASE_URL + link.get("href")
            driver.get(link)
            # driver.get("https://www.featherbase.info/uk/species/melanerpes/formicivorus")

            time.sleep(1)
            content = driver.page_source.encode("utf-8").strip()
            soup = bs(content, "lxml")
            diagram = soup.find("div", id="diagramWrapper")
            
            if  diagram != None:

                while not diagram.script:
                    content = driver.page_source.encode("utf-8").strip()
                    soup = bs(content, "lxml")
                    diagram = soup.find("div", id="diagramWrapper")
                
                species = None
                feather_type = None
                feather_length = None
                feather_num = None
                
                script_lines = str(diagram.script).splitlines()
                for line in script_lines:
                    if name_str in line: # get the name of the bird 
                        for item in line.split(";"):
                            if "[\"names\"].latin" in item:
                                species = item.split("\"")[3]  # prints the name of the bird
                    
                    elif "featherId:" in line:
                        feather_num = int(line.split(":")[1].strip().replace(",", ""))
                    
                    elif "typeOfFeathers:" in line: # get feather type
                        feather_type = float(line.split(":")[1].strip().replace(",", ""))
                        if feather_type == 1:
                            feather_type = "Primary Wing"
                        elif feather_type == 2:
                            feather_type = "Secondary Wing"
                        elif feather_type == 3:
                            feather_type = "Tail"

                    elif "max:" in line:
                        feather_length = float(line.split(":")[1].strip().replace(",", "")) / 10.0

                    if feather_length:
                        DF_dict["Species"].append(species)
                        DF_dict["Feather Number"].append(feather_num)
                        DF_dict["Feather Type"].append(feather_type)
                        DF_dict["Feather Length (cm)"].append(feather_length)
                        feather_type = None
                        feather_length = None

            # else:
            #     print(link, "Does not have feather data")
        except Exception as e:
            print(e)
        
        # break ###### DONT FORGET TO REMOVE #######
    
    DF = pd.DataFrame.from_dict(DF_dict)
    DF.to_excel("FeatherScrape/FeatherBase.xlsx")
    print(DF)



def create_driver():
    options_ = webdriver.ChromeOptions()
    options_.add_argument("headless")
    # options_.add_argument('window-size=2000,2000')
    # options_.add_argument('window-position=3000,0')

    return webdriver.Chrome(ChromeDriverManager().install(), options=options_)


if __name__ == "__main__":
    main()