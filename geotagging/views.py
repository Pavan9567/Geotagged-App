from django.shortcuts import redirect, render
from .models import GeotaggedImage
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from django.http import JsonResponse, HttpResponse
from django.template import loader
import pytesseract
import cv2
import numpy as np

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Create your views here.

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def extract_geolocation(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return None, None
    
    gps_info = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for gps_tag in value:
                gps_name = GPSTAGS.get(gps_tag, gps_tag)
                gps_info[gps_name] = value[gps_tag]

    def convert_to_degrees(value):
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)
    
    lati = gps_info.get("GPSLatitude")
    longi = gps_info.get("GPSLongitude")

    if lati and longi:
        lati_ref = gps_info.get("GPSLatitudeRef", "N")
        longi_ref = gps_info.get("GPSLongitudeRef", "E")
        lati = convert_to_degrees(lati)
        longi = convert_to_degrees(longi)
        if lati_ref != "N":
            lati = -lati
        if longi_ref != "E":
            longi = -longi
    else:
        return None, None
    return lati, longi

def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        lati, longi = extract_geolocation(uploaded_image)
        text = pytesseract.image_to_string(Image.open(uploaded_image))
        geotagged_image = GeotaggedImage(
            image = uploaded_image,
            extracted_data = text,
            latitude = lati or 0.0,
            longitude = longi or 0.0
        )
        geotagged_image.save()
        return redirect('image_list')
    
    return render(request, "upload.html")

def geotagged_data_view(request):
    geotagged_data = GeotaggedImage.objects.all()
    return render(request, 'geotagged_data.html', {'geotagged_data': geotagged_data})

def geotagged_data_api(request):
    images = GeotaggedImage.objects.all()
    data = [
        {
            "id": image.id,
            "latitude": image.latitude,
            "longitude": image.longitude,
            "extracted_data": image.extracted_data,
            "timestamp": image.timestamp
        }
        for image in images
    ]
    return JsonResponse(data, safe=False)

def image_list(request):
    images = GeotaggedImage.objects.all()
    return render(request, 'images.html', {'images': images})

def map_visualization(request):
    return render(request, 'map.html')

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(image)

def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        temp_path = f"temp_{uploaded_image.name}"
        with open(temp_path, 'wb+') as temp_file:
            for chunk in uploaded_image.chunks():
                temp_file.write(chunk)
        lati, longi = extract_geolocation(temp_path)
        processed_image = preprocess_image(temp_path)
        text = pytesseract.image_to_string(processed_image)
        geotagged_image = GeotaggedImage(
            image = uploaded_image,
            extracted_data = text,
            latitude = lati or 0.0,
            longitude = longi or 0.0
        )
        geotagged_image.save()
        return redirect('image_list')
    
    return render(request, "upload.html")