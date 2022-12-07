import time
start_millis = int(round(time.time() * 1000))

global end_millis
end_millis = None

import os
import glob
import json
import oss2
from flask import Flask, flash, request, json,\
        render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from shutil import copyfile
import tarfile
import traceback
from PIL import Image

from settings import UPLOAD_FOLDER, TEST_DIR, \
        ALLOWED_EXTENSIONS, IMAGE_INFO_JSON, IS_DEBUG, SAVE_INFO_ON_OSS
from fc_context import FC_CONTEXT
from predict import predict

INIT_IMAGE_INFO_DONE = False

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'some_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MODEL_DIR = 'model'

# used for rendering after feedback
#CURRENT_IMAGE_INFO = os.path.join(UPLOAD_FOLDER, 'current_image_info.json')
#MODEL_OSS_BUCKET = os.environ['MODEL_OSS_BUCKET']
#MODEL_FILE_OSS_KEY = os.environ["MODEL_FILE_OSS_KEY"]

tarfile_name = "models.tar.gz"
tarfile_path = os.path.join(MODEL_DIR, tarfile_name)
print(tarfile_path)
# tf = tarfile.open(tarfile_path)
# tf.extractall(path=MODEL_DIR)
 
def download_file_from_oss(oss_client, source_file, target_file):
  try:
      print('\nLatest Downloading %s from OSS %s to %s' % (source_file, MODEL_OSS_BUCKET, target_file))
      oss_client.get_object_to_file(source_file, target_file)
      print('\nDownloading %s from OSS %s to %s' % (source_file, MODEL_OSS_BUCKET, target_file))
  except:
      print(traceback.format_exc())

def resize_img(src_file, dst_file, width=128, height=128):
    img=Image.open(src_file)
    try:
        new_img=img.resize((width,height),Image.BILINEAR)   
        new_img.save(dst_file)
    except Exception as e:
        print(traceback.format_exc())

def update_fc_context():
    # update FC_CONTEXT
    FC_CONTEXT.access_key_id = request.headers.get('x-fc-access-key-id')
    FC_CONTEXT.access_key_secret = request.headers.get(
        'x-fc-access-key-secret')
    FC_CONTEXT.security_token = request.headers.get('x-fc-security-token')
    FC_CONTEXT.region = request.headers.get('x-fc-region')
    FC_CONTEXT.account_id = request.headers.get('x-fc-account-id')


def init_image_info():
    """Init settings.IMAGE_INFO_JSON using file stored on OSS for
    warm start.
    """
    update_fc_context()

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    global INIT_IMAGE_INFO_DONE
    if INIT_IMAGE_INFO_DONE:
        print("init_image_info is already done!")
        return

    if SAVE_INFO_ON_OSS:
        json_info_key = IMAGE_INFO_JSON.replace(app.config['UPLOAD_FOLDER'],
                                                '').replace('/', '')
        try:
            auth = oss2.StsAuth(FC_CONTEXT.access_key_id,
                                FC_CONTEXT.access_key_secret,
                                FC_CONTEXT.security_token)
            bucket = oss2.Bucket(
                auth, "http://oss-{}-internal.aliyuncs.com".format(
                    FC_CONTEXT.region), os.environ['OSS_BUCKET_NAME'])
            for obj in oss2.ObjectIterator(bucket):
                if obj.key == json_info_key:
                    res = bucket.get_object(json_info_key)
                    image_info = json.loads(res.read().decode('utf-8'))
                    print("init_image_info, from oss get: {0}".format(
                        image_info))

                    # merge local result
                    local_info = {}
                    if os.path.exists(IMAGE_INFO_JSON):
                        with open(IMAGE_INFO_JSON, 'r') as f:
                            local_info = json.load(f)

                    for k, v in local_info.items():
                        if k not in image_info:
                            image_info[k] = v
                        elif k in image_info and v.get('label',
                                                       '') != 'unknown':
                            image_info[k] = v

                    # initialize local image_info
                    with open(IMAGE_INFO_JSON, 'w') as f:
                        json.dump(image_info, f, indent=4)
                else:  # merge oss pic to local
                    if "/" not in obj.key and allowed_file(obj.key):
                        file_name = os.path.join(app.config['UPLOAD_FOLDER'],
                                                 obj.key)
                        if not os.path.exists(file_name):
                            bucket.get_object_to_file(obj.key, file_name)
        except:
            # when there is no IMAGE_INFO_JSON on OSS
            # just initialize local file and upload later
            print(
                "init_image_info: there is no IMAGE_INFO_JSON on OSS, key = {}"
                .format(json_info_key))
        finally:
            INIT_IMAGE_INFO_DONE = True


@app.route('/generate-gallery', methods=['GET'])
def generate_gallery():
    img_files = glob.glob(os.path.join(TEST_DIR, '*.jpg'))
    for i, src_path in enumerate(img_files):
        if i > 1000: break
        file_name = src_path.split('/')[-1]

        dst_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        if not os.path.exists(dst_path):
            copyfile(src_path, dst_path)
            prob = predict(dst_path, MODEL_DIR)
            save_image_info(file_name, prob)

    images, cur_accuracy, num_stored_images = get_stat_of_recent_images()
    return render_template('index.html',
                           images=images,
                           cur_accuracy=cur_accuracy,
                           num_stored_images=num_stored_images)

def predict_image_in_main():
    """View that receive images and render predictions
    """
    # save image for prediction and rendering
    file_path = "./static/images/cat.0.jpg"

    resize_img(file_path, file_path)
    prob = predict(file_path, MODEL_DIR)

    end_millis = int(round(time.time() * 1000))
    info = {'prob': prob, 'start_millis': start_millis, 'end_millis': end_millis, 'latency_latency': end_millis - start_millis}
    return info
# @app.route('/predict_image', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def predict_image():
    """View that receive images and render predictions
    """
    if request.method == 'POST':
        # save image for prediction and rendering
        file_path = "./static/images/cat.0.jpg"

        resize_img(file_path, file_path)
        prob = predict(file_path, MODEL_DIR)
	
        end_millis = int(round(time.time() * 1000))
        info = {'prob': prob, 'start_millis': start_millis, 'end_millis': end_millis, 'latency_latency': end_millis - start_millis}
        return info

@app.route('/invoke', methods=['GET', 'POST'])
def make_prediction():
    """View that receive images and render predictions
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # security concerns
            filename = secure_filename(file.filename)

            # save image for prediction and rendering
            file_path = save_image(file, filename)
            # resize image
            resize_img(file_path, file_path)
            prob = predict(file_path, MODEL_DIR)

            # save image info
            save_image_info(filename, prob)

            # keep record of current prediction for later rendering
            # after getting user feedback
            info = {'prob': prob, 'file_name': filename}
            with open(CURRENT_IMAGE_INFO, 'w') as f:
                json.dump(info, f, indent=4)

            # get information of gallery
            images, cur_accuracy, num_stored_images = get_stat_of_recent_images(
            )

            return render_template('index.html',
                                   cat_prob=float('{:.1f}'.format(prob * 100)),
                                   dog_prob=float('{:.1f}'.format(
                                       (1 - prob) * 100)),
                                   cur_image_path=file_path,
                                   images=images,
                                   num_stored_images=num_stored_images,
                                   cur_accuracy=cur_accuracy,
                                   show_feedback=True)

    # get information of gallery when receive GET request
    images, cur_accuracy, num_stored_images = get_stat_of_recent_images()
    return render_template('index.html',
                           images=images,
                           cur_accuracy=cur_accuracy,
                           num_stored_images=num_stored_images)


@app.route('/feedback', methods=['POST'])
def save_user_feedback():
    """Save user feedback of current prediction"""

    filename = ""
    prob = None
    # get most recently prediction result
    if os.path.exists(CURRENT_IMAGE_INFO):
        with open(CURRENT_IMAGE_INFO, 'r') as f:
            info = json.load(f)
            filename = info['file_name']
            prob = info['prob']

    label = request.form['label']

    print('save_user_feedback, filename: {}, prob: {}'.format(filename, prob))

    init_image_info()

    if filename:
        # save user feedback in file
        with open(IMAGE_INFO_JSON, 'r') as f:
            image_info = json.load(f)
            image_info[filename]['label'] = label
        with open(IMAGE_INFO_JSON, 'w') as f:
            json.dump(image_info, f, indent=4)

        if SAVE_INFO_ON_OSS:
            save_image_info_on_oss(image_info)

    # get information of gallery
    images, cur_accuracy, num_stored_images = get_stat_of_recent_images()

    return render_template('index.html',
                           prob=float('{:.1f}'.format(prob *
                                                      100)) if prob else 0,
                           cur_image_path=uploaded_image_path(filename),
                           images=images,
                           num_stored_images=num_stored_images,
                           cur_accuracy=cur_accuracy,
                           show_thankyou=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """generate url for user uploaded file"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/initialize', methods=['POST'])
def initialize():
    print("just initialize to import app.py and all dependency")
    # 下载模型文件
    update_fc_context()
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    auth = oss2.StsAuth(FC_CONTEXT.access_key_id, FC_CONTEXT.access_key_secret, FC_CONTEXT.security_token)
    oss_endpoint = "oss-%s-internal.aliyuncs.com" % FC_CONTEXT.region
    oss_client = oss2.Bucket(auth, oss_endpoint, MODEL_OSS_BUCKET)
    tarfile_name = "models.tar.gz"
    tarfile_path = os.path.join(MODEL_DIR, tarfile_name)
    download_file_from_oss(oss_client, MODEL_FILE_OSS_KEY, tarfile_path)
    tf = tarfile.open(tarfile_path)

    tf.extractall(path=MODEL_DIR)
    # 生成 model
    return render_template('init.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def allowed_file(filename):
    """Check whether a uploaded file is valid and allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def uploaded_image_path(filename):
    """generate file path for user uploaded image"""
    return '/'.join((app.config['UPLOAD_FOLDER'], filename))


def get_stat_of_recent_images(num_images=300):
    """Return information of recent uploaded images for galley rendering

    Parameters
    ----------
    num_images: int
        number of images to show at once
    Returns
    -------
    image_stats: list of dicts representing images in last modified order
        path: str
        label: str
        pred: str
        cat_prob: int
        dog_prob: int

    cur_accuracy: float
    num_stored_images: int
        indepenent of num_images param, the total number of images available

    """
    folder = app.config['UPLOAD_FOLDER']

    init_image_info()

    # get list of last modified images
    # exclude .json file and files start with .
    files = ['/'.join((folder, file)) \
        for file in os.listdir(folder) if ('json' not in file) \
        and not (file.startswith('.')) ]

    # list of tuples (file_path, timestamp)
    last_modified_files = [(file, os.path.getmtime(file)) for file in files]
    last_modified_files = sorted(last_modified_files,
                                 key=lambda t: t[1],
                                 reverse=True)
    num_stored_images = len(last_modified_files)

    # read in image info
    with open(IMAGE_INFO_JSON, 'r') as f:
        info = json.load(f)

    # build info for images
    image_stats = []
    for i, f in enumerate(last_modified_files):
        # set limit for rendering pictures
        if i > num_images: break

        path, filename = f[0], f[0].replace(folder, '').replace('/', '')
        cur_image_info = info.get(filename, {})

        prob = cur_image_info.get('prob', 0)
        image = {
            'path': path,
            'label': cur_image_info.get('label', 'unknown'),
            'pred': cur_image_info.get('pred', 'dog'),
            'cat_prob': int(prob * 100),
            'dog_prob': int((1 - prob) * 100),
        }
        image_stats.append(image)

    # comput current accuracy if labels available
    total, correct = 0, 0
    for image in image_stats:
        if image['label'] != 'unknown':
            total += 1
            if image['label'] == image['pred']:
                correct += 1

    try:
        cur_accuracy = float('{:.3f}'.format(correct / float(total)))
    except ZeroDivisionError:
        cur_accuracy = 0

    # print(image_stats)
    # print(cur_accuracy)

    return image_stats, cur_accuracy, num_stored_images


def save_image(file, filename):
    """Save current images to setting.UPLOAD_FOLDER and return the
    corresponding file path. Also save the image to OSS if aws information
    is available.

    Parameters
    ----------
    file: werkzeug.datastructures.FileStorage
    filename: str
        pure file name with extension

    Returns
    -------
    file_path: str
        the complete path of the saved image

    """

    # create folder for storing images if not exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # save image locally
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # save image to OSS
    if SAVE_INFO_ON_OSS:
        file.seek(0)
        auth = oss2.StsAuth(FC_CONTEXT.access_key_id,
                            FC_CONTEXT.access_key_secret,
                            FC_CONTEXT.security_token)
        bucket = oss2.Bucket(
            auth,
            "http://oss-{}-internal.aliyuncs.com".format(FC_CONTEXT.region),
            os.environ['OSS_BUCKET_NAME'])
        bucket.put_object(filename, file.read())
    return file_path


def save_image_info(filename, prob):
    """Save predicted result of the image in a json file locally.
    Also save the json to OSS if aws information is available.

    Parameters
    ----------
    filename: str
        pure file name with extension
    prob: float
        the probability of the image being cat
    """

    # save prediction info locally
    with open(IMAGE_INFO_JSON, 'r') as f:
        image_info = json.load(f)
        image_info[filename] = {
            'prob': float(prob),
            'y_pred': 1 if prob > 0.5 else 0,
            'pred': 'cat' if prob > 0.5 else 'dog',
            'label': 'unknown'
        }
    with open(IMAGE_INFO_JSON, 'w') as f:
        json.dump(image_info, f, indent=4)

    # save image info to OSS
    if SAVE_INFO_ON_OSS:
        save_image_info_on_oss(image_info)


def save_image_info_on_oss(image_info):
    """Save the json file containing image info on OSS

    Parameters
    ----------
    image_info: dict
    """
    update_fc_context()
    auth = oss2.StsAuth(FC_CONTEXT.access_key_id, FC_CONTEXT.access_key_secret,
                        FC_CONTEXT.security_token)
    bucket = oss2.Bucket(
        auth, "http://oss-{}-internal.aliyuncs.com".format(FC_CONTEXT.region),
        os.environ['OSS_BUCKET_NAME'])
    bucket.put_object(IMAGE_INFO_JSON\
        .replace(app.config['UPLOAD_FOLDER'], '').replace('/', ''), json.dumps(image_info, indent=4))


if __name__ == '__main__':
    print("Invoking")
    print(predict_image_in_main())
    print("Invoke done. Can stop trace recording.")
    # application.run(host='0.0.0.0', port=5602)
    app.run(host='0.0.0.0', port=9000, debug=IS_DEBUG)
    # predict('static/uploaded_images/10.jpg')
