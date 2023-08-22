from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def fetch_url(url):
    try:
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            return response.json().get("numbers", [])
        else:
            return []
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tasks = [fetch_url(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    merged_numbers = []
    for result in results:
        merged_numbers.extend(result)

    unique_numbers = list(set(merged_numbers))
    sorted_numbers = sorted(unique_numbers)

    return jsonify({"numbers": sorted_numbers})



if __name__ == '__main__':
    app.run(port=8008)
