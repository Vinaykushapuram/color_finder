from flask import Flask, request
from flask_restful import Api, Resource
import cv2
import urllib.request
import numpy as np
import base64
import matplotlib

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def border_color(img):
    size=128
    image = cv2.resize(img, (size,size))
    map_color= {}
    for pixel in image[1]:
        hex_value=rgb_to_hex((pixel[0],pixel[1],pixel[2]))
        if  map_color.__contains__(hex_value):
            map_color[hex_value] += 1
        else:
            map_color[hex_value] = 1
    for pixel in image[size-2]:
      hex_value=rgb_to_hex((pixel[0],pixel[1],pixel[2]))
      if map_color.__contains__(hex_value):
            map_color[hex_value] += 1
      else :
            map_color[hex_value] = 1
    max_hex_value = "000000"
    max_count = 0
    for key, value in map_color.items():
        if value > max_count:
            max_hex_value = key
            max_count = value
    return  "#" + max_hex_value


def primary_color(img):
    size=128
    print(img)
    image = cv2.resize(img, (size, size))
    map_color={}
    for rows in image:
        for pixel in rows:
            hex_value=rgb_to_hex((pixel[0],pixel[1],pixel[2]))
            if map_color.__contains__(hex_value) :
               map_color[hex_value] += 1
            else:
              map_color[hex_value] = 1
    max_hex_value = "000000"
    max_count= 0
    bordr_col=border_color(img);
    for key, value in map_color.items():
        if "#"+key!=bordr_col:
            if  value > max_count:
                max_hex_value= key
                max_count= value
    return  "#"+max_hex_value


app = Flask(__name__)
api = Api(app)


class FindColor(Resource):
    def get(self, url):
        ##url += "=" * ((4 - len(url) % 4) % 4)
        base64_bytes = url.encode('ascii')
        print(url)
        message_bytes = base64.b64decode(base64_bytes)
        decoded_url = message_bytes.decode('ascii')
        resp = urllib.request.urlopen(decoded_url)
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return {'primary_color': primary_color(img), 'border_color': border_color(img)}

api.add_resource(FindColor, "/find_color/<path:url>")

if __name__ == "__main__":
    app.run(debug=True)