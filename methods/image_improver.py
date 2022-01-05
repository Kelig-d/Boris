import urllib.request
import requests
import base64
import json

def ImageImprover(link, image):
            if link:
                image_url = link[0]
            else:
                image_url = image.url
                image_segment = image_url.split(".")
                image_extension = image_segment[len(image_segment)-1]
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            opener.retrieve(image_url, 'images/image_to_improve.'+image_extension)
            encoded_image = base64.b64encode(open("images/image_to_improve."+image_extension, "rb").read())
            encoded_image_clean = str(encoded_image)[2:]
            string_json = {
                "data": [
                    'data:image/'+image_extension+';base64,'+encoded_image_clean,
                    'base'
                ]
            }
            json_to_send = json.dumps(string_json)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url='https://hf.space/gradioiframe/akhaliq/Real-ESRGAN/api/predict', data=json_to_send, headers= headers)
            json_data = r.json()["data"]
            all_data_string = str(json_data)
            image_data = all_data_string[24:]
            image_result = open('images/image_improved.jpg','w').close()
            image_result = open('images/image_improved.jpg','wb')
            image_result.write(base64.b64decode(image_data))