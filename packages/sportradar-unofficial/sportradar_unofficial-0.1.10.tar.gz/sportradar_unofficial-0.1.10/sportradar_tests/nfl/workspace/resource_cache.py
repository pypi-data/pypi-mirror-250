import unittest
import os

from sportradar.workspace.resource_cache import (
    AbstractCache,
    RedisCache,
    NFLStatsResourceKey,
)


class TestCache(unittest.TestCase):
    def setUp(self):
        self.setup_documents()
        self.setup_environment_variables()

    def setup_documents(self):
        self.document_to_store = {
            "name": "John",
            "documents": [
                {"title": "Doc 1", "content": "Content 1"},
                {"title": "Doc 2", "content": "Content 2"},
            ],
        }

    def setup_environment_variables(self):
        self.redis_host = os.getenv("REDIS_HOST_GG", "localhost")
        self.redis_port = os.getenv("REDIS_PORT_GG", 6379)
        self.redis_pass = os.getenv("REDIS_PASS_GG", "")

        # Let's check if Redis server is available
        try:
            cache = RedisCache(
                host=self.redis_host, port=self.redis_port, password=self.redis_pass
            )
            assert cache is not None
        except Exception as e:
            self.fail(f"Redis server is not available because of this error: {e}")

    def test_abstract_cache(self):
        with self.assertRaises(TypeError):
            AbstractCache()

    def test_nfl_stats_resource_key(self):
        key = NFLStatsResourceKey()
        self.assertEqual(str(key), str(key))

    def test_redis_cache(self):
        key = NFLStatsResourceKey()
        cache = RedisCache(
            host=self.redis_host, port=self.redis_port, password=self.redis_pass
        )
        result = cache.get(resource=key)
        print(result)
        self.assertEqual(result, self.document_to_store)

        cache.add(resource=key, value=self.document_to_store)
        cache.delete(resource=key)

        self.assertFalse(cache.contains(key))


if __name__ == "__main__":
    unittest.main()
