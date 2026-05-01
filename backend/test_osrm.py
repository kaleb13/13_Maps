import asyncio
import httpx

async def main():
    coords = [{"latitude": 9.0 + i*0.001, "longitude": 38.7 + i*0.001} for i in range(150)]
    
    # test route
    coords_str = ";".join(f"{loc['longitude']},{loc['latitude']}" for loc in coords)
    url = f"http://router.project-osrm.org/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code != 200:
            print(resp.text)
        else:
            print("Success")

asyncio.run(main())
