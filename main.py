import sys
import uvicorn

from fastapi import FastAPI
from dataclasses import asdict
from starlette.routing import Mount
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from database.database import db
from config.config import conf
from router import app_api, admin_api


app_tags_metadata = [
    {
        'name': 'user',
        'description': '고객정보'
    },
    {
        'name': 'home',
        'description': '홈'
    },
]

admin_tags_metadata = [
    {
        'name': 'user',
        'description': '고객정보'
    },
]


def create_app():
    # APP API http://127.0.0.1:8000/api/v1/_docs
    app = FastAPI(title='DanceMate App API',
                  docs_url='/_docs',
                  openapi_tags=app_tags_metadata)
    app.include_router(app_api.routers)

    # Admin API http://127.0.0.1:8000/admin/api/v1/_docs
    admin_app = FastAPI(title='DanceMate Admin API',
                        docs_url='/_docs',
                        openapi_tags=admin_tags_metadata)
    admin_app.include_router(admin_api.routers)

    app = Starlette(
        routes=[
            Mount('/api/v1', app),
            Mount('/admin/api/v1', admin_app),
        ]
    )

    conf_dict = asdict(conf())
    db.init_app(app, **conf_dict)
    return app


app = create_app()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def on_app_start():
    print(sys.version)


@app.on_event('shutdown')
async def on_app_shutdown():
    print('shutdown')


