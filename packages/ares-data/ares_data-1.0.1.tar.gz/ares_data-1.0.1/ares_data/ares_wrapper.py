import csv
import requests
import logging
import pathlib

from dataclasses import dataclass
from typing import List, Optional

from .czso import get_main_cz_nace

logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.WARNING,
    datefmt="%Y-%m-%d %H:%M:%S",
)


current_directory = pathlib.Path(__file__).parent
cznace_csv_path = current_directory / "cznace.csv"
pocet_pracovniku_csv_path = current_directory / "pocet_pracovniku.csv"


@dataclass
class AresCompany:
    ico: str
    name: Optional[str]
    address: Optional[str]
    psc: Optional[str]
    legal_form: Optional[str]
    business_fields: Optional[List[str]]
    size: Optional[str]
    main_cz_nace: Optional[str] = None # Hlavní ekonomická činnost (CZ NACE)


legal_forms = {
    "100": "Podnikající fyzická osoba tuzemská fyzická osoba",
    "111": "Veřejná obchodní společnost",
    "112": "Společnost s ručením omezeným",
    "113": "Společnost komanditní",
    "114": "Společnost komanditní na akcie",
    "115": "Společný podnik",
    "116": "Zájmové sdružení",
    "117": "Nadace",
    "118": "Nadační fond",
    "121": "Akciová společnost",
    "131": "Svépomocné zemědělské družstvo",
    "141": "Obecně prospěšná společnost",
    "145": "Společenství vlastníků jednotek",
    "151": "Komoditní burza",
    "152": "Garanční fond obchodníků s cennými papíry",
    "161": "Ústav",
    "201": "Zemědělské družstvo",
    "205": "Družstvo",
    "211": "Družstevní podnik zemědelský",
    "231": "Výrobní družstvo",
    "232": "Spotřební družstvo",
    "233": "Bytové družstvo",
    "234": "Jiné družstvo",
    "241": "Družstevní podnik (s 1 zakladatelem)",
    "242": "Společný podnik (s více zakladateli)",
    "251": "Zájmová organizace družstev",
    "261": "Společná zájmová organizace družstev",
    "301": "Státní podnik",
    "302": "Národní podnik",
    "311": "Státní banka československá",
    "312": "Banka-státní peněžní ústav",
    "313": "Česká národní banka",
    "314": "Česká konsolidační agentura",
    "325": "Organizační složka státu",
    "326": "Stálý rozhodčí soud",
    "331": "Příspěvková organizace zřízená územním samosprávným celkem",
    "332": "Státní příspěvková organizace",
    "333": "Státní příspěvková organizace ostatní",
    "341": "Státní hospodářská organizace řízená okresním úřadem",
    "343": "Obecní podnik",
    "351": "Československé státní dráhy-státní organizace",
    "352": "Správa železniční dopravní cesty, státní organizace",
    "353": "Rada pro veřejný dohled nad auditem",
    "361": "Veřejnoprávní instituce",
    "362": "Česká tisková kancelář",
    "381": "Státní fond ze zákona",
    "382": "Státní fond ze zákona nezapisující se do obchodního rejstříku",
    "391": "Zdravotní pojišťovna (mimo VZP)",
    "392": "Všeobecná zdravotní pojišťovna",
    "401": "Sdružení mezinárodního obchodu",
    "411": "Podnik se zahraniční majetkovou účastí",
    "421": "Odštěpný závod zahraniční právnické osoby",
    "422": "Organizační složka zahraničního nadačního fondu",
    "423": "Organizační složka zahraniční nadace",
    "424": "Zahraniční fyzická osoba fyzická osoba",
    "425": "Odštěpný závod zahraniční fyzické osoby",
    "426": "Zastoupení zahraniční banky",
    "441": "Podnik zahraničního obchodu",
    "442": "Účelová zahraničně obchodní organizace",
    "501": "Odštěpný závod",
    "521": "Samostatná drobná provozovna (obecního úřadu)",
    "525": "Vnitřní organizační jednotka organizační složky státu",
    "601": "Vysoká škola (veřejná, státní)",
    "641": "Školská právnická osoba",
    "661": "Veřejná výzkumná instituce",
    "671": "Veřejné neziskové ústavní zdravotnické zařízení",
    "701": "Občanské sdružení",
    "703": "Odborová organizace a organizace zaměstnavatelů",
    "704": "Zvláštní organizace pro zastoupení českých zájmů v mezinárodních nevládních organizacích",
    "705": "Podnik nebo hospodářské zařízení sdružení",
    "706": "Spolek",
    "707": "Odborová organizace",
    "708": "Organizace zaměstnavatelů",
    "711": "Politická strana, politické hnutí",
    "715": "Podnik nebo hospodářské zařízení politické strany",
    "721": "Církve a náboženské společnosti",
    "722": "Evidované církevní právnické osoby",
    "723": "Svazy církví a náboženských společností",
    "731": "Organizační jednotka občanského sdružení",
    "733": "Pobočná odborová organizace a organizace zaměstnavatelů",
    "734": "Organizační jednotka zvláštní organizace pro zastoupení českých zájmů v mezinárodních nevládních organizacích",
    "736": "Pobočný spolek",
    "741": "Samosprávná stavovská organizace (profesní komora)",
    "745": "Komora (hospodářská, agrární)",
    "751": "Zájmové sdružení právnických osob",
    "761": "Honební společenstvo",
    "771": "Dobrovolný svazek obcí",
    "801": "Obec",
    "804": "Kraj",
    "805": "Regionální rada regionu soudržnosti",
    "811": "Městská část, městský obvod",
    "906": "Zahraniční spolek",
    "907": "Mezinárodní odborová organizace",
    "908": "Mezinárodní organizace zaměstnavatelů",
    "921": "Mezinárodní nevládní organizace",
    "922": "Organizační jednotka mezinárodní nevládní organizace",
    "931": "Evropské hospodářské zájmové sdružení",
    "932": "Evropská společnost",
    "933": "Evropská družstevní společnost",
    "936": "Zahraniční pobočný spolek",
    "937": "Pobočná mezinárodní odborová organizace",
    "938": "Pobočná mezinárodní organizace zaměstnavatelů",
    "941": "Evropské seskupení pro územní spolupráci",
    "960": "Právnická osoba zřízená zvláštním zákonem zapisovaná do veřejného rejstříku",
    "961": "Svěřenský fond",
    "962": "Zahraniční svěřenský fond"
}



def validation_ico(ico:str) -> bool:
    """
    Funkce pro kontrolu platnosti IČO podle českých pravidel.

    Args:
    ico (str): IČO k ověření.

    Returns:
    bool: True pokud je IČO platné, jinak False.
    """
    if len(ico) != 8 or not ico.isdigit():
        return False
    vahy = [8, 7, 6, 5, 4, 3, 2]
    vazeny_soucet = sum(int(ico[i]) * vahy[i] for i in range(7))
    kontrolni_cislice = (11 - vazeny_soucet % 11) % 10
    return kontrolni_cislice == int(ico[7])



def translate_legal_form(legal_form_code: str) -> str:
    return legal_forms.get(legal_form_code, legal_form_code)


def find_cznace_description(key):
    try:
        with open(cznace_csv_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row['id_cznace'] == key:
                    return row['text_cznace']
            logging.info(f'Žádný popis pro id_cznace: {key} nebyl nalezen.')
            return None
    except Exception as e:
        logging.error(f'Chyba při načítání nebo vyhledávání v souboru {cznace_csv_path}: {e}')
        return None


def find_company_size(chodnota):
    try:
        with open(pocet_pracovniku_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                if row['chodnota'] == chodnota:
                    return row['zkrtext']
            logging.info(f'Žádná velikost společnosti pro chodnota: {chodnota} nebyla nalezena.')
            return None
    except Exception as e:
        logging.error(f'Chyba při načítání nebo vyhledávání v souboru {pocet_pracovniku_csv_path}: {e}')
        return None



def get_company_data(ico: str, main_cz_nace_important:bool = False) -> Optional[AresCompany] | str:
    """
    Retrieves data about a company from the ARES registry using the given ICO (Identification Number of the Organization).

    Args:
        ico (str): The ICO of the company for which data is to be retrieved.
        main_cz_nace_important (bool, optional): Flag to indicate if main CZ NACE (main economic activity) is important. Defaults to False.

    Returns:
        Optional[AresCompany] | str: An AresCompany object with the retrieved company data if successful, a string indicating an error ('IČO is not valid!' if ICO is invalid), or None if the request fails or no records are found.
    """

    if not validation_ico(ico):
        return "IČO is not valid!"
    
    ares_url: str = f'https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-res/{ico}'
    response = requests.get(ares_url, headers={'accept': 'application/json'})
    if response.status_code != 200:
        logging.error(f"Status code for request to {ares_url} is {response.status_code}")
        return None

    data = response.json()
    records = data.get("zaznamy", [])
    if not records:
        logging.error("Žádné záznamy.")
        return None

    record:dict = records[0]
    address_components = record.get('sidlo', {})
    address = address_components.get('textovaAdresa')
    psc = address_components.get('psc')
    business_field_codes = record.get('czNace', [])
    business_field_descriptions = [find_cznace_description(code) for code in business_field_codes if isinstance(find_cznace_description(code), str)]
    kategorie_poctu_pracovniku:str = record.get("statistickeUdaje").get("kategoriePoctuPracovniku")

    if main_cz_nace_important:
        company_data = AresCompany(
            ico=record.get('ico'),
            name=record.get('obchodniJmeno'),
            address=address,
            psc=str(psc) if psc else None,
            legal_form=translate_legal_form(record.get('pravniForma')),
            business_fields=business_field_descriptions,
            size=find_company_size(kategorie_poctu_pracovniku),
            main_cz_nace=get_main_cz_nace(ico)
        )
    else:
            company_data = AresCompany(
            ico=record.get('ico'),
            name=record.get('obchodniJmeno'),
            address=address,
            psc=str(psc) if psc else None,
            legal_form=translate_legal_form(record.get('pravniForma')),
            business_fields=business_field_descriptions,
            size=find_company_size(kategorie_poctu_pracovniku),
            main_cz_nace="Nepožadováno"
        )

    return company_data



def main():
    pass

if __name__ == "__main__":
    main()
