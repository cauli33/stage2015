def find_hughes_matrix(q):
    M = GL(3,GF(q))
    l = []
    for m in M:
        if is_hughes_matrix(m,q):
            l.append(m)
    return l

def is_hughes_matrix(m,q,verbose=False):
    p= (m**(q**2+q+1)).matrix()
    if not p[0,0]==p[1,1]==p[2,2]!=0 or not p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
        return False
    for i in range(1,q**2+q+1):
        p = (m**i).matrix()
        if p[0,0]==p[1,1]==p[2,2]!=0 and p[0,1]==p[0,2]==p[1,0]==p[1,2]==p[2,0]==p[2,1]==0:
            return False
    return True
            
def HughesProjectivePlane(A, n):
    K = FiniteField(n, 'x')
    relabel = {x:i for i,x in enumerate(K)}
    
    
    


