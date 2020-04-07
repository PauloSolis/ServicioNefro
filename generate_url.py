#!/usr/bin/python

from google.cloud import storage
from datetime import timedelta
import uuid
import sys

if len(sys.argv) == 2:
    file_name = sys.argv[1]
else:
    file_name = uuid.uuid1().hex

if len(sys.argv) == 3:
    content_type = sys.argv[2]
else:
    content_type = 'application/octet-stream'

bucket = storage.Client().get_bucket('nefrovida_develop')
blob = bucket.blob(file_name)
# print(blob.generate_signed_url(method="PUT", expiration=timedelta(minutes=5), content_type=content_type))
