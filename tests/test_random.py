from tests.test_base import BaseTest


class RandomTests(BaseTest):
    def test_100_random_operations(self):
        self.n_random_operations(100)

    def test_1000_random_operations(self):
        self.n_random_operations(1000)

    def test_10000_random_operations(self):
        self.n_random_operations(10000)

    def test_50000_random_operations(self):
        self.n_random_operations(50000)



