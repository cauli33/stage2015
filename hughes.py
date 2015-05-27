from sage.categories.sets_cat import EmptySetError

def random_q3_minus_one_matrix(K):
    r"""
    Return a companion matrix in `GL(3, K)` whose multiplicative order is `q^3 - 1`.

    EXAMPLES::

        sage: m = random_q3_minus_one_matrix(GF(3))
        sage: m.multiplicative_order() == 3**3 - 1
        True

        sage: m = random_q3_minus_one_matrix(GF(4,'a'))
        sage: m.multiplicative_order() == 4**3 - 1
        True

        sage: m = random_q3_minus_one_matrix(GF(5))
        sage: m.multiplicative_order() == 5**3 - 1
        True

        sage: m = random_q3_minus_one_matrix(GF(9,'a'))
        sage: m.multiplicative_order() == 9**3 - 1
        True
    """
    q = K.cardinality()
    M = MatrixSpace(K, 3)

    if q.is_prime():
        from sage.rings.finite_rings.conway_polynomials import conway_polynomial
        try:
            a,b,c,_ = conway_polynomial(q, 3)
        except RuntimeError:  # the polynomial is not in the database
            pass
        else:
            return M([0,0,-a,1,0,-b,0,1,-c])

    while True:
        a = K._random_nonzero_element()
        b = K.random_element()
        c = K.random_element()
        m = M([0,0,-a,1,0,-b,0,1,-c])
        if m.multiplicative_order() == q**3 - 1:
            return m

def find_hughes_matrix(q):
    r"""
    Return the generator of matrix that have Hughes property.

    INPUT:
    - ``q`` (integer) - the dimension such that generated matrix are in GL(3,GF(q))

    EXAMPLES::

        sage: G=find_hughes_matrix(3)
        sage: G.next()
        [0 2 0]
        [0 0 2]
        [1 2 0]
        sage: M = G.next()
        sage: M
        [0 2 0]
        [0 0 2]
        [2 2 0]
        sage: M** (3**2 + 3 + 1)
        [2 0 0]
        [0 2 0]
        [0 0 2]

    """
    M = GL(3,GF(q))
    for m in M:
        o = gap.Order(m._gap_())
        if o >= q**2 + q + 1:
            if is_hughes_matrix(m,q,o):
                yield m

def is_hughes_matrix(m,q,o):
    r"""
    Check whether the matrix has the Hughes property.
    
    INPUT:

    - ``m`` - matrix in GL(3,GF(q))
    
    - ``q`` (integer)

    - ``o`` (integer) - m order

    EXAMPLES::

        sage: G=find_hughes_matrix(3)
        sage: M=G.next()
        sage: o=gap.Order(M._gap_())
        sage: is_hughes_matrix(M,3,o)
        True
        sage: M** (3**2 + 3 + 1)
        [1 0 0]
        [0 1 0]
        [0 0 1]

        sage: M=GL(3,GF(3))[10]
        sage: o=gap.Order(M._gap_())
        sage: is_hughes_matrix(M,3,o)
        False
        sage: M ** (3**2 + 3 + 1)
        [0 2 1]
        [2 1 2]
        [2 0 1]

    """
    p= m.matrix()**(q**2 + q + 1)
    if not p[0,0]==p[1,1]==p[2,2]!=0 or not p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
        return False
    for i in divisors(int(o)):
        if i < q**2 + q + 1:
            p = (m**i).matrix()
            if p[0,0]==p[1,1]==p[2,2]!=0 and p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
                return False
    return True

def normalize(p,K,q):
    r"""
    Return the normalized form of point (x,y,z).

    For all integer k non-zero, (x,y,z)k refers to the same point.

    For the normalized form, the last non-zero coordinate must be 1.

    INPUT:
    
    - ``p`` - point with the coordinates (x,y,z) (a list, a vector, a tuple...)

    - ``K```- a finite field (coordinates x,y,z are elements of K)

    - ``q`` - cardinality of K

    OUTPUT:
    List of the coordinates from the normalized form of p

    EXAMPLE::

        sage: K=FiniteField(9,'x')
        sage: p=(K('x'),K('x+1'),K('x'))
        sage: normalise(p,K,9)
        [1, x, 1]
        sage: q=vector((K('x'),K('x'),K('x')))
        sage: normalise(q,K,9)
        [1, 1, 1]
        sage: s=(K('2*x+2'), K(0), K(0))
        sage: normalise(s,K,9)
        [1, 0, 0]
        sage: t=[K('2*x'),K(1),K(0)]
        sage: normalise(t,K,9)
        [2*x, 1, 0]

    """
    if type(p) != list :
        p = list(p)
    for i in range(3):
        if p[2-i] == 1:
            break
        elif p[2-i] != 0:
            k=~p[2-i]
            if k.is_square():
                for j in range(3-i):
                    p[j] *= k
                for j in range(3-i,3):
                    p[j] = K(0) 
                break
            else:
                for j in range(3-i):
                    p[j]= p[j]**q * k**q
                for j in range(3-i,3):
                    p[j] = K(0) 
                break
    return p
        
        
def HughesPlane(n2):
    r"""
    Return Hughes projective plane of order ``n2``.
    
    INPUT:

    - ``n2`` -- an integer which must be an odd square

    EXAMPLES::
    
        sage: HughesPlane(9)
        Incidence structure with 91 points and 91 blocks
        sage: HughesPlane(9).is_projective_plane()
        True

        sage: HughesPlane(5)
        Traceback (most recent call last):
        ...
        EmptySetError: No Hughes plane of non-square order exists.

        sage: HughesPlane(16)
        Traceback (most recent call last):
        ...
        EmptySetError: No Hughes plane of even order exists.

    """
    if not n2.is_square():
        raise EmptySetError("No Hughes plane of non-square order exists.")
    if n2%2 == 0:
        raise EmptySetError("No Hughes plane of even order exists.")
    n = n2.sqrt()
    A = find_hughes_matrix(n).next()
    K = FiniteField(n2, 'x')
    F = FiniteField(n, 'y')
    v = K.list()
# Construct the points (x,y,z) of the projective plane, (x,y,z)=(xk,yk,zk)
    points=[[x,y,K(1)] for x in v for y in v]+[[x,K(1),K(0)] for x in v]+[[K(1),K(0),K(0)]]
    relabel={tuple(p):i for i,p in enumerate(points)}
    blcks = []
# Find the first line satisfying x+ay+z=0
    for a in v:
        if a not in F or a == 1:
            l=[]
            l.append(vector((-a,K(1),K(0))))
            for x in v:
                if ((~a)*(-x-K(1))).is_square():
                    l.append(vector((x,(~a)*(-x-K(1)),K(1))))
                else:
                    l.append(vector((x,(~a) **n * (-x-K(1)),K(1))))
# We can now deduce the other lines from these ones
            blcks.append(l)
            for i in range(n2 + n):
                l = [A*j for j in l]
                blcks.append(l)
    for b in blcks:
        for p in range(len(b)):
            b[p]=relabel[tuple(normalize(b[p],K,n))]
    return IncidenceStructure(n2**2+n2+1, blcks, name="Hughes projective plane of order %d"%n2)
