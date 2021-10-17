import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# deploy application
IS_DEBUG = False

# model meta
TEST_DIR = os.path.join(PROJECT_PATH, 'datasets', 'test1')

# Log for tensorboard
LOG_DIR = os.path.join(PROJECT_PATH, 'tensorboard', 'logs')

# image-related
# UPLOAD_FOLDER = 'static/uploaded_images'
UPLOAD_FOLDER = 'static/resized_uploaded_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
IMAGE_INFO_JSON = os.path.join(UPLOAD_FOLDER, 'image_info.json')

SAVE_INFO_ON_OSS = False
