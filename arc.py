from sage.numerical.mip import MIPSolverException
from sage.categories.sets_cat import EmptySetError
          

def arc(s):
    r"""
    Return the arc which has the biggest cardinality in s

    INPUT:
    
    - ''s'' -- incidence structure

    OUTPUT:
    
    The list of the points from the arc which has the biggest cardinality in s.

    EXAMPLES:
    ::
        sage: s=designs.projective_plane(3)
        sage: arc(s)
        [1, 2, 7, 11]
    ::
    """
    
    p=MixedIntegerLinearProgram()
    b=p.new_variable(binary=True)
    p.set_objective(p.sum(b[v] for v in s._points))
    for i in s._blocks:
        p.add_constraint(p.sum(b[k] for k in i)<=2)
    try:
        p.solve()
        r=p.get_values(b)
        return [i for (i,j) in r.items() if j==1]
    except:
        print('There is  no arc in this incidence structure.')











        
def blocking_set(s):
    r"""
    Return the blocking set which has the lowest cardinality in s

    INPUT:
    
    - ''s'' -- incidence structure

    OUTPUT:
    
    The list of the points from the minimal blocking set in s.

    EXAMPLES::
    
        sage: s=designs.projective_plane(3)
        sage: blocking_set(s)
        [1, 3, 5, 7, 10, 11]

        sage: p=designs.projective_plane(2)
        sage: blocking_set(p)
        EmptySetError: There is no minimal blocking set in this incidence structure
    ::
    """
    
    p=MixedIntegerLinearProgram(maximization=False)
    b=p.new_variable(binary=True)
    p.set_objective(p.sum(b[v] for v in s._points))
    for i in s._blocks:
        p.add_constraint(p.sum(b[k] for k in i)>=1)
        p.add_constraint(p.sum(b[k] for k in i)<=len(i)-1)
    try:
        p.solve()
        r=p.get_values(b)
        return [i for (i,j) in r.items() if j==1]
    except MIPSolverException :
        raise EmptySetError('There is no blocking set in this incidence structure')
       









    

def is_minimal_blocking_set(b,s):
     r"""
    Test whether the blocking set b is a minimal blocking set in s or not

    INPUT:
    
    - ''b'' -- blocking set
    - ''s'' -- incidence structure

    OUTPUT:
    
    True/False bool

    EXAMPLES::
    
    sage: p=designs.projective_plane(4)
    sage: b=blocking_set(p)
    sage: is_minimal_blocking_set(b,p)
    True


    ::
    """
     m=s.incidence_matrix()
     v=True
     for i in b:
        v=False
        for j in range(len(s._blocks)):
            if m[i,j]==1 and sum(m[k,j] for k in b if k!=i)==0:
                v=True
                break
        if not v:
            break
     return v






 
def concurrent_lines(p,s):
    r"""
    Return the lines that contains the point p in s.

    INPUT:

    - ''p'' -- point
    - ''s'' -- incidence structure

    OUTPUT:
    
    The list of lines that contains the point p.

    EXAMPLES::
    
        sage: s=designs.projective_plane(4)
        sage: concurrent_lines(10,s)
        [[0, 5, 10, 15, 19],
        [1, 7, 10, 12, 17],
        [2, 6, 10, 14, 16],
        [3, 4, 10, 13, 18],
        [8, 9, 10, 11, 20]]                
        sage: concurrent_lines(30,s)
        []

        sage: p=designs.projective_plane(2)
        sage: concurrent_lines(4,p)
        [[0, 2, 4], [1, 3, 4], [4, 5, 6]]
        
    ::
    """
    res=[]
    for z in s.blocks():
        if p in z:
            res.append(z)
    return res
    





         
def minimal_blocking_set(s):
    r"""
    Return the minimal blocking set which has the lowest cardinality in s

    INPUT:
    
    - ''s'' -- incidence structure

    OUTPUT:
    
    The list of the points from the minimal blocking set which has the lowest cardinality in s.

    EXAMPLES::
    
        sage: s=designs.projective_plane(4)
        sage: minimal_blocking_set(s)
        [0, 3, 5, 7, 14, 15, 20]

    ::
    """
    p=MixedIntegerLinearProgram(maximization=False)
    b=p.new_variable(binary=True)
    p.set_objective(p.sum(b[v] for v in s._points))
    for x in s._points:
        p.add_constraint(p.sum(b[tuple(i)] for i in concurrent_lines(x,s))>=b[x])    
    for i in s._blocks:
        p.add_constraint(p.sum(b[k] for k in i)>=1)
        p.add_constraint(p.sum(b[k] for k in i)<=len(i)-1)
        p.add_constraint(b[tuple(i)]>=2-p.sum(b[k] for k in i))
        p.add_constraint(1+len(i)*(1-b[tuple(i)])>=p.sum(b[k] for k in i))     
    try:
        p.solve()
    except MIPSolverException :
        raise EmptySetError('There is no minimal blocking set in this incidence structure')     
    r=p.get_values(b)
    return [i for (i,j) in r.items() if j==1 and type(i)==int]
