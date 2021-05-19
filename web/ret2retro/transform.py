import hashlib
import tensorflow as tf

from glitcher.main import glitch_bytes_io
from nn.nn import ImageClassifier

from io import BytesIO

from functools import partial
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor

from ret2retro.storages.fs_storage import FsStorage
from ret2retro.config import UPLOAD_PATH, IS_PRODUCTION, WORKER_COUNT
from ret2retro.flag_hustler import get_part, encrypt, mix_data_to_img

pool_executor = ThreadPoolExecutor(max_workers=WORKER_COUNT)
graph = tf.get_default_graph()
classifier = ImageClassifier()



def process_image(data):
    global graph
    storage = FsStorage(UPLOAD_PATH)
    md5 = hashlib.md5()
    md5.update(data)
    name = md5.hexdigest()[:16]
    filename = f'{name}.png'
    transformed_data = storage.get_resource(filename)
    if not transformed_data:
        with graph.as_default():
            score = classifier.score(data)
        buffer = BytesIO(data)
        flag_part = get_part(score)
        encrypted_flag_part = encrypt(flag_part.encode())
        transformed_data = glitch_bytes_io(buffer, score)
        mixed_data = mix_data_to_img(transformed_data, encrypted_flag_part)
        storage.add_resource(filename, mixed_data)
    extension = 'png'
    return filename, transformed_data, extension

async def process_image_async(data):
    loop = get_event_loop()
    if IS_PRODUCTION:
        name, transformed_image, extension = await loop.run_in_executor(
            pool_executor,
            partial(process_image, data)
        )
    else:
        name, transformed_image, extension = process_image(data)
    return name, transformed_image, extension
