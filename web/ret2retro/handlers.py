import aiohttp_jinja2
from aiohttp import web

from ret2retro.config import UPLOAD_PATH
from ret2retro.storages.fs_storage import FsStorage
from ret2retro.exceptions import ValidationError
from ret2retro.transform import process_image_async
from ret2retro.validate import clean_file


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


async def transform_image(request):
    multipart_data = await request.post()
    try:
        *_, content = clean_file(multipart_data)
    except ValidationError as ve:
        response = aiohttp_jinja2.render_template('index.html', request, {
            'errors': {
                ve.field_name: ve.errors
            }
        })
        response.set_status(400)
        return response
    name, result, extension = await process_image_async(content)
    return web.HTTPFound(f'/result?name={name}')


async def glitched_image(request):
    storage = FsStorage(UPLOAD_PATH)
    try:
        image = request.query['name']
    except KeyError:
        return web.HTTPNotFound()

    if image == '':
        return web.HTTPNotFound()

    if 'proc' in image:
        return web.HTTPForbidden()

    data = storage.get_resource(f'{image}')
    if data:
        return web.Response(body=data, content_type='image/png', headers={
            'Content-Disposition': f'inline; filename="{image}"'
        }, status=200)
    return web.HTTPNotFound()


async def redirect_to_main(request):
    return web.HTTPFound('/')
