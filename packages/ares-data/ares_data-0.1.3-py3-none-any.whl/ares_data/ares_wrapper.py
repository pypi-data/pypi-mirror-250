import requests

def get_company_data(ico: str):
    """
    Retrieve company data from the ARES registry using the given ICO (Identification Number of the Organization).

    Parameters:
    ico (str): The ICO number of the company to retrieve data for.

    Returns:
    dict: A dictionary containing the company data if successful.
    In case of a validation error, returns a dictionary with details of the error.
    """
    url = f'https://ares.novopacky.com/company/{ico}'
    response = requests.get(url, headers={'accept': 'application/json'})

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 422:
        # Handle validation error
        return {"error": "Validation error", "details": response.json()}
    else:
        # Handle other possible errors
        return {"error": f"An error occurred with status code {response.status_code}"}

def main():
    #ico = "02423243"
    #company_data = get_company_data(ico)
    #print(company_data)
    pass

if __name__ == "__main__":
    main()
