import graphviz


def processGraph(n):
    nodes = []
    g = graphviz.Digraph('gaussian_elimination_diekert')

    # nodes generation
    for k in range(1, n):
        for j in range(k+1, n+1):
            desc_a = "A" + str(j) + str(k)
            nodes.append(desc_a)
            g.node(desc_a, color='red')
            for i in range(k, n+2):
                desc_b = "B" + str(i) + str(j) + str(k)
                nodes.append(desc_b)
                g.node(desc_b, color='blue')

                desc_c = "C" + str(i) + str(j) + str(k)
                nodes.append(desc_c)
                g.node(desc_c, color='green')

                g.edge(desc_a, desc_b)
                g.edge(desc_b, desc_c)

    print("Nodes: ")
    print(nodes)

    # edges generation
    for kc in range(1, n+2):
        for jc in range(1, n+2):
            for ic in range(1, n+2):
                desc_c = "C" + str(ic) + str(jc) + str(kc)
                for ka in range(1, n + 2):
                    for ja in range(1, n + 2):
                        desc_a = "A" + str(ja) + str(ka)
                        if desc_a in nodes and desc_c in nodes:
                            if ic == ka and kc == ka-1:
                                if jc == ja:
                                    g.edge(desc_c, desc_a)
                                if jc == ka:
                                    g.edge(desc_c, desc_a)

    for kc in range(1, n+2):
        for jc in range(1, n+2):
            for ic in range(1, n+2):
                desc_c = "C" + str(ic) + str(jc) + str(kc)
                for kb in range(1, n + 2):
                    for jb in range(1, n + 2):
                        for ib in range(1, n + 2):
                            desc_b = "B" + str(ib) + str(jb) + str(kb)
                            if desc_b in nodes and desc_c in nodes:
                                if ic == ib and jc == kb and kc == kb-1 and ic != jc:
                                    g.edge(desc_c, desc_b)

    for k1 in range(1, n+2):
        for j1 in range(1, n+2):
            for i1 in range(1, n+2):
                desc_c1 = "C" + str(i1) + str(j1) + str(k1)
                for k2 in range(1, n + 2):
                    for j2 in range(1, n + 2):
                        for i2 in range(1, n + 2):
                            desc_c2 = "C" + str(i2) + str(j2) + str(k2)
                            if desc_c1 in nodes and desc_c2 in nodes:
                                if i1 == i2 and j1 == j2 and k1 == k2-1 and k2 != i2:
                                    g.edge(desc_c1, desc_c2)

    # FNF generator
    FNF = []
    for k in range(1, n):
        fnf_a = []
        fnf_b = []
        fnf_c = []
        for j in range(k+1, n+1):
            desc_a = "A" + str(j) + str(k)
            fnf_a.append(desc_a)
            for i in range(k, n+2):
                desc_b = "B" + str(i) + str(j) + str(k)
                fnf_b.append(desc_b)
                desc_c = "C" + str(i) + str(j) + str(k)
                fnf_c.append(desc_c)

        FNF.append(fnf_a)
        FNF.append(fnf_b)
        FNF.append(fnf_c)

    print(" ")
    print("FNF")
    for elem in FNF:
        print(elem)

    g.view()


if __name__ == '__main__':
    n = int(input("n = "))
    processGraph(n)
