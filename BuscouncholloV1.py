    #!/usr/bin/env python
#_*_ coding: utf8 _*_

import requests
import json
import time
from bs4 import BeautifulSoup

Webhook = "https://discord.com/api/webhooks/xxxxx"

ofertasAnteriores = []

nuevos = 15

while True:

  if len(ofertasAnteriores) >= 120:
    ofertasAnteriores = ofertasAnteriores[:30]

  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)

  source = requests.get('https://www.buscounchollo.com/').text

  soup = BeautifulSoup(source, 'lxml')

  articulos = soup.find_all('article',class_='panel panel-small post_chollo')

  articulos = articulos[:nuevos]

  for articulo in articulos:

    titulo = articulo.a.strong.text
    print(titulo+' | '+current_time)

    if titulo in ofertasAnteriores:

      print('repetido')

    else:

      ofertasAnteriores.append(titulo)

      print(len(ofertasAnteriores))

      product_link = articulo.find('a', class_='no-underline')
      product_link = product_link.get('href')
      product_link = "https://www.buscounchollo.com"+ product_link
      print(product_link)

      image = articulo.find('img')
      image = image.get('src')
      image = "https:"+ image
      print(image)           


      descripcion = articulo.find('div',class_='description')
      descripcion = descripcion.get_text()
      print(descripcion)


      precio= articulo.find('span', class_='header_chollo_preu_num').text
      print("Precio :", precio)



      def sendwebhook():
          data={
                  "content": "¿Te apetecen unas vacaciones? Nuevo Chollo encontrado!",
                  "embeds": [
          {
            "title": titulo,
            "description": descripcion,
            "url": product_link,
            "color": 48895,
            "fields": [
              {
                "name": "Desde",
                "value": precio+"€ / Pers."
              }
            ],
            "author": {
              "name": "Busco un Chollo Monitor | Vacaciones al mejor precio!"
            },
            "footer": {
              "text": "BuscounChollo.com by jjandula22#8402 | " +current_time,
              "icon_url": "https://www.basket4us.com/blog/wp-content/uploads/2015/12/James-Harden8.jpg"
            },
            "image": {
              "url": image
            }
          }
        ]
      }
          try:
              response = requests.post(Webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})
          except:
              print("Error al enviar el Webhook")

          matches = ['platja aro', 'aro', 'resort']

          try:

            for articulo in matches:
              if articulo in descripcion.lower():
                keyword = articulo
                here={
                  "username": "J's monitors",
                  "content": "Keyword detected: "+keyword+" @here"
                  }
                r = requests.post(Webhook, data=json.dumps(here), headers={"Content-Type": "application/json"})

          except:
            print("error checking for keywords")

      sendwebhook()

  time.sleep(10)
            






#precio_descuento = articulo.find('span', class_='thread-price text--b cept-tp size--all-l size--fromW3-xl').text
#print("Nuevo precio :", precio_descuento)
