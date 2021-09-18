import requests
from bs4 import BeautifulSoup as bs
import re

def music(name: str):
    name = name.replace(' ', '+')
    url = f'https://www.youtube.com/results?search_query={name}'
    print(url)
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    soup = str(soup)
    result = re.search(r'"videoId":"(\w+)"', soup).group(0)
    result = result.replace('"', "")
    result = result.replace("videoId:", "")
    result = "https://www.youtube.com/watch?v=" + result
    print(result)
    return(result)


def main():
    music("doomer")

if __name__ == "__main__":
    main()