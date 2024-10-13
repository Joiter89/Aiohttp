from aiohttp import web
from models import engine, Session, Ads, Base
import json

from sqlalchemy.exc import IntegrityError

app = web.Application()


async def context_orm(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('STOP')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(context_orm)
app.middlewares.append(session_middleware)


def get_http_error(error_class, description: str):
    return error_class(
        text=json.dumps({"status": "error", "description": description}),
        content_type='application/json'
    )


async def get_ad(ads_id: int, session: Session):
    ad = await session.get(Ads, ads_id)
    if ad is None:
        raise get_http_error(web.HTTPNotFound, 'Ads not found')
    return ad


async def add_ads(ad, session: Session):
    try:
        session.add(ad)
        await session.commit()
    except IntegrityError as er:
        raise get_http_error(web.HTTPConflict, "Ads already exists")
    return ad


class AdsView(web.View):
    @property
    def session(self):
        return self.request['session']

    @property
    def ads_id(self):
        return int(self.request.match_info['ads_id'])

    async def get(self):
        ad = await get_ad(self.ads_id, self.session)
        return web.json_response(
            {
                "id": ad.id,
                "header": ad.header,
                "description": ad.description,
                "creation_time": ad.creation_time.isoformat(),
                "owner": ad.owner
            }
        )

    async def post(self):
        json_validated = await self.request.json()
        ad = Ads(**json_validated)
        ad = await add_ads(ad, self.session)
        return web.json_response(
            {
                "id": ad.id,
            }
        )

    async def patch(self):
        json_validated = await self.request.json()
        ad = await get_ad(self.ads_id, self.session)
        for field, value in json_validated.items():
            setattr(ad, field, value)
            user = await add_ads(ad, self.session)
        return web.json_response({
            'id': ad.id,
        })

    async def delete(self):
        ad = await get_ad(self.ads_id, self.session)
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({
            'status': 'success',
        })


app.add_routes([web.post('/ad', AdsView),
                web.get('/ad/{ads_id:\d+}', AdsView),
                web.patch('/ad/{ads_id:\d+}', AdsView),
                web.delete('/ad/{ads_id:\d+}', AdsView)])

if __name__ == '__main__':
    web.run_app(app)