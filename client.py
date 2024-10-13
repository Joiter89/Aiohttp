import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # response = await session.post(
        #     'http://127.0.0.1:8080/ad',
        #     json={'header': 'header',
        #           'description': 'Hi guys',
        #           'owner': 'Svetlana'},
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)
        #
        # response = await session.get(
        #     'http://127.0.0.1:8080/ad/1',
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)

        # response = await session.patch(
        #     'http://127.0.0.1:8080/ad/1',
        #     json={"owner": "owner_new"}
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)
        #
        # response = await session.get(
        #     'http://127.0.0.1:8080/ad/1',
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)

        # response = await session.delete(
        #     'http://127.0.0.1:8080/ad/1',
        #     json={"owner": "owner_new"}
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)
        #
        response = await session.get(
            'http://127.0.0.1:8080/ad/2',
        )
        json_data = await response.json()
        print(response.status)
        print(json_data)


if __name__ == '__main__':
    asyncio.run(main())