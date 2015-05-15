def is_projective_plane(s,verbose=False):
    r"""
    Test whether the incidence structure s is a projective plane or not

    INPUT:
    
    - ''s'' -- incidence structure
    
    - ``verbose`` - whether to print additional information

    OUTPUT:
    
    True/False bool

    EXAMPLES::
    
    sage: p=designs.projective_plane(4)
    sage: is_projective_plane(p)
    True
    sage: is_projective_plane(p,verbose=True)
    True


    sage: p=designs.projective_plane(2)
    sage: is_projective_plane(p)
    True
    sage: a=p.blocks()
    sage: a[0][2]=5
    sage: s=IncidenceStructure(a)
    sage: is_projective_plane(s,verbose=True)
    Given any two distinct lines, there must be exactly one point incident with both of them : concerns points 0 and 2
    False


    sage: s=IncidenceStructure([[1,2,3],[2,3,5]])
    sage: is_projective_plane(s,verbose=True)
    There must be the same numbers of points and lines
    False


    sage: s=IncidenceStructure([[0,1],[1,2],[2,3],[0,3]])
    sage: is_projective_plane(s,verbose=True)
    There is less than 3 points in the first line
    False

    
    sage: s=IncidenceStructure([[1,2,3],[4,5,6],[1,2,6],[4,5,3],[2,3,4],[2,5,6]])
    sage: is_projective_plane(s,verbose=True)
    if k is the number of points in every lines, the total number of points in a projective plane must be k^2-k+1
    False


    sage: p=designs.projective_plane(2)
    sage: a=p.blocks()
    sage: a[2].append(4)
    sage: s=IncidenceStructure(a)
    sage: is_projective_plane(s,verbose=True)
    Lines must contain the same number of points : concerns lines 0 and 2
    False

    

    ::
    """
    b=list(s._blocks)
    np=len(s._points)
    # Check if there is there are as much points as lines
    if np!=len(b):
        if verbose:
            print "There must be the same numbers of points and lines"
        return False
    k=len(b.pop(0))
    # Check if there is almost 3 points on a line
    if k<3:
        if verbose:
            print "There is less than 3 points in the first line"
        return False
    # Check the relation between number of points in a line and total number of points
    if k**2-k+1!=np:
        if verbose:
            print "if k is the number of points in every lines, the total number of points in a projective plane must be k^2-k+1"
        return False
    compt=1
    for i in b:
        # Check if every lines contains the same number of points
        if len(i)!=k:
            if verbose:
                print "Lines must contain the same number of points : concerns lines 0 and",compt
            return False
        compt+=1
    m=s.incidence_matrix()
    for j in range(np):
        for i in range(j):
            # Check the number of lines passing through points i and j
            li=m.nonzero_positions_in_row(i)
            lj=m.nonzero_positions_in_row(j)
            inter=set(li).intersection(lj)
            if len(inter)!=1:
                if verbose:
                    print 'Given any two distinct points, there must be exactly one line incident with both of them : concerns points',i,'and',j
                return False
    return True


    
    


            

        
