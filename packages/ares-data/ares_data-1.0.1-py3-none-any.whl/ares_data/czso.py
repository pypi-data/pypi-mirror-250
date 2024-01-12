import logging
import requests
import unicodedata

from bs4 import BeautifulSoup

logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.WARNING,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def czso_get_website_content(ico: str):
    url = f"https://apl.czso.cz/res/detail?ico={ico}"
    try:

        response = requests.get(url)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
        content = response.content

        return content

    except requests.RequestException as e:
        logging.error(f"Error occurred: {e}")
        return None


def czso_parse_content(content):
    if content is None:
        logging.warning("No content to parse.")
        return None

    try:
        soup = BeautifulSoup(content, "html.parser")
        data = soup.select(
            "body > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(7) > div:nth-of-type(2)"
        )

        # Normalize unicode characters in the extracted data
        normalized_data = [
            unicodedata.normalize("NFKD", item.get_text()) for item in data
        ]

        return normalized_data
    except Exception as e:
        logging.error(f"Error occurred while parsing: {e}")
        return None


def get_main_cz_nace(ico:str) -> str | None:
    try:
        content = czso_get_website_content(ico)
        cz_nace = czso_parse_content(content)[0]
        return cz_nace
    except IndexError:
        return None


def main():
    pass


if __name__ == "__main__":
    main()
