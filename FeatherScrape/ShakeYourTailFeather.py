import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

BASE_URL = "https://www.fws.gov/lab/featheratlas/idtool.php"



def main():
    driver = create_driver()
    driver.get(BASE_URL)

    nav_all_feathers_pg(driver)
    content = driver.page_source.encode("utf-8").strip()
    soup = bs(content, "lxml")
    try:
        links = soup.find("div", class_="caption").find_all("div", class_="singleResult")
    except:
        return

    try:
        tables = []
        for x in range(len(links) - 1):
            link = links[x]
            click_button(driver, xpath_soup(link.a))
            dfs = pd.read_html(driver.current_url)
            df = dfs[3].append(pd.Series(), ignore_index=True)
            tables.append(df)
            driver.back()
            driver.refresh()
        pd.concat(tables).to_excel("Python/FeatherScrape/Feather.xlsx")
    except Exception as e:
        print("ERROR: ", e)


def nav_all_feathers_pg(driver):
    button_paths = [
        "/html/body/div/div[5]/div[2]/form/section/div[2]/div[1]/button",
        "/html/body/div/div[5]/div[2]/form/div[5]/div/label[3]/input",
        "/html/body/div/div[5]/div[2]/form/p/input"
    ]

    for path in button_paths:
        click_button(driver, path)


def click_button(driver, path):
    try:
        button = driver.find_elements_by_xpath(path)[0]
        button.click()
    except Exception as e:
        print("ERROR: ", e)


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def create_driver():
    options_ = webdriver.ChromeOptions()
    # options_.add_argument("headless")
    options_.add_argument('window-size=2000,2000')
    options_.add_argument('window-position=3000,0')

    return webdriver.Chrome(ChromeDriverManager().install(), options=options_)


def wait_notify(wait_time):
    for x in range(wait_time):
        if wait_time-x < 10:
            print(wait_time - x)
        time.sleep(1)



if __name__ == "__main__":
    # t = time.time()
    main()
    # each_time = t - time.time()
    # print("Each: ", each_time, "Total: ", (each_time * 663)/60/60)
    # Each:  -13.68498682975769 Total:  -2.520318407813708