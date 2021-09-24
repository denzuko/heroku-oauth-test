#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
baseapi JSON-LD meta data
"""

__all__ = [
     '__author__',
     '__copyright__',
     '__credits__',
     '__email__', 
     '__license__',
     '__maintainer__',
     '__status__',
     '__version__', 
]

__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__copyright__ = 'Copyright (c) 2011-2018 Digital Bazaar, Inc.'
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley","Matthew Wakefield"]
__email__ = "rob@spot.colorado.edu"
__license__ = 'New BSD license'
__maintainer__ = "Rob Knight"
__status__ = "Production"
__version__ = "1.0.1"

from eve import Eve
from eve_swagger import swagger
from invoke import task

def schema():
    return {
            "test": {},
            "users": {
                'item_title': 'member',
                'schema': {
                    'username': {
                        "type": str(),
                        "minlength": 5,
                        "maxlength": 25,
                    },
                }
            }
        }
  
def openapi_info():
    return {
            'title': 'Example API',
            'version': "v1",
            'description': 'an API description',
            'termsOfService': 'my terms of service',
            'contact': {
                'name': 'Dwight (@denzuko) Spencer',
                'url': 'http://dwightaspencer.com'
            },
            'license': {
                'name': 'BSD',
                'url': 'https://denzuko.github.io/LICENSE.md',
            },
            'schemes': ['http', 'https']
    }

def settings():
    return {
        "DEBUG": True,
        "API_VERSION": 'v1',
        "RENDERERS": ['eve.render.JSONRenderer'],
        "X_DOMAINS": ['*', 'http://editor.swagger.io' ],
        "X_HEADERS": ['Content-Type', 'If-Match'],
        "CACHE_CONTROL": 'max-ege=20',
        "CACHE_EXPIRES": 20,
        "RESOURCE_METHODS": ["GET", "DELETE", "POST"],
        "ITEM_METHODS": ["GET", "PUT", "DELETE"],
        "SWAGGER_INFO": openapi_info(),
        "DOMAIN": schema()
    }


@task
def proxy(ctx):
     ctx.run(" ".join([
          'oauth2-proxy',
          '--provider=github',
          '--http-address', '0.0.0.0:${PORT}',
          '--reverse-proxy',
          '--upstream', '"http://localhost:3000"']))
     
@task
def migrate(ctx):
     pass

@task(default=True)
def serve(ctx):

    app = Eve(auth=None, settings=settings())
    app.register_blueprint(swagger)

    app.run(host='0.0.0.0', port=3000)
