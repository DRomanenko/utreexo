from tests.test_base import BaseTest


class BigTests(BaseTest):
    def test_many_adds(self):
        for i in range(100):
            for (count, utxo) in enumerate(self.generate_utxos(1000)):
                self.DA.add_one(utxo)
                self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added on {count + 1} stage')
                self.assertEquals(i * 1000 + (count + 1), self.DA.get_size(),
                                  f'Size isn\'t correct on {count + 1} stage')

    def test_many_operations(self):
        for i in range(30000):
            utxo = self.generate_utxo()

            self.DA.add_one(utxo)
            self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added')
            self.assertEquals(1, self.DA.get_size(), f'Size isn\'t correct after add')

            self.DA.delete_one(self.NM.get_proof(utxo))
            self.assertFalse(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t deleted')
            self.assertEquals(0, self.DA.get_size(), f'Size isn\'t correct after delete')

    def test_many_operations_batch(self):
        s = set()
        for i in range(1000):
            utxo = self.generate_utxo()
            if utxo in s:
                continue
            s.add(utxo)

            self.DA.add_one(utxo)
            self.assertTrue(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t added')
            self.assertEquals(len(s), self.DA.get_size(), f'Size isn\'t correct after add')

        l = len(s)
        for i in range(l):
            utxo = s.pop()

            self.DA.delete_one(self.NM.get_proof(utxo))
            self.assertFalse(self.DA.verify(self.NM.get_proof(utxo)), f'Element isn\'t deleted')
            self.assertEquals(len(s), self.DA.get_size(), f'Size isn\'t correct after delete')

    def test_many_removes(self):
        utxos = self.generate_utxos(10000, 24)
        self.DA.add_all(utxos)
        for utxo in utxos:
            proof = self.NM.get_proof(utxo)
            self.assertTrue(self.DA.delete_one(proof), f'Element isn\'t deleted')
            self.assertFalse(self.DA.verify(proof), f'Element isn\'t deleted')
