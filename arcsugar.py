def arc(b, s, filename):
    ' b is for the bibd and s for the (s,n)-arc'
    f = open(filename, "w")
    f.write("; Arc \n")
    for p in b._points:
        f.write("(int q_{} 0 1)\n".format(p))
    f.write("(int m 0 ")
    l=str(len(b._points))
    f.write(l)
    f.write(") \n")
    f.write("(objective maximize m)\n")
    f.write("(= m (+ ")
    for p in b._points:
        f.write(" q_{}".format(p))
    f.write("))\n")       
    for bl in b._blocks:
        f.write("(le (+")
        for i in bl:
            f.write(" q_{}".format(i))
        f.write(") ")
        f.write(s)
        f.write(")\n")
    f.write(";END")
    f.close()
