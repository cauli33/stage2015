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
    M = GL(3,GF(q))
    for m in M:
        o = gap.Order(m._gap_())
        if o >= q**2 + q + 1:
            if is_hughes_matrix(m,q,o):
                yield m

def is_hughes_matrix(m,q,o):
    p= m.matrix()**(q**2 + q + 1)
    if not p[0,0]==p[1,1]==p[2,2]!=0 or not p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
        return False
    for i in divisors(int(o)):
        if i < q**2 + q + 1:
            p = (m**i).matrix()
            if p[0,0]==p[1,1]==p[2,2]!=0 and p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
                return False
    return True

def op(x,y,q):
    if y.is_square():
        return x*y
    else:
        return x**q * y

def normalise(p,K,q):
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
    Return the Hughes projective plane of order ``n2``.
    
    INPUT:

    - ``n2`` -- an integer which must be an odd square

    EXAMPLES::



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
                if (~a*(-x-K(1))).is_square():
                    l.append(vector((x,~a*(-x-K(1)),K(1))))
                else:
                    l.append(vector((x,~a **n * (-x-K(1)),K(1))))
           # l = []
           # for p in points:
           #     if p[0] + op(a,p[1],n) + p[2] == 0:
           #         l.append(vector(p))
# We can now deduce the other lines from these ones
            blcks.append(l)
            for i in range(n2 + n):
                l = [A*j for j in l]
                blcks.append(l)
    for b in blcks:
        for p in range(len(b)):
            b[p]=relabel[tuple(normalise(b[p],K,n))]
    return IncidenceStructure(n2**2+n2+1, blcks, name="Hughes projective plane of order %d"%n2)


def classify(MH,n2):
    S=([])
    for i in range(10):
        c=HughesPlane(MH[i],n2).canonical_label()
        if c not in S:
            S.append(c)
    return S
    
#P.relabel(P.canonical_label())
#récupérer les matrices qui sont isomorphes
