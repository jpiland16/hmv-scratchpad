import numpy as np
print("Let's calculate q1*q0:")

def ham_product(q1, q2):
    """ Returns Hamilton product q1q2 for two quaternions in (wxyz) form
    https://en.wikipedia.org/wiki/Quaternion#Hamilton_product
    """
    prod = np.empty(4)
    prod[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
    prod[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
    prod[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
    prod[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
    return prod

q0 = np.empty(4)
q0[0] = input("q0 | w: ")
q0[1] = input("q0 | x: ")
q0[2] = input("q0 | y: ")
q0[3] = input("q0 | z: ")
print("q0={0}".format(q0))

q1 = np.empty(4)
q1[0] = input("q1 | w: ")
q1[1] = input("q1 | x: ")
q1[2] = input("q1 | y: ")
q1[3] = input("q1 | z: ")
print("q1={0}".format(q0))

print("q1*q0=(wxyz)={0}".format(ham_product(q1,q0)))