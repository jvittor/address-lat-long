import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
import time

def geocode_address(address, geolocator, index, retries=3):
    for attempt in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                print(f"{index}: Geocodificado '{address}'")
                return location.latitude, location.longitude
            else:
                print(f"{index}: Endereço não encontrado '{address}'")
                return None, None
        except GeocoderTimedOut:
            print(f"{index}: Timeout ao tentar geocodificar '{address}', tentativa {attempt + 1}/{retries}")
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente
        except Exception as e:
            print(f"{index}: Falha ao geocodificar '{address}' - {e}")
            return None, None
    return None, None
file_path = 'address.xlsx' 
df = pd.read_excel(file_path)

geolocator = Nominatim(user_agent="geoapiExercises")

# taxa de limite
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)

latitudes = []
longitudes = []

start_time = time.time()

for i, row in df.iterrows():
    lat, lon = geocode_address(f"{row['endereco']}, {row['municipio']}", geolocator, i)
    latitudes.append(lat)
    longitudes.append(lon)
    if i % 10 == 0: 
        print(f"processados {i+1}/{len(df)} endereços")

df['latitude'] = latitudes
df['longitude'] = longitudes

end_time = time.time()
print(f"tempo total de execução: {end_time - start_time:.2f} segundos")

result_df = df[['latitude', 'longitude']]


output_file_path = 'address-converted.xlsx' 
result_df.to_excel(output_file_path, index=False)

print("tabela de latitude e longitude criada com sucesso!")
