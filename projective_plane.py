def is_projective_plane(s,verbose=False):
    r"""
    Test whether the incidence structure s is a projective plane or not

    INPUT:
    
    - ''s'' -- incidence structure
    
    - ``verbose`` - whether to print additional information


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
        Given any two distinct lines, there must be exactly one point incident with both of them : concerns points 0 and 5 (for the second time in [0, 3, 5] )
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
    b = s._blocks
    N = len(s._points)
    # Check if there is there are as much points as lines
    if N != len(b):
        if verbose:
            print "There must be the same numbers of points and lines"
        return False
    k = len(b[0])-1
    # Check if there is almost 3 points on a line
    if k < 2:
        if verbose:
            print "There is less than 3 points in the first line"
        return False
    # Check the relation between number of points in a line and total number of points
    if k**2+k+1 != N:
        if verbose:
            print "The number of points must be k^2 + k + 1 = ".format()
        return False
    for i in b:
        # Check if every lines contains the same number of points
        if len(i) != k+1:
            if verbose:
                print "Lines must contain the same number of points : concerns lines",[p._points[x] for x in p._blocks[O]],"and",[p._points[x] for x in p._blocks[i]]
            return False
    seen = [[False] * n for n in range(N)]
    for b in s._blocks:
        for i in range(1,k+1):
            for j in range(i):
                if seen[b[i]][b[j]]:
                    if verbose:
                        print 'Given any two distinct points, there must be exactly one line incident with both of them : concerns points',s._points[b[j]],'and',s._points[b[i]],'(for the second time in',[p._points[x] for x in b],')'
                    return False
                seen[b[i]][b[j]] = True
    return True

class ProjectivePlane(IncidenceStructure):
    from sage.numerical.mip import MIPSolverException
    from sage.categories.sets_cat import EmptySetError

    'def __init__'

    def arc(self):
        r"""
        Return the arc which has the biggest cardinality in this projective plane.

        A k-arc in a projective plane is a set of k points, no three colinears.

        For more informations : :wikipedia:`Blocking_set`

        OUTPUT:

        The arc which has the biggest cardinality

        EXAMPLES:

            sage: s=designs.projective_plane(3)
            sage: arc(s)
            [1, 2, 7, 11]
        ::
        """
    
        p=MixedIntegerLinearProgram()
        b=p.new_variable(binary=True)
        p.set_objective(p.sum(b[v] for v in self._points))
        for i in self._blocks:
            p.add_constraint(p.sum(b[k] for k in i)<=2)
        try:
            p.solve()
            r=p.get_values(b)
            return [i for (i,j) in r.items() if j==1]
        except MIPSolverException :
            raise EmptySetError('There is no arc in this incidence structure')
        
    def committee(self):
        r"""
        Return a committee in the projective plane.

        A blocking set is a set of points in a projective plane which every line intersects and which does not contain an entire line.

        A committee is a blocking set of smallest size. For more informations :wikipedia:`Blocking_set`

        EXAMPLES::

            sage: s=designs.projective_plane(3)
            sage: s.committee()
            [1, 3, 5, 7, 10, 11]

            sage: p=designs.projective_plane(2)
            sage: p.committee()
            EmptySetError: There is no blocking set in this incidence structure
        ::
        """
    
        p=MixedIntegerLinearProgram(maximization=False)
        b=p.new_variable(binary=True)
        p.set_objective(p.sum(b[v] for v in self._points))
        for i in self._blocks:
            p.add_constraint(p.sum(b[k] for k in i)>=1)
            p.add_constraint(p.sum(b[k] for k in i)<=len(i)-1)
        try:
            p.solve()
            r=p.get_values(b)
            return [i for (i,j) in r.items() if j==1]
        except MIPSolverException :
            raise EmptySetError('There is no blocking set in this incidence structure.')


        
'''        def make_projective_plane(k):
    if is_prime(k):
        R=GF(k)
        E=[(a,b,c) for a in R for b in R for c in R]
        E.remove((0,0,0))
        return ProjectivePlane([make_line(e,E) for e in E])

def make_line(coef,points):
    l=[]
    for i in points:
        if coef[0]*i[0]+coef[1]*i[1]+coef[2]*i[2]==0: 
            l.append(i)
    return l'''
