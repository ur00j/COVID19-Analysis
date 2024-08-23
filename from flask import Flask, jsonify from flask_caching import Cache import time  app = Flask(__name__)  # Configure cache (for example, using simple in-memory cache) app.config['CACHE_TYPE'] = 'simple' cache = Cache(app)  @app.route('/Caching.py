from flask import Flask, jsonify
from flask_caching import Cache
import time

app = Flask(__name__)

# Configure cache (for example, using simple in-memory cache)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.route('/data', methods=['GET'])
@cache.cached(timeout=60, key_prefix='data_endpoint')
def get_data():
    # Simulate a slow data retrieval
    time.sleep(2)  # Simulate delay
    data = {
        'message': 'This is the data response.',
        'timestamp': time.time()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

app.config['CACHE_TYPE'] = 'simple'

@cache.cached(timeout=60, key_prefix='data_endpoint')

from flask_caching import RedisCache

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    cache.clear()
    return jsonify({'message': 'Cache cleared!'})
@app.after_request
def log_cache_status(response):
    cache_info = {
        'cache_type': cache.cache_type,
        'cache_hits': cache._cache.stats['hits'],
        'cache_misses': cache._cache.stats['misses'],
    }
    app.logger.info(f"Cache Info: {cache_info}")
    return response

