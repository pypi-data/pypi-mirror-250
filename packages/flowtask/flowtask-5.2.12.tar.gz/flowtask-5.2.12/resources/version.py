"""version.

Extract the version of all required packages and showed in a response.
"""
import importlib
from aiohttp import web

# TODO: Add Qworker, Scheduler and other DI packages.
package_list = (
    'asyncdb',
    'querysource',
    'notify',
    'navconfig',
    'navigator',
    'dataintegration',
    'navigator_auth',
    'qw'
)


async def get_versions(request):
    """
    ---
    summary: Return version of all required packages
    tags:
    - version
    produces:
    - application/json
    responses:
        "200":
            description: list of packages and versions.
    """
    versions = {}
    for package in package_list:
        mdl = importlib.import_module(f'{package}.version', package='version')
        obj = getattr(mdl, '__version__')
        versions[package] = obj
    return web.json_response(versions, status=200)
