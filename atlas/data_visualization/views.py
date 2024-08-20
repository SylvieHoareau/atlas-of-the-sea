from django.shortcuts import render
from django.conf import settings
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
import io
import urllib, base64
import json
import folium
import subprocess
import os
import geopandas as gpd
import requests

# Create your views here.
def home(request):
    return render(request, 'data_visualization/home.html')

def graphique_view(request):
    # Créer une figure et une trame
    fig, ax = plt.subplots()

    # Générer un graphique simple avec seaborn
    sns.set_theme(style="darkgrid")
    tips = sns.load_dataset("tips")
    sns.barplot(x="day", y="total_bill", data=tips, ax=ax)

    # Sauvegarder la figure dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    # Retourner le graphique en HTML
    return HttpResponse(f'<img src="data:image/png;base64,{uri}"/>')

def carte_view(request):
    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=6)

    # Ajouter un marqueur
    folium.Marker([48.8566, 2.3522], popup="Paris").add_to(m)

    # Sauvegarder la carte dans un fichier HTML
    m.save('map.html')
    with open('map.html', 'r') as file:
        return HttpResponse(file.read())
    
def world_view(request):
    url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/country_shapes/records?limit=100"
    response = requests.get(url)
    data = json.loads(response.text)

    # extraire les données GeoJSON de la réponse de l'API
    geojson_data = {
       "type": "FeatureCollection",
       "features": [
          {
             "type": "Feature",
             "geometry": record["geo_shape"]["geometry"],
             "properties": {
                "name": record["cntry_name"],
                "iso_a3": record["iso3"]
             }
          }
          for record in data["results"]
          if "geo_shape" in record and "geometry" in record["geo_shape"]
       ]
    }
   
    # Créer une carte Folium centrée sur le monde
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Ajouter les données GeoJSON à la carte
    folium.GeoJson(geojson_data).add_to(m)

    # Rendre la carte dans le template
    context = {'map': m._repr_html_()}
    return render(request, 'data_visualization/world.html', context)
    
def r_graphique_view(request):
    # Chemin du répertoire contenant les scripts
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', 'script.R')

    # Chemin de l'image générée
    plot_path = os.path.join(settings.MEDIA_ROOT, 'plot.png')
    # with open(plot_path, 'rb') as f:
    #     image_data = f.read()

     # Appeler le script R et passer par le chemin de l'image
    result = subprocess.run(['Rscript', script_path, plot_path], capture_output=True, text=True)

    # Afficher les messages de débogage
    print(result.stdout)
    print(result.stderr)

    # Chemin relatif pour accéder à l'image via l'URL
    plot_url = os.path.join(settings.MEDIA_URL, 'plot.png')

    # return HttpResponse(image_data, content_type="image/png")
    return render(request, "data_visualization/r_graphique.html", {"plot_url": plot_url})