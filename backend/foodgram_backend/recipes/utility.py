import json
import os

from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, 'static/data/ingredients.json')

with open(file_path) as file_object:
    contents_json = file_object.read()
    contents = json.loads(contents_json)
