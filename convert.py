import pandas as pd
import requests
import time

def geocode_address(address, api_key, index):
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(url).json()
        
        if response['status'] == 'OK' and response['results']:
            location = response['results'][0]['geometry']['location']
            print(f"{index}: Geocodificado '{address}'")
            return location['lat'], location['lng'] 
        else:
            print(f"{index}: Não foi possível geocodificar '{address}' - Status: {response['status']}")
            return None, None
    except Exception as e:
        print(f"{index}: Falha ao geocodificar '{address}' - {e}")
        return None, None


google_api_key = 'api_key'

file_path = 'address-cruz.xlsx' 
df = pd.read_excel(file_path)

latitudes = []
longitudes = []

start_time = time.time()

for i, row in df.iterrows():
    address = f"{row['endereco']}, {row['municipio']}"
    lat, lon = geocode_address(address, google_api_key, i)
    latitudes.append(lat)
    longitudes.append(lon)
    if i % 10 == 0: 
        print(f"Processados {i+1}/{len(df)} endereços")

df['latitude'] = latitudes
df['longitude'] = longitudes

end_time = time.time()
print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")

output_file_path = 'address-cruz-converted-google.xlsx' 
df.to_excel(output_file_path, index=False)

print("Tabela de latitude e longitude criada com sucesso!")
