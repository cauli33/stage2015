def arc(s, filename):
    f = open(filename, "w")
    f.write("; Arc \n")

    for p in s._points:
        f.write("(int q_{} 0 1)\n".format(p))
    f.write("(int m 0 ")
    l=str(len(s._points))
    f.write(l)
    f.write(") \n")
    f.write("(objective maximize m)\n")
    f.write("(= m (+ ")
    for p in s._points:
        f.write(" q_{}".format(p))
    f.write("))\n")       
    for b in s._blocks:
        f.write("(le (+")
        for i in b:
            f.write(" q_{}".format(i))
        f.write(") 2)\n")
    f.write(";END")
    f.close()
