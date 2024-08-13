# invoker.py
import requests
import redis
import json
from cachetools import TTLCache
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Local cache with TTL of 10 seconds and a max of 3 keys
local_cache = TTLCache(maxsize=3, ttl=10)

# Redis setup (assuming Redis is running on the default port)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

GENERATOR_URL = 'http://generator:5001/generate'


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    viewer_id = data.get('viewerid')

    # Check local cache
    if viewer_id in local_cache:
        return jsonify(local_cache[viewer_id])

    # Check Redis cache
    redis_cached = redis_client.get(viewer_id)
    if redis_cached:
        result = json.loads(redis_cached)
        local_cache[viewer_id] = result
        return jsonify(result)

    # Run cascade if cache miss
    result = runcascade(viewer_id)

    # Save result in caches
    local_cache[viewer_id] = result
    redis_client.set(viewer_id, json.dumps(result))

    return jsonify(result)


def runcascade(viewer_id):
    models = ['model1', 'model2', 'model3', 'model4', 'model5']

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(make_request, model, viewer_id) for model in models]

    results = [future.result() for future in futures]
    merged_result = {"recommendations": results}
    return merged_result


def make_request(model_name, viewer_id):
    response = requests.post(GENERATOR_URL, json={"model_name": model_name, "viewerid": viewer_id})
    return response.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
