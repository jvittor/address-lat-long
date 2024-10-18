import pandas as pd
from mapbox import Geocoder
import time

def geocode_address(address, geocoder, index):
    try:
        response = geocoder.forward(address).json()
        if response['features']:
            location = response['features'][0]['geometry']['coordinates']
            print(f"{index}: Geocodificado '{address}'")
            return location[1], location[0]  # Latitude, Longitude
        else:
            print(f"{index}: Não foi possível geocodificar '{address}'")
            return None, None
    except Exception as e:
        print(f"{index}: Falha ao geocodificar '{address}' - {e}")
        return None, None

# Adicione sua chave de API do Mapbox aqui
mapbox_token = 'sk.eyJ1Ijoic2luZWNhIiwiYSI6ImNtMmY0aGp1ZzA1Y3gybW9tbDd0NnptNDcifQ.ZlzSXSqG7VJsEp7OJhAq_Q'
geocoder = Geocoder(access_token=mapbox_token)

file_path = 'address-cruz.xlsx' 
df = pd.read_excel(file_path)

latitudes = []
longitudes = []

start_time = time.time()

for i, row in df.iterrows():
    lat, lon = geocode_address(f"{row['endereco']}, {row['municipio']}", geocoder, i)
    latitudes.append(lat)
    longitudes.append(lon)
    if i % 10 == 0: 
        print(f"processados {i+1}/{len(df)} endereços")

df['latitude'] = latitudes
df['longitude'] = longitudes

end_time = time.time()
print(f"tempo total de execução: {end_time - start_time:.2f} segundos")

result_df = df[['latitude', 'longitude']]

output_file_path = 'address-cruz-converted.xlsx' 
result_df.to_excel(output_file_path, index=False)

print("tabela de latitude e longitude criada com sucesso!")
