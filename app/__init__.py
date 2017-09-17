from flask import Flask, render_template, jsonify, make_response, request, send_from_directory
from app.util import gzipped
import os
from clarifai.rest import ClarifaiApp, Image as ClImage, ApiError


app = Flask(__name__)
app.config.from_object('config')
clari = ClarifaiApp(api_key='YOUR-API-KEY')             # API key for Clarifai


@app.route('/')
@gzipped
def home():
    return render_template('hotdog.html')


@app.route('/nothotdog', methods=['GET', 'POST'])
@gzipped
def hotdog_url():
    img_link = request.form['url_link']                 # Get the url link from the input field

    return hotdog_or_nothotdog(img_link)


def hotdog_or_nothotdog(image_url):
    try:
        model = clari.models.get('food-items-v1.0')
        image = ClImage(url=image_url)
        response_data = model.predict([image])

        concepts = response_data['outputs'][0]['data']['concepts']
        concept_names = [concept['name'] for concept in concepts]

        if 'hot dog' in concept_names:
            return jsonify({'status': 200, 'msg': 'Yumm that\'s a good looking Hotdog!!'})

        return jsonify({'status': 200, 'msg': 'This is DEFINITELY not a Hotdog!'})

    except ApiError:                                    # Happens when the url can't be decoded properly
        return jsonify({'status': 500, 'error': 'Unable to find an image from this link.'})


""" Compress Static files """


# Template for serving static resources
def _response_path(static_path):
    return make_response(send_from_directory(os.path.join(app.root_path, 'static'), static_path))


""" CSS """


@app.route('/static/assets/css/bootstrap.min.css')
@gzipped
def css_bootstrap():
    return _response_path('assets/css/bootstrap.min.css')


@app.route('/static/assets/css/gsdk-bootstrap-wizard.css')
@gzipped
def css_material_dashboard():
    return _response_path('assets/css/gsdk-bootstrap-wizard.css')


""" JS """


@app.route('/static/assets/js/bootstrap.min.js')
@gzipped
def js_bootstrap():
    return _response_path('assets/js/bootstrap.min.js')


@app.route('/static/assets/js/jquery-2.2.4.min.js')
@gzipped
def js_material():
    return _response_path('assets/js/jquery-2.2.4.min.js')


@app.route('/static/assets/js/jquery.bootstrap.wizard.js')
@gzipped
def js_stats():
    return _response_path('assets/js/jquery.bootstrap.wizard.js')


@app.route('/static/assets/js/gsdk-bootstrap-wizard.js')
@gzipped
def js_chartist():
    return _response_path('assets/js/gsdk-bootstrap-wizard.js')


@app.route('/static/assets/js/jquery.validate.min.js')
@gzipped
def js_notify():
    return _response_path('assets/js/jquery.validate.min.js')
