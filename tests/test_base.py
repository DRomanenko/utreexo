import random
import string
import time
from unittest import TestCase

from dynamic_accumulator.dynamic_accumulator import DynamicAccumulator, NeighboursMap, Hash
from utils.hash_utils import base64_decode


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.NM = NeighboursMap()
        self.DA = DynamicAccumulator(neighbours_map=self.NM)

    def n_random_operations_perf(self, da: DynamicAccumulator, nm: NeighboursMap, n: int) -> float:
        s = set()
        not_algorithm_time = 0.0

        start_time = time.time()
        for i in range(n):
            start_iteration_time = time.time()
            op = random.randrange(0, 3)
            if op == 0:
                utxo = self.generate_utxo()
                if utxo in s:
                    not_algorithm_time += (time.time() - start_iteration_time)
                    continue
                s.add(utxo)
                da.add_one(utxo)
            elif op == 1:
                if len(s) == 0:
                    not_algorithm_time += (time.time() - start_iteration_time)
                    continue

                start_generating_proof = time.time()
                proof = nm.get_proof(s.pop())
                not_algorithm_time += (time.time() - start_generating_proof)

                da.delete_one(proof)
            else:
                utxo = self.generate_utxo()

                start_generating_proof = time.time()
                proof = nm.get_proof(utxo)
                not_algorithm_time += (time.time() - start_generating_proof)

                self.assertEquals(utxo in s, da.verify(proof))

        return time.time() - start_time - not_algorithm_time

    def n_random_operations(self, n: int):
        self.n_random_operations_perf(self.DA, self.NM, n)

    def n_adds_and_removes_perf(self, da: DynamicAccumulator, nm: NeighboursMap, n: int) -> float:
        s = set()
        not_algorithm_time = 0.0

        start_time = time.time()
        for i in range(n // 2):
            start_iteration_time = time.time()
            utxo = self.generate_utxo()
            if utxo in s:
                not_algorithm_time += (time.time() - start_iteration_time)
                continue
            s.add(utxo)
            da.add_one(utxo)

        for i in range(n // 2):
            start_iteration_time = time.time()
            if len(s) == 0:
                not_algorithm_time += (time.time() - start_iteration_time)
                continue

            start_generating_proof = time.time()
            proof = nm.get_proof(s.pop())
            not_algorithm_time += (time.time() - start_generating_proof)

            da.delete_one(proof)

        return time.time() - start_time - not_algorithm_time

    @staticmethod
    def generate_utxos(count: int, size: int = 4) -> [Hash]:
        return [Hash(base64_decode(
            str(''.join(random.choice(string.ascii_letters)
                        for _ in range(size)))))
            for _ in range(count)]

    @staticmethod
    def generate_utxo() -> Hash:
        return BaseTest.generate_utxos(1)[0]
