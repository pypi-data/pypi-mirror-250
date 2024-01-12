# Ares Data

`ares_data` je Python knihovna pro snadné získávání dat o společnostech z Českého obchodního rejstříku ARES.

## Funkce

- Jednoduché rozhraní pro získávání dat o společnostech podle IČO.
- Jako objekt AresCompany.

## Instalace

Pro instalaci `ares_data` použijte následující příkaz:

```bash
pip install ares_data
```

## Použití 

Použití knihovny ares_data je jednoduché. Zde je příklad, jak získat data o společnosti:

```python
from ares_data import get_company_data

ico = "60193336"
company_data = get_company_data(ico)
print(company_data)
```

Tento příklad demonstruje, jak naimportovat a použít funkci get_company_data z knihovny ares_data. Funkce bere jako parametr identifikační číslo organizace (IČO). Pokud chcete rozšířit data o hlavní ekonomickou činnost společnosti podle CZNACE, přidejte parametr main_cz_nace_important=True. To však celý proces významně zpomalí, protože dochází k parsování stránky https://apl.czso.cz.

Formát vráceného objektu (pokud není chybový), je:
```python
@dataclass
class AresCompany:
    ico: str
    name: Optional[str]
    address: Optional[str]
    psc: Optional[str]
    legal_form: Optional[str]
    business_fields: Optional[List[str]]
    size: Optional[str]
    main_cz_nace: Optional[str] = None
```

