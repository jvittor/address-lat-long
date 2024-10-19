import pandas as pd
import folium

file_path = 'address-cruz-converted-google.xlsx'
df = pd.read_excel(file_path)

map_center = [df['latitude'].mean(), df['longitude'].mean()]
mapa = folium.Map(location=map_center, zoom_start=12)

for i, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"{row['endereco']}, {row['municipio']}").add_to(mapa)
mapa.save('mapa_enderecos.html')

print("Mapa gerado com sucesso!")
