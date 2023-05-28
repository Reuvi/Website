import requests

url = 'http://50.116.61.76/upload'  # Website IP

image_path = 'image.jpg'  # Path to the image file in your local directory

with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    response = requests.post(url, files=files)

if response.status_code == 200:
    print('Image upload successful')
else:
    print('Error:', response.json()['error'])
