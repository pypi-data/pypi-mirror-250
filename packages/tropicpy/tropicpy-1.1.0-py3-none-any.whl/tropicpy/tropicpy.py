"""


"""
from attacks.kotov_ushakov_simple import *
from attacks.kotov_ushakov import *
from protocols.grigorie_shpilrain_2019 import *
from attacks.rudy_monico import *
from attacks.isaac_kahrobaei import *
from protocols.grigorie_shpilrain_2014 import *


def tropical_demo():
    print("In tropical algebra we have:")

    print("0 = " + str(tropical_0))
    print("1 = " + str(tropical_1))

    print("0(3x3) \n=\n" + str(tropical_matrix_0(3)))
    print("1(3x3) \n=\n" + str(tropical_matrix_1(3)))

    print("Examples of tropical operations:")

    a = generate_random_tropical_value(-100, 100)
    b = generate_random_tropical_value(-100, 100)

    print("a) addition:")
    print("(" + str(a) + ")+(" + str(b) + ")=" + str(a + b))

    print("b) multiplication:")
    print("(" + str(a) + ")+(" + str(b) + ")=" + str(a * b))

    print("Examples of operations on tropical matrices:")

    e = generate_random_tropical_matrix(3, -100, 100)
    f = generate_random_tropical_matrix(3, -100, 100)

    print("a) addition:")
    print(e)
    print("+")
    print(f)
    print("=")
    print(e + f)

    print("b) multiplication:")

    print(e)
    print("*")
    print(f)
    print("=")
    print(e * f)

    print("c) power")
    print(e)
    print("** 4\n=")
    print(e ** 4)

    print("d) adjoint multiplication:")

    print(e)
    print("@")
    print(f)
    print("=")
    print(e @ f)

    print("e) adjoint power")
    print(e)
    print("^3\n=")
    print(e ^ 3)


def protocol_demo(protocol):
    print("Example of " + protocol.__name__ + " protocol:")

    n = 3
    A = generate_random_tropical_matrix(n, -10 ** 10, 10 ** 10)
    B = generate_random_tropical_matrix(n, -10 ** 10, 10 ** 10)

    print("Parameters:")
    print("A = \n" + str(A))
    print("B = \n" + str(B))

    Alice = None
    Bob = None

    if protocol == GrigorieShpilrain2014:
        g = random.randint(1, 10)
        print("g = " + str(g))

        Alice = protocol(A, B, g, -1000, 1000)
        Bob = protocol(A, B, g, -1000, 1000)

        print("n = " + str(Alice.n))
    elif protocol == GrigorieShpilrain2019:
        Alice = protocol(A, B)
        Bob = protocol(A, B)

        print("k = " + str(Alice.k))

    U = Alice.send_message()
    V = Bob.send_message()

    print("Alice's message: \n" + str(U))
    print("Bob's message: \n" + str(V))

    Alice.set_Key(V)
    Bob.set_Key(U)

    if Alice.get_Key() == Bob.get_Key():
        print("Alice and Bob share a secret!")
    else:
        print("Something went wrong!")


def attack_demo(protocol, attack):
    print("Example of " + attack.__name__ + " attack:")

    n = 3

    A = generate_random_tropical_matrix(n, -10 ** 10, 10 ** 10)
    B = generate_random_tropical_matrix(n, -10 ** 10, 10 ** 10)

    print("Parameters:")
    print("A = \n" + str(A))
    print("B = \n" + str(B))

    Alice = None
    Bob = None

    if protocol == GrigorieShpilrain2014:
        g = random.randint(1, 10)
        print("g = " + str(g))

        Alice = protocol(A, B, g, -1000, 1000)
        Bob = protocol(A, B, g, -1000, 1000)

        print("n = " + str(Alice.n))
    elif protocol == GrigorieShpilrain2019:
        Alice = protocol(A, B)
        Bob = protocol(A, B)

        print("k = " + str(Alice.k))

    U = Alice.send_message()
    V = Bob.send_message()

    print("U:\n" + str(U))
    print("V:\n" + str(V))

    Alice.set_Key(V)

    attack_K = None

    if protocol == GrigorieShpilrain2014:
        if attack == kotov_ushakov_simple:
            attack_K = attack(A, B, g, U, V)
        elif attack == kotov_ushakov:
            attack_K = attack(A, B, g, U, V, -1000)
    elif protocol == GrigorieShpilrain2019:
        attack_K = attack(A, B, U, V)

    if Alice.check_Key(attack_K):
        print("Key was found!")
        print("K = \n" + str(attack_K))
    else:
        print("Keys don't match..")
        print("Protocol key:\n" + str(Alice.get_Key()))
        print("Attack key:\n" + str(attack_K))


def tropicpy_demo():
    protocol = None
    attack = None

    print("What do you want to see?")
    print("1. Tropical algebra examples")
    print("2. Grigorie-Shpilrain (2014) protocol")
    print("3. Grigorie-Shpilrain (2019) protocol")

    ans1 = input()

    try:
        ans1 = int(ans1)

        if ans1 == 1:
            tropical_demo()
        elif ans1 == 2:
            protocol = GrigorieShpilrain2014

            print("What attack do you want to see?")
            print("1. Kotov-Ushakov Simple")
            print("2. Kotov-Ushakov")
            print("3. None, just the protocol")

            ans2 = input()

            try:
                ans2 = int(ans2)

                if ans2 == 1:
                    attack = kotov_ushakov_simple
                elif ans2 == 2:
                    attack = kotov_ushakov
                else:
                    attack = None
            except:
                print("Not a number.")

        elif ans1 == 3:
            protocol = GrigorieShpilrain2019

            print("What attack do you want to see?")
            print("1. Rudy-Monico")
            print("2. Isaac-Kahrobaei")
            print("3. None, just the protocol")

            ans3 = input()
            try:
                ans3 = int(ans3)

                if ans3 == 1:
                    attack = rudy_monico
                elif ans3 == 2:
                    attack = isaac_kahrobaei
                else:
                    attack = None
            except:
                print("Not a number.")

        else:
            print("Nothing to show.")
            return 0
    except:
        print("Not a number.")

    if attack is not None and protocol is not None:
        attack_demo(protocol, attack)
    elif protocol is not None:
        protocol_demo(protocol)


if __name__ == "__main__":
    tropicpy_demo()
