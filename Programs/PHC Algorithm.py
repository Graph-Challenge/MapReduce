import snap
import time


def algorithm(G,D):
	#Pruning Step
    P=1
    T=0
    while P==1:
        P=0
        for NI in G.Nodes():
            NID=NI.GetId()
            d=NI.GetDeg()
            if d<=D or d>G.GetNodes()-2:
                if d<=D and d>1:
                    for i in range(d-1):
                        for j in range(i+1,d):
                            a=NI.GetNbrNId(i)
                            b=NI.GetNbrNId(j)
                            if G.IsEdge(a,b):
                                T=T+1
                if d>D and d>G.GetNodes()-2:
                    T=T+G.GetEdges()-NI.GetDeg()
                P=1
                G.DelNode(NID)   
	#Hierarchical Clustering Step
    if G.GetNodes()>5:
        H = snap.ConvertGraph(type(G), G)
        S=[]
        i=0    
        while H.GetNodes()>0:
            S.append([])
            S[i].append(snap.GetMxDegNId(H))
            j=1
            TTT=True
            while TTT:
                s = snap.TIntV()
                snap.GetNodesAtHop(H, S[i][0], j, s, True)
                if len(s)!=0:
                    S[i].append(s)
                    j=j+1
                else:
                    TTT=False
            H.DelNode(S[i][0])
            for j in range(1,len(S[i])):
                for nodeID in S[i][j]:
                    H.DelNode(nodeID)
            i=i+1
        subgraphs = [[] for x in range(len(S))]		
		#Counting Step
        for i in range(len(S)):
            for j in range(1,len(S[i])):
                G01 = snap.ConvertSubGraph(snap.PUNGraph,G,S[i][j])
                subgraphs[i].append(G01)
            T=T+subgraphs[i][0].GetEdges()
            G.DelNode(S[i][0])
        for i in range(len(S)):
            for j in range(1,len(S[i])):
                for upnodeID in S[i][j]:
                    U=[]
                    D=[]
                    for t in range(G.GetNI(upnodeID).GetDeg()):
                        a=G.GetNI(upnodeID).GetNbrNId(t)
                        if j<len(S[i])-1:
                            if subgraphs[i][j].IsNode(a):
                                U.append(a)
                        if j>1:        
                            if subgraphs[i][j-2].IsNode(a):
                                D.append(a)
                    for s in range(len(U)):
                        for t in range(s+1,len(U)):
                            if subgraphs[i][j].IsEdge(U[s],U[t]):
                                T=T+1
                    for s in range(len(D)):
                        for t in range(s+1,len(D)):
                            if subgraphs[i][j-2].IsEdge(D[s],D[t]):
                                T=T+1
        for i in range(len(S)):
            for j in range(len(S[i])-1):
                T=T+algorithm(subgraphs[i][j],D)
                
    return T

#Threshold D
for D in range(0,15):
	#Graph G
    G = snap.LoadEdgeList(snap.PUNGraph, "facebook.txt", 0, 1)
    for NI in G.Nodes():
        NID=NI.GetId()
        if G.IsEdge(NID,NID):
            G.DelEdge(NID,NID)   
    tStart = time.time()
	#Output the number of triangles in G
    print algorithm(G,D)
    tEnd = time.time()
	#The time spent while we set threshold=D in the pruning step
    print tEnd - tStart