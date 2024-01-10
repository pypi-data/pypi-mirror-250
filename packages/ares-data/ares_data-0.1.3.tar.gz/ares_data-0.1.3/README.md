# Ares Data

`ares_data` je Python knihovna pro snadné získávání dat o společnostech z Českého obchodního rejstříku ARES.

## Funkce

- Jednoduché rozhraní pro získávání dat o společnostech podle IČO.
- Vrací data ve formátu JSON.

## Instalace

Pro instalaci `ares_data` použijte následující příkaz:

```bash
pip install ares_data
```

## Použití 

Použití knihovny ares_data je jednoduché. Zde je příklad, jak získat data o společnosti:

```python
from ares_data import get_company_data

ico = "01220551"
company_data = get_company_data(ico)
print(company_data)
```

Tento příklad demonstruje, jak naimportovat a použít funkci get_company_data z knihovny ares_data. Funkce bere jako parametr identifikační číslo organizace (IČO) a vrací data o dané společnosti ve formátu JSON.

## Chybové stavy 

Pokud dojde k chybě (například neplatné IČO), get_company_data vrátí slovník s informacemi o chybě:

```json
{
    "error": "Popis chyby",
    "details": ...  # Další detaily chyby
}
```
