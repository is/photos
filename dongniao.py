import pprint
import requests
import json

from PIL import Image

import logging
from http.client import HTTPConnection  # py3
log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)
# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)
# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 1

FN = 'I_08326__20220315_102114.jpg'

# ===
def main():
    img = Image.open(FN)
    w, h = img.size
    w2 = int(w/2)
    h2 = int(h/2)
    w4 = int(w/4)
    h4 = int(h/4)

    
    if w > h:
        B = (w2 - h4, h2 - h4, w2 + h4, h2 + h4)
    else:
        B = ((w2 - w4, h2 - w4, w2 + w4, h2 + w4))
    pprint.pprint(B)
    img2 = img.crop(B)
    img2.save('__center.jpg')
    for n in (150,200,256,320,480,512,640):
        img3 = img2.resize((n, n))
        img3.save(f'__center_{n}.jpg')

    headers = {
        'Origin': 'https://dongniao.net',
        'Referer': 'https://dongniao.net',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

    R = requests.post('https://dongniao.net/niaodian2', files={
        'image':('blob', open('__center_640.jpg', 'rb'), 'image/jpeg')},
        data={'async':'0', 'sc':'web'})

    print(R.headers)
    print(R.content)
    s = json.loads(R.text)
    pprint.pprint(s)
    #print(R.text)

if __name__ == '__main__':
    main()
