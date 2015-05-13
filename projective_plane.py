def is_projective_plane(s):
    r"""
    Test whether the incidence structure s is a projective plane or not

    INPUT:
    
    - ''s'' -- incidence structure

    OUTPUT:
    
    True/False bool

    EXAMPLES::
    
    sage: p=designs.projective_plane(4)
    sage: is_projective_plane(p)
    True

    sage: p=designs.projective_plane(2)
    sage: is_projective_plane(p)
    True
    sage: p._blocks
    [[0, 1, 6], [0, 2, 4], [0, 3, 5], [1, 2, 5], [1, 3, 4], [2, 3, 6], [4, 5, 6]]
    sage: a=[[0, 1, 5], [0, 2, 4], [0, 3, 5], [1, 2, 5], [1, 3, 4], [2, 3, 6], [4, 5, 6]]
    sage: s=IncidenceStructure(a)
    sage: is_projective_plane(s)
    False

    ::
    """    
    m=s.incidence_matrix()
    l=m.nrows()
    c=m.ncols()
    v=False
    if l!=c:
        return False
    p=sum(m[i,0] for i in range(l))
    if p**2-p+1!=l or p<3:
        return False
    else:
        for j in range(l):
            for i in range(j):
                if m[i]*m[j]!=1 or m.column(i)*m.column(j)!=1:
                    return False
                if sum(m[x,j] for x in range(l))!=p:
                    return False
        for j in range(l-1):
            for i in range(j):
                for k in range(l)[j+1:]:
                    b=1
                    for n in range(l):
                        if m[i,n]+m[j,n]+m[k,n]==3:
                            b*=0
                    if b==1:
                        return True
    return False



    


            

        
