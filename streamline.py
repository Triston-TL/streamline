import asyncio
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.handler = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path, handler):
        node = self.root
        for part in path.split('/'):
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.handler = handler

    def search(self, path):
        node = self.root
        for part in path.split('/'):
            if part in node.children:
                node = node.children[part]
            else:
                return None
        return node.handler

class Streamline:
    def __init__(self):
        self.routes = {}
        self.trie = Trie()
        self.lock = asyncio.Lock()
        self.cache = {}

    def route(self, path, methods=['GET']):
        def wrapper(func):
            for method in methods:
                self.routes[(method, path)] = func
                self.trie.insert(path, func)
            return func

        return wrapper

    async def handle_request(self, request):
        path = request.path
        method = request.method
        logging.info(f"Received {method} request for path: {path}", extra={"path": path, "method": method})

        response = None
        try:
            async with self.lock:
                handler = self.trie.search(path)
                if handler:
                    response = await handler(request)
                    self.cache[path] = response
                    logging.info(f"Response for {path}: {response}", extra={"path": path, "response": response})
                else:
                    return web.Response(status=404, text="Not Found")

            return web.Response(status=200, text=response if response else "Internal Server Error")
        except Exception as e:
            logging.error(f"Error processing {method} request for {path}: {e}", extra={"error": str(e)})
            return web.Response(status=500, text="Internal Server Error")

    def get(self, path):
        return self.route(path, methods=['GET'])

    def post(self, path):
        return self.route(path, methods=['POST'])

    def put(self, path):
        return self.route(path, methods=['PUT'])

    def delete(self, path):
        return self.route(path, methods=['DELETE'])

    def run(self, host="127.0.0.1", port=5000):
        app = web.Application()
        for route in self.routes:
            app.router.add_route('*', route, self.handle_request)
        web.run_app(app, host=host, port=port)