#def arc(S):  #s structure d'incidence
    #ne fonctionne pas si les points en sont pas numérotés (0,..n-1)
#    blocs=S._blocks
#    b=[0 for i in range(len(blocs))]
#    arc=[blocs[0][0]]
#    for i in range(len(blocs)):
#        if b[i]==0:
#            j=0
#            while blocs[i][j] in arc and j<min(2,len(blocs[i])):
#                 #point déja dans l'arc ou qui formerait une ligne de 3 points
#                j+=1 
#            if j==1:
#                arc.append(blocs[i][j])
#            b[i]=1
#        print(arc)
#    print(arc)




def independent_set(g):
    "return an indepedent set in g"
    p=MixedIntegerLinearProgram()
    b=p.new_variable(binary=True)
    p.set_objective(sum(b[v] for v in g.vertices()))
    for i in g.edges(labels=False):
        p.add_constraint(b[i[0]]+b[i[1]]<=1)
    p.solve()
    r=p.get_values(b)
    return [i for (i,j) in r.items() if j==1]            

def arc(s):
    "return the arc which has the biggest cardinality in s"
    p=MixedIntegerLinearProgram()
    b=p.new_variable(binary=True)
    p.set_objective(sum(b[v] for v in s._points))
    for i in range(len(s.blocks())):
        p.add_constraint(sum(b[k] for k in s.blocks()[i])<=2)
    p.solve()
    r=p.get_values(b)
    return [i for (i,j) in r.items() if j==1]

def blocking_set(s):
    "return the blocking set which has the lowest cardinality in s"
    p=MixedIntegerLinearProgram()
    b=p.new_variable(binary=True)
    p.set_objective(-sum(b[v] for v in s._points))
    for i in range(len(s.blocks())):
        p.add_constraint(sum(b[k] for k in s.blocks()[i])>=1)
        p.add_constraint(sum(b[k] for k in s.blocks()[i])<=len(s.blocks()[i])-1)
    p.solve()
    r=p.get_values(b)
    return [i for (i,j) in r.items() if j==1]
