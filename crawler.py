import re
import time
from io import StringIO

from bs4 import BeautifulSoup

from browser import Browser
from crawler_config import PION_WORLD, TAB_LIST
import pandas as pd
import os

"""
    Browser 객체를 초기화해서 실제 url 을 로드한뒤 데이터를 가공하는 파일.
    BeautifulSoup 써서 html 파싱.
"""

def format_text(element):
    text_content = element.text.strip()

    # if element.name in ["h1", "h2", "h3", "h4"]:
    #     return f"<{text_content}>\n"
    # elif element.name == "li":
    #     list_content = text_content or "•".join(element.find('span').text if element.find('span') else "")
    #     return f"• {list_content}\n"
    # elif element.name == "table":
    #     return format_table(element)
    # else:
    #     return re.sub(r'\s+', ' ', text_content) if element.name not in ["table", "li"] else text_content

    if element.name == "table":
        return format_table(element)
    else:
        return re.sub(r'\s+', ' ', text_content) if element.name not in ["table", "li"] else text_content


def format_table(table_element):
    return f"\n[table]\n{str(pd.read_html(StringIO(str(table_element))))}\n"


def scrap_pion_world(show_screen: bool = False):
    print("scraping start!")
    result_strings = []

    with Browser(show_screen) as browser:
        for i, tab in enumerate(TAB_LIST):
            browser.load(PION_WORLD + tab)
            time.sleep(2)  # 동적 컨텐츠 로드 기다리기

            # TODO! 너무 길어질 경우 파일을 나눠넣는다.

            # 크롤링 경과 로딩바
            print("\r", f"scraping... {'■' * (i + 1)}{'□' * (len(TAB_LIST) - (i + 1))}", end="")

            is_work_tab = i in [20, 21, 22]

            soup = BeautifulSoup(browser.page_source(), "html.parser")
            div = soup.find_all("div", attrs={'class': 'container'})[2]
            tag_list = ["h1", "h2", "h3", "h4", "h5", "p", "span"] + (
                ["li", "dt", "dd", "a", "table"] if not is_work_tab else [])

            matching_tags = div.find_all(tag_list)
            matching_tags += div.find_all("div", class_="about-author2")

            formatted_text = [format_text(x) for x in matching_tags]
            result_string = " ".join(formatted_text)
            result_strings.append(result_string + "\n" + "-" * 60 + "\n\n")

            file_save(tab + ".txt", result_string)

        print("\r", "scraping complete!")

    return "".join(result_strings)


def file_save(file_name, file_text):
    directory = os.getcwd() + '/crawler_data'

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)

    with open(file_path, 'w') as file:
        file.write(file_text)


def get_text_list_from_files(dir_path: str):
    result_list = []

    if not os.path.exists(dir_path):
        print("directory does not exist!")
        return result_list

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            result_list.append(content)

    return [str(i) for i in result_list]


"""
    크롤러 테스트용.
    배치 프로세스로 돌릴 예정
"""
if __name__ == "__main__":
    scrap_pion_world()
