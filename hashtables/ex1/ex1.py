#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for index in range(len(weights)):
        weight = weights[index]
        hash_table_insert(ht, weight, index)

    for index in range(len(weights)):
        weight = weights[index]
        difference = limit - weight
        otherIndex = hash_table_retrieve(ht, difference)
        if otherIndex is not None:
            return (max(otherIndex, index), min(otherIndex, index))
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
