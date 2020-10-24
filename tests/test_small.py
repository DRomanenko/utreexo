from dynamic_accumulator.dynamic_accumulator import Neighbour
from tests.test_base import BaseTest


class SmallTests(BaseTest):
    def test_adds_by_one(self):
        for (count, utxo) in enumerate(self.generate_utxos(10)):
            self.DA.add_one(utxo)
            self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added on {count + 1} stage')
            self.assertEquals(count + 1, self.DA.get_size(), f'Size isn\'t correct on {count + 1} stage')

    def test_batch_adds(self):
        for i in range(3):
            utxos = self.generate_utxos(3)
            self.DA.add_all(utxos)
            for (count, utxo) in enumerate(utxos):
                self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)),
                                f'Element isn\'t added on {i + 1}/{count + 1} stage')
                self.assertEquals(3 * (i + 1), self.DA.get_size(), f'Size isn\'t correct on {i + 1}/{count + 1} stage')

    def test_add_remove(self):
        utxo = self.generate_utxo()

        self.DA.add_one(utxo)
        self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added')
        self.assertEquals(1, self.DA.get_size(), f'Size isn\'t correct after add')

        self.DA.delete_one(self.NM.get_proof(utxo))
        self.assertFalse(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t deleted')
        self.assertEquals(0, self.DA.get_size(), f'Size isn\'t correct after delete')

    def test_binary_roots(self):
        utxos_count = 23
        self.DA.add_all(self.generate_utxos(utxos_count))
        roots = self.DA.roots()
        self.assertEquals(5, len(roots))
        for i in range(len(roots) - 1, -1):
            self.assertTrue(roots[i].is_empty() if utxos_count % 2 == 0 else not roots[i].is_empty())

    def test_remove_not_added(self):
        utxo1 = self.generate_utxo()
        utxo2 = self.generate_utxo()

        self.DA.add_one(utxo1)
        self.assertTrue(self.DA.verify(self.NM.get_proof(utxo1)), f'Element isn\'t added')
        self.assertEquals(1, self.DA.get_size(), f'Size isn\'t correct after add')

        self.DA.delete_one(self.NM.get_proof(utxo2))
        self.assertTrue(self.DA.verify(self.NM.get_proof(utxo1)), f'Element is deleted')
        self.assertEquals(1, self.DA.get_size(), f'Size isn\'t correct after delete')

    def test_remove_with_fake_proof(self):
        utxos = self.generate_utxos(10)
        self.DA.add_all(utxos)
        proof = self.NM.get_proof(utxos[3])
        proof.set_element(utxos[7])
        self.assertFalse(self.DA.delete_one(proof), "Element with fake proof was deleted")

    def test_remove_with_corrupted_proof(self):
        utxos = self.generate_utxos(16)
        self.DA.add_all(utxos)
        proof = self.NM.get_proof(utxos[8])
        proof.set_neighbour(1, Neighbour(utxos[1], False))
        self.assertFalse(self.DA.delete_one(proof), "Element with corrupted proof was deleted")

    def test_remove_with_shorter_proof(self):
        utxos = self.generate_utxos(16)
        self.DA.add_all(utxos)
        proof = self.NM.get_proof(utxos[8])
        proof.get_neighbours().pop()
        self.assertFalse(self.DA.delete_one(proof), "Element with shorter proof was deleted")

    def test_remove_with_longer_proof(self):
        utxos = self.generate_utxos(16)
        self.DA.add_all(utxos)
        proof = self.NM.get_proof(utxos[8])
        proof.get_neighbours().append(Neighbour(utxos[4], True))
        self.assertFalse(self.DA.delete_one(proof), "Element with longer proof was deleted")

    def test_remove_two_times(self):
        utxo = self.generate_utxo()

        self.DA.add_one(utxo)
        self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added')
        self.assertEquals(1, self.DA.get_size(), f'Size isn\'t correct after add')

        self.assertTrue(self.DA.delete_one(self.NM.get_proof(utxo)), f'Element isn\'t deleted')
        self.assertEquals(0, self.DA.get_size(), f'Size isn\'t correct after delete')

        self.assertFalse(self.DA.delete_one(self.NM.get_proof(utxo)), f'Element isn\'t deleted')
        self.assertEquals(0, self.DA.get_size(), f'Size isn\'t correct after delete')
