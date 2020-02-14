import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof, iterations):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    # start = timer()
    # print("Searching for next proof")
    proof = 0

    last_proof = f"{last_proof}"
    lastHex = hashlib.sha256(last_proof.encode()).hexdigest()
    
    for i in range(iterations):
        proof = str(int(random.random() * 100000000))
        if valid_proof(lastHex, proof):
            print(f"found proof for {last_proof} - {proof}")
            return proof

    # print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return None


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    lastSix = last_hash[-6:]
    newHash = hashlib.sha256(proof.encode()).hexdigest()
    return lastSix == newHash[:6]


def getLastProof():
    r = requests.get(url=node + "/last_proof")
    # Handle non-json response
    data = {}
    try:
        data = r.json()
    except ValueError:
        print("Error:  Non-json response (via last_proof)")
        print("Response returned:")
        print(r)
        return None

    return data.get("proof", None)


def submitProof(new_proof):
    # When found, POST it to the server {"proof": new_proof, "id": id}
    post_data = {"proof": new_proof,
                 "id": id}

    r = requests.post(url=node + "/mine", json=post_data)
    try:
        data = r.json()
        status = data.get("message", None)
    except ValueError:
        print("Error:  Non-json response (via submission)")
        print("Response returned:")
        print(r)
        status = str(r)
    return status

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    # Load ID
    if len(sys.argv) > 2:
        id = sys.argv[2]
    else:
        f = open("my_id.txt", "r")
        id = f.read()
        f.close()

    print("ID is", id)

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server

        start = timer()
        print("Searching for next proof")

        new_proof = None
        while new_proof is None:
            oldProof = getLastProof()
            if oldProof is None:
                break
            print(f"old proof {oldProof}")

            new_proof = proof_of_work(oldProof, 1000000)
        if new_proof is None:
            print("none proof")
            break

        print("Proof found: " + str(new_proof) + " in " + str(timer() - start))

        success = submitProof(new_proof)

        if success == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(success)
