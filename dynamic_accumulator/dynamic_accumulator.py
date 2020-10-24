from utils.hash_utils import sha256_encode


class Hash:
    def __init__(self, b: bytes = None):
        if b:
            self.__data = sha256_encode(b)
        else:
            self.__data = b''

    def is_empty(self):
        return self.__data == b''

    def get_data(self):
        return self.__data


class Neighbour:
    def __init__(self, value: Hash, is_right: bool):
        self.__value = value
        self.__is_right = is_right

    def get_value(self) -> Hash:
        return self.__value

    def is_right(self) -> [Hash]:
        return self.__is_right


class Proof:
    def __init__(self, element: Hash, neighbours: [Neighbour]):
        self.__element = element
        self.__neighbours = neighbours

    def get_element(self) -> Hash:
        return self.__element

    def set_element(self, element: Hash):
        self.__element = element

    def get_neighbours(self) -> [Neighbour]:
        return self.__neighbours

    def set_neighbour(self, i: int, neighbour: Neighbour):
        self.__neighbours[i] = neighbour

    def get_length(self):
        return len(self.__neighbours)


class NeighboursMap:
    def __init__(self):
        self.__data = {}

    def get_data(self):
        return self.__data.copy()

    def add_neighbour(self, element: Hash, neighbour: Neighbour):
        self.__data[element.get_data()] = neighbour

    def delete_neighbour(self, element: Hash):
        if element.get_data() in self.__data.keys():
            self.__data.pop(element.get_data())

    def get_neighbour(self, element: Hash) -> Neighbour:
        return self.__data[element.get_data()]

    def get_proof(self, element: Hash):
        neighbours: [Neighbour] = []
        current_element = element
        while current_element.get_data() in self.__data.keys():
            neighbour = self.__data[current_element.get_data()]
            neighbours.append(neighbour)
            current_element = DynamicAccumulator.parent_with_neighbour(current_element, neighbour)

        return Proof(element, neighbours)


class DynamicAccumulator:
    def __init__(self, initial_capacity: int = 1, neighbours_map: NeighboursMap = None):
        if initial_capacity < 1:
            initial_capacity = 1
        self.__merkle_roots: [Hash] = [Hash()] * initial_capacity
        self.__size = 0

        # Inject NeighboursMap for building proofs in tests
        self.__neighbours_map = neighbours_map

    def get_size(self):
        return self.__size

    def roots(self):
        return self.__merkle_roots.copy()

    def add_all(self, elements: [Hash]):
        self.__size += len(elements)
        new_merkle_trees: [[Hash]] = self.__create_new_merkle_trees()
        new_merkle_trees[0].extend(elements)
        self.__push_roots(new_merkle_trees)

    def add_one(self, element: Hash):
        self.add_all([element])

    def verify(self, proof: Proof) -> bool:
        root_number = proof.get_length()
        if root_number >= len(self.__merkle_roots):
            return False

        true_root = self.__merkle_roots[root_number]
        if true_root.is_empty():
            return False

        current_element = proof.get_element()
        for neighbour in proof.get_neighbours():
            current_element = DynamicAccumulator.parent_with_neighbour(current_element, neighbour)

        return current_element.get_data() == true_root.get_data()

    def delete_one(self, proof: Proof) -> bool:
        if len(self.__merkle_roots) <= proof.get_length() or self.__merkle_roots[proof.get_length()].is_empty():
            return False

        new_merkle_trees: [[Hash]] = self.__create_new_merkle_trees()
        current_height = 0
        current_element = proof.get_element()

        for neighbour in proof.get_neighbours():
            new_merkle_trees[current_height].append(neighbour.get_value())
            if self.__neighbours_map:
                self.__neighbours_map.delete_neighbour(neighbour.get_value())
            current_element = DynamicAccumulator.parent_with_neighbour(current_element, neighbour)
            current_height += 1

        if current_element.get_data() == self.__merkle_roots[proof.get_length()].get_data():
            new_merkle_trees[current_height].clear()
            self.__push_roots(new_merkle_trees)
            self.__size -= 1
            return True

        return False

    def __push_roots(self, new_merkle_trees: [[Hash]]):
        i = 0
        while i < len(new_merkle_trees):
            while len(new_merkle_trees[i]) > 1:
                left = new_merkle_trees[i].pop()
                right = new_merkle_trees[i].pop()
                parent = self.parent(left, right)

                if i == len(new_merkle_trees) - 1:
                    new_merkle_trees.append([])

                new_merkle_trees[i + 1].append(parent)

                # Remember neighbours if NeighboursMap for building proof in tests
                if self.__neighbours_map:
                    self.__neighbours_map.add_neighbour(left, Neighbour(right, True))
                    self.__neighbours_map.add_neighbour(right, Neighbour(left, False))

            i += 1

        for (index, root) in enumerate(new_merkle_trees):
            if index == len(self.__merkle_roots):
                self.__merkle_roots.append(Hash())

            if len(root) == 0:
                self.__merkle_roots[index] = Hash()
            else:
                self.__merkle_roots[index] = root[0]

    def __create_new_merkle_trees(self) -> [[Hash]]:
        new_merkle_trees: [[Hash]] = []
        for root in self.__merkle_roots:
            new_merkle_trees.append([])
            if not root.is_empty():
                new_merkle_trees[-1].append(root)
        return new_merkle_trees

    @staticmethod
    def parent(left: Hash, right: Hash) -> Hash:
        if left.is_empty() and right.is_empty():
            return Hash()
        return Hash(b''.join([b'\x01', left.get_data(), b'\x02', right.get_data()]))

    @staticmethod
    def parent_with_neighbour(element: Hash, neighbour: Neighbour) -> Hash:
        if neighbour.is_right():
            return DynamicAccumulator.parent(element, neighbour.get_value())
        else:
            return DynamicAccumulator.parent(neighbour.get_value(), element)
