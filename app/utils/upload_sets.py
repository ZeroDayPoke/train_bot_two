#!/usr/bin/env python3

from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
