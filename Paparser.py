import requests
from bs4 import BeautifulSoup as bs
import re

def music(name: str):
    name = name.replace(' ', '+')
    if name == "":
       return None
    url = f'https://www.youtube.com/results?search_query={name}'
    print(url)
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    soup = str(soup)
    result = re.search(r'"videoId":"(\w+)"', soup).group(0)
    result = result.replace('"', "")
    result = result.replace("videoId:", "")
    print(result)
    return(str(result))


def main():
    music("doomer")

if __name__ == "__main__":
    main()