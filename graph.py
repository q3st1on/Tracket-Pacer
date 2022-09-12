from pyvis.network import Network

class dataNetwork:
    def __init__(self, dataStore, filename, nonContrib=False):

        options = {
            "nodes": {
                "borderWidth": 4,
                "borderWidthSelected": 5,
                "opacity": None,
                "size": None
            },
            "edges": {
                "color": {
                "inherit": False
                },
                "selfReferenceSize": None,
                "selfReference": {
                "angle": 0.7853981633974483
                },
                "smooth": {
                "forceDirection": "none"
                }
            },
            "interaction": {
                "hover": True,
                "navigationButtons": True
            },
            "manipulation": {
                "enabled": True
            },
            "physics": {
                "minVelocity": 0.75
            }
        }

        self.net = Network(bgcolor="#222222", height='750px', width='100%', font_color="white")
        nodes = []
        titles = []
        labels = []
        colours = []
        ents = []
        for i in dataStore.destNames:
            if i in dataStore.sourceNames:
                dataStore.sourceNames.remove(i)

        dataStore.genNames()

        for i in range(len(dataStore.names)):
            if nonContrib:
                nodes.append(i)
                labels.append((dataStore.names)[i])
                if (dataStore.names)[i] not in dataStore.destNames:
                    colours.append("#dc8e01")
                    titles.append("Non-Contributory Entity")
                else:
                    colours.append("#feb32b")
                    titles.append("{} ({})".format((dataStore.names)[i], len(nodes)))
            else:
                if (dataStore.names)[i] in dataStore.destNames:
                    ents.append((dataStore.names)[i])
                    nodes.append(len(nodes)+1)
                    labels.append((dataStore.names)[i])
                    colours.append("#feb32b")
                    titles.append("{} ({})".format((dataStore.names)[i], len(nodes)))

        self.net.add_nodes(nodes, label=labels, title=titles, color=colours)

        totaledge = []
        maxEdge = 0
        for i in range(len(dataStore.destNames)):
            edges = []
            for x in dataStore.NetworkEntities[dataStore.destNames[i]].comms:
                try:
                    num = dataStore.NetworkEntities[dataStore.destNames[i]].comms[x]
                    if nonContrib:
                        edges.append((i, (dataStore.names).index(x), num))
                    else:
                        edges.append((i, ents.index(x), num))
                    
                except:
                    continue
            
            totaledge = totaledge + edges   

        finedge = []
        working = {}

        for i in totaledge:
            id = "({}, {})".format(i[0], i[1])
            if id not in working:
                working[id] = float(i[2])
            else:
                working[id] = working[id]+i[2]

        def invert(s):
            tup = tuple(map(int, s[1:len(s)-1].split(', ')))
            return '({}, {})'.format(tup[1], tup[0])

        inverses = {}

        for i in working:
            inverse = invert(i)
            if inverse not in inverses:
                inverses[i] = inverse

        for i in inverses:
            if inverses[i] in working:
                working[i] = working[i] + working[inverses[i]]
                del working[inverses[i]]
        

        for i in working:
            tup = tuple(map(int, i[1:len(i)-1].split(', ')))
            finedge.append((tup[0], tup[1], working[i]))
            if working[i] > maxEdge:
                maxEdge = working[i]

        for i in range(len(finedge)):
            finedge[i] = (finedge[i][0], finedge[i][1], ((finedge[i][2]//(maxEdge/15))+1)) 

        ps = []
        pd = []
        pw = []
        for i in finedge:
            ps.append(i[0])
            pd.append(i[1])
            pw.append(i[2])
        try:
            self.net.add_edges(finedge)
        except BaseException as e:
            print(f"Error: {e}")
            print(f"Sources: {set(ps)}")
            print(f"Destinations: {set(pd)}")
            print(f"Weights: {set(pw)}")
            print(f"Nodes: {nodes}")

        self.net.show(filename)