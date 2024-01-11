import requests
import json

def ip_info(ip_address):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    api_url = f'https://ipapi.co/{ip_address}/json/'
    headers = {'Accept': 'application/json', 'User-Agent': user_agent}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        ip_info = response.json()

        ip_info_formatted = {
            "IP Address": ip_info.get('ip'),
            "Network": ip_info.get('network'),
            "Version": ip_info.get('version'),
            "City": ip_info.get('city'),
            "Region": ip_info.get('region'),
            "Region Code": ip_info.get('region_code'),
            "Country": f"{ip_info.get('country_name')} ({ip_info.get('country_code')})",
            "Country ISO Code": ip_info.get('country_code_iso3'),
            "Country Capital": ip_info.get('country_capital'),
            "Country TLD": ip_info.get('country_tld'),
            "Continent Code": ip_info.get('continent_code'),
            "In EU": ip_info.get('in_eu'),
            "Postal Code": ip_info.get('postal'),
            "Latitude": ip_info.get('latitude'),
            "Longitude": ip_info.get('longitude'),
            "Timezone": ip_info.get('timezone'),
            "UTC Offset": ip_info.get('utc_offset'),
            "Country Calling Code": ip_info.get('country_calling_code'),
            "Currency": f"{ip_info.get('currency')} ({ip_info.get('currency_name')})",
            "Languages": ip_info.get('languages'),
            "Country Area": f"{ip_info.get('country_area')} km²",
            "Country Population": ip_info.get('country_population'),
            "ASN Number": ip_info.get('asn'),
            "Organization": ip_info.get('org'),
            "Google Map": f"https://www.google.com/maps/@{ip_info.get('latitude')},{ip_info.get('longitude')},12z",
            "code": "By: @SaMi_ye"
        }

        return {"status": "success", "response": ip_info_formatted}
    
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}

