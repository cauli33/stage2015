def find_hughes_matrix(q):
    M = GL(3,GF(q))
    l = []
    for m in M:
        if is_hughes_matrix(m,q):
            l.append(m)
    return l

def is_hughes_matrix(m,q):
    p= (m**(q**2+q+1)).matrix()
    if not p[0,0]==p[1,1]==p[2,2]!=0 or not p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
        return False
    for i in range(1,q**2+q+1):
        p = (m**i).matrix()
        if p[0,0]==p[1,1]==p[2,2]!=0 and p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
            return False
    return True

def inverse(x,F):
    for i in F.list():
        if x*i==1:
            return i

def op(x,y,q):
    if y.is_square():
        return x*y
    else:
        return x**q * y

def normalise(p,K,q):
    if type(p) != list :
        p = list(p)
    for i in range(3):
        if p[2-i] !=  1 and p[2-i] != 0:
            k=inverse(p[2-i],K)
            if k.is_square():
                for j in range(3-i):
                    p[j] *= k
                for j in range(3-i,3):
                    p[j] = K.list()[0] 
                break
            else:
                for j in range(3-i):
                    p[j]= p[j]**q * k**q
                for j in range(3-i,3):
                    p[j] = K.list()[0] 
                break
        if p[2-i] == 1:
            break
    return p
        
        
def HughesPlane(A, n2):
    if not n2.is_square():
        raise EmptySetError("No Hughes plane of non-square order exists.")
    if n2%2 == 0:
        raise EmptySetError("No Hughes plane of even order exists.")
    n = n2.sqrt()
    n4 = n2**2
    K = FiniteField(n2, 'x')
    v = K.list()
# Construct the points (x,y,z) of the projective plane, (x,y,z)=(xk,yk,zk)
    points=[[x,y,z] for x in v for y in v for z in v if [x,y,z] != [0,0,0] if normalise([x,y,z],K,n) == [x,y,z]]
    blcks = []
# Find the first line satisfying x+ay+z=0
    for a in v:
        if a not in FiniteField(n,'y') or a == 1:
            l = []
            for p in points:
                if p[0] + op(a,p[1],n) + p[2] == 0:
                    l.append(vector(p))
# We can now deduce the other lines from these ones
            blcks.append(l)
            for i in range(n2 + n + 1):
                l = [A*i for i in l]
                blcks.append(l)
    for b in blcks:
        for p in range(len(b)):
            b[p]=normalise(b[p],K,n)
    return blcks
                
    
