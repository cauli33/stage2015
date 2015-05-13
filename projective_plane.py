def is_projective_plane(s):
    r"""
    Test whether the incidence structure s is a projective plane or not

    INPUT:
    - ''s'' -- incidence structure

    OUTPUT:
    True/False bool

    EXAMPLES:
    ::
    sage: p=designs.projective_plane(4)
    sage: is_projective_plane(p)
    True
    ::
    """


    
    m=s.incidence_matrix()
    l=len(m.column(0))
    c=len(m[0])

    if l!=c:
        return False

    p=sum(m[i,0] for i in range(l))
    if p**2-p+1!=l or p<3:
        return false


    else:

        for (i,j,) in [(i,j) for i in range(l) for j in range(l) if i<j]:
            if m[i]*m[j]!=1 or m.column(i)*m.column(j)!=1:
                return False
            if sum(m[x,j] for x in range(l))!=p:
                return False
        
            if j<l-1:
                for k in range(l)[j+1:]:
                    b=1
                    for n in range(l):
                        if m[i,n]+m[j,n]+m[k,n]==3:
                            b*=0
                    if b==1:
                        return True



    return False

        


            

        
