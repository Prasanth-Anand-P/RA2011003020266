from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def url_fetch(url):
    try:
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            return response.json().get("numbers", [])
        else:
            return []
    except Exception as e:
        return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tasks = [url_fetch(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    merge_num = []
    for i in results:
        merge_num.extend(i)

    uni_num = list(set(merge_num))
    sort_num = sorted(uni_num)

    return jsonify({"numbers": sort_num})



if __name__ == '__main__':
    app.run(port=8008)
