import pandas as pd
import random as rand
import csv, os

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pandastable import Table

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


fig = Figure()
dist = fig.add_subplot(111)

algorithms = ["Original graph","Random Node", "Random Edge", "Random Walk"]

report = pd.DataFrame(algorithms, columns=['Algorithm'])

# Network Sampling functions

def randomWalk_inv(adjList, sampleSize):
    print("\nRandom Walk inv Strated")
    sampledAdjList = {}
    v = rand.choice(list(adjList.keys()))
    # v = 78
    print("Seed Node : \n", nodeFile[nodeFile.Id == v])
    cur_v = v
    k = 0
    while (len(sampledAdjList)/len(adjList)) < (1-(sampleSize/100)):
        # print(k)
        if k > 100:
            cur_v = v
        if k > 1000:
            break
        next_v = rand.choice(adjList[cur_v])
        if next_v or v not in sampledAdjList.keys():
            if next_v not in sampledAdjList.keys():
                sampledAdjList[next_v] = [cur_v]
            else:
                if cur_v not in sampledAdjList[next_v]:
                    sampledAdjList[next_v].append(cur_v)
            if cur_v not in sampledAdjList.keys():
                sampledAdjList[cur_v] = [next_v]
            else:
                if next_v not in sampledAdjList[cur_v]:
                    sampledAdjList[cur_v].append(next_v)
            cur_v = next_v
            k+=1
    sampledEdgeList =  adjtoedgelist(sampledAdjList)  
    print("len of Sal = ", len(sampledAdjList))
    print("len of Sel = ", len(sampledEdgeList))
    saveascsv(sampledEdgeList,"RWINVSampledEdgeList.csv")
    sampNodeFile = node_file[node_file.Id.isin(list(sampledAdjList.keys()))]
    sampNodeFile.to_csv("RWINVSampledNodeList.csv", index=False, encoding='utf-8')
    print("End of random Walk Inverse")
    return sampledAdjList

def randomWalk(adjList, sampleSize):
    print("\nRandom Walk Strated")
    sampledAdjList = {}
    # v = rand.choice(list(adjList.keys()))
    v = 78
    print("Seed Node : \n", node_file[node_file.Id == v])
    cur_v = v
    k = 0
    while (len(sampledAdjList)/len(adjList))<=sampleSize:
        # print(k)
        if k > 100:
            cur_v = v
        if k > 1000:
            break
        next_v = rand.choice(adjList[cur_v])
        if next_v or v not in sampledAdjList.keys():
            if next_v not in sampledAdjList.keys():
                sampledAdjList[next_v] = [cur_v]
            else:
                if cur_v not in sampledAdjList[next_v]:
                    sampledAdjList[next_v].append(cur_v)
            if cur_v not in sampledAdjList.keys():
                sampledAdjList[cur_v] = [next_v]
            else:
                if next_v not in sampledAdjList[cur_v]:
                    sampledAdjList[cur_v].append(next_v)
            cur_v = next_v
            k+=1
    sampledEdgeList =  adjtoedgelist(sampledAdjList)  
    print("len of Sal = ", len(sampledAdjList))
    print("len of Sel = ", len(sampledEdgeList))
    saveascsv(sampledEdgeList,("RW"+ str(sampleSize) +"SampledEdgeList.csv"))
    sampNodeFile = node_file[node_file.Id.isin(list(sampledAdjList.keys()))]
    sampNodeFile.to_csv(("RW"+ str(sampleSize) +"SampledNodeList.csv"), index=False, encoding='utf-8')
    print("End of random Walk")
    return sampledAdjList, sampledEdgeList

def randomEdge(edgeList,sampleSize):
    print("\nRandom Edge Started")
    sampledAdjList = {}    
    visited = {e: False for e in edgeList}
    global n
    while (len(sampledAdjList)/n)<=sampleSize:
        e = rand.choice(edgeList)
        if visited[e] == False:
            src = e[0]
            tgt = e[1]
            if src not in sampledAdjList.keys():
                sampledAdjList[src] = [tgt]
            else:
                sampledAdjList[src].append(tgt)
            if tgt not in sampledAdjList.keys():
                sampledAdjList[tgt] = [src]
            else:
                sampledAdjList[tgt].append(src)
            visited[e] = True
    sampledEdgeList =  adjtoedgelist(sampledAdjList)  
    print("len of Sal = ", len(sampledAdjList))
    print("len of Sel = ", len(sampledEdgeList))
    saveascsv(sampledEdgeList,("RE"+ str(sampleSize) +"SampledEdgeList.csv"))
    sampNodeFile = node_file[node_file.Id.isin(list(sampledAdjList.keys()))]
    sampNodeFile.to_csv(("RE"+ str(sampleSize) +"SampledNodeList.csv"), index=False, encoding='utf-8')
    print("End of Random Edge")
    return sampledAdjList, sampledEdgeList
        
def randomNode(adjList,sampleSize):
    print("\nRandom Node Started")
    global n
    p = sampleSize## real formula sampleSize/(n +(2*m))
    sampledAdjList = {}
    vertices = list(sorted(adjList.keys()))
    prob = [rand.random() for vertex in vertices]
    while len(sampledAdjList)<= (p*n):
        v = rand.choice(vertices)
        if prob[vertices.index(v)] <= p:                
            sampledAdjList[v] = adjList[v]
            for vertex in adjList[v]:
                if vertex not in sampledAdjList:
                    sampledAdjList[vertex] = [v]
            del prob[vertices.index(v)]
            vertices.remove(v)
    sampledEdgeList = adjtoedgelist(sampledAdjList)
    saveascsv(sampledEdgeList, ("RN"+ str(sampleSize) +"SampledEdgeList.csv"))
    print("len of Sal = ", len(sampledAdjList))
    print("len of Sel = ", len(sampledEdgeList))
    sampNodeFile = node_file[node_file.Id.isin(list(sampledAdjList.keys()))]
    sampNodeFile.to_csv(("RN"+ str(sampleSize) +"SampledNodeList.csv"), index=False, encoding='utf-8')
    print("End of Random Node")
    return sampledAdjList, sampledEdgeList


# Dist Functions
    
def cal_degree(adjList):
    deg = {vertex: len(adjList[vertex]) for vertex in list(sorted(adjList.keys()))}
    return deg

def dig(adjList):
    deg = cal_degree(adjList)
    degree_dist = {x: (list(deg.values()).count(x)/len(deg)) for x in list(set(deg.values()))}
    return degree_dist

# General Sampling functions
    
def temp_fun():
    print("Sampling running")

def saveascsv(edgelist, filename):
    with open(filename, "w") as f:
        fileWriter = csv.writer(f, lineterminator='\n')
        fileWriter.writerow(("source","target"))
        fileWriter.writerows(edgelist)
    print(filename, " is saved successfully")

def fileProcessor(edgeFile,nodeFile):
    adj_list = {}
    
    # edge file
    for i in range(len(edgeFile)):
        source = int(edgeFile.Source[i])
        target = int(edgeFile.Target[i])
        if source not in adj_list.keys():
            adj_list[source] = [target]
        else:
            adj_list[source].append(target)
        if target not in adj_list.keys():
            adj_list[target] = [source]
        else:
            adj_list[target].append(source)
    
    # node file -- missing nodes
    for i in range(len(nodeFile)):
        id = int(nodeFile.Id[i])
        if id not in adj_list.keys():
            if str(id) not in edgeFile.Source:
                if str(id) not in edgeFile.Target:
                    adj_list[id] = []
    return adj_list
    

def fileProcessor_withoutIndividualNodes(edgeFile,nodeFile):
    adj_list = {}
    
    # edge file
    for i in range(len(edgeFile)):
        source = int(edgeFile.Source[i])
        target = int(edgeFile.Target[i])
        if source not in adj_list.keys():
            adj_list[source] = [target]
        else:
            adj_list[source].append(target)
        if target not in adj_list.keys():
            adj_list[target] = [source]
        else:
            adj_list[target].append(source)
    
    return adj_list

def fileProcessor_old(edgeFile,nodeFile):
    adj = {}
    edgelist = edgeFile
    for i in range(len(edgelist)):
        if edgelist.iloc[i,0] in adj.keys():
            adj[edgelist.iloc[i,0]].append(edgelist.iloc[i,1])
        elif edgelist.iloc[i,0] not in adj.keys():
            lis = [edgelist.iloc[i,1]]
            adj[edgelist.iloc[i,0]] = lis
        if edgelist.iloc[i,1] in adj.keys():
            adj[edgelist.iloc[i,1]].append(edgelist.iloc[i,0])
        elif edgelist.iloc[i,1] not in adj.keys():
            lis = [edgelist.iloc[i,0]]
            adj[edgelist.iloc[i,1]] = lis
    ## adding single disconnected nodes with degree 0 
    for i in range(len(nodeFile)):
        if nodeFile.iloc[i,0] not in adj:
           adj[nodeFile.iloc[i,0]] = []
    return adj

def adjtoedgelist(adjList):
    edgList = []
    for src in list(sorted(adjList.keys())):
        for tgt in adjList[src]:
            if src<tgt:
                e = (src,tgt)
                edgList.append(e)
    return edgList
    

# Application Command functions

def browse_node():
    file_path = filedialog.askopenfilename(title="Select Node file")
    ent_node_loc.delete(0, tk.END)
    ent_node_loc.insert(0, file_path)
    print("Selected node file : ", file_path)

def browse_edge():
    file_path = filedialog.askopenfilename(title="Select Edge file")
    ent_edge_loc.delete(0, tk.END)
    ent_edge_loc.insert(0, file_path)
    print("Selected edge file : ", file_path)

def close_app():
    root.destroy()
    print("Successfully closed")
    
def run_algo():
    print("run")    
    global node_file, edge_file
    
    node_file = pd.read_csv(ent_node_loc.get())
    edge_file = pd.read_csv(ent_edge_loc.get())
    sample_size = int(ent_sample_size.get())/100

    adjacency_list = fileProcessor(edge_file,node_file)    
    edge_list = adjtoedgelist(adjacency_list)
    
    global n
    n = len(adjacency_list)
    m = len(edge_list)
    
    print("Original Graph")
    print("len of al = ", n)
    print("len of el = ", m)

    rnAdj, rnEdge = randomNode(adjacency_list, sample_size)
    reAdj, reEdge = randomEdge(edge_list, sample_size)
    rwAdj, rwEdge = randomWalk(adjacency_list, sample_size)     

    org = dig(adjacency_list)
    re = dig(reAdj)
    rn = dig(rnAdj)
    rw = dig(rwAdj)
       
    frm_dist = tk.Frame(frm_preview)
    frm_dist.pack(expand=tk.TRUE,fill=tk.BOTH)
    
    dist.clear()
    canvas = FigureCanvasTkAgg(fig,frm_dist)

    dist.plot(list(org.keys()),list(org.values()), label='Original Graph')
    dist.plot(list(rn.keys()),list(rn.values()), label="Random Node")
    dist.plot(list(re.keys()),list(re.values()), label="Random Edge")
    dist.plot(list(rw.keys()),list(rw.values()), label="Random Walk")
    dist.set_title("Smaple size : " + str(sample_size))
    dist.set_xlabel("Degree")
    dist.set_ylabel("Number of nodes")
    fig.legend(loc='upper right')
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand= tk.TRUE, fill=tk.BOTH)
    
    toolbar = NavigationToolbar2Tk(canvas,frm_dist)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, expand= tk.TRUE, fill=tk.BOTH)
    
    ## Generating reports
    
    g = {}
    # algorithms = ["Original graph","Random Node", "Random Edge", "Random Walk"]
    g["Original graph"] = (adjacency_list,edge_list)
    g["Random Node"] = (rnAdj, rnEdge)
    g["Random Edge"] = (reAdj, reEdge)
    g["Random Walk"] = (rwAdj, rwEdge)
    
    total_node = {}
    total_edge = {}
    max_degree = {}
    min_degree = {}
    avg_degree = {}
    
    for gr in g:
        adj,edge = g[gr]
        total_node[gr] = len(adj)
        total_edge[gr] = len(edge)
        d = cal_degree(adj)
        max_degree[gr] = max(d.values())
        min_degree[gr] = min(d.values())
        avg_degree[gr] = sum(list(d.values()))/len(d.values())
        # print("d : ", d)
        # print("avg_degree ", gr, " : ", avg_degree[gr])
        # print(gr, " -- ", len(adj), " -- ", len(edge))
    report["Total Nodes"] = report['Algorithm'].map(total_node)
    report["Total Edges"] = report['Algorithm'].map(total_edge)
    report["Average_Degree"] = report['Algorithm'].map(avg_degree)
    report["Maximum_Degree"] = report['Algorithm'].map(max_degree)
    report["Minimum_Degree"] = report['Algorithm'].map(min_degree)
    
    lbl_res = tk.LabelFrame(frm_result, text = "Result")
    lbl_res.pack(expand= tk.TRUE, fill=tk.BOTH)
    
    pt = Table(lbl_res, dataframe=report)
    pt.show()
    pt.autoResizeColumns()
    pt.redraw()
    

# General application functions
    
    # --------------


# Start of Main function -- root app initialisation

root = tk.Tk()
root.title("Sampling Algorithms")
root.geometry("1280x720")
root.resizable(True, True)


# frames

frm_node = tk.Frame(root)
frm_node.pack(side=tk.TOP)

frm_edge = tk.Frame(root)
frm_edge.pack()

frm_sampleSize = tk.Frame(root)
frm_sampleSize.pack()

# frm_canvas = tk.Canvas(root)


frm_preview = tk.Frame(root)
frm_preview.pack(expand=tk.TRUE, fill=tk.BOTH)

frm_result = tk.Frame(root)
frm_result.pack(expand = tk.TRUE,fill=tk.BOTH)

frm_footer = tk.Frame(root)
frm_footer.pack(side=tk.BOTTOM)


# Footer frame

btn_close = tk.Button(frm_footer,text="Close", command= close_app)
btn_close.pack(side=tk.RIGHT)

btn_run = tk.Button(frm_footer, text="Run", command= run_algo)
btn_run.pack()


# Node Frame

lbl_node_file = tk.Label(frm_node,text="Node file location")
lbl_node_file.grid(row=0,column=0)

ent_node_loc = tk.Entry(frm_node, width=60)
ent_node_loc.insert(tk.END,"E:/Edu/Sem 2/Data analysis II/ver 2/final/coauthship/Project 2/coauthnodes.csv")
ent_node_loc.grid(row=0,column=1)

btn_browse_node = tk.Button(frm_node, text="Browse", command=browse_node)
btn_browse_node.grid(row=0,column=2)


# Edge Frame

lbl_edge_file = tk.Label(frm_edge,text="Edge file location")
lbl_edge_file.grid(row=0,column=0)

ent_edge_loc = tk.Entry(frm_edge, width=60)
ent_edge_loc.insert(tk.END,"E:/Edu/Sem 2/Data analysis II/ver 2/final/coauthship/Project 2/coauthedges.csv")
ent_edge_loc.grid(row=0,column=1)

btn_browse_edge = tk.Button(frm_edge, text="Browse", command=browse_edge)
btn_browse_edge.grid(row=0,column=2)

# Sample Size Frame

lbl_sample_size = tk.Label(frm_sampleSize, text= "Sample size")
lbl_sample_size.grid(row=0,column=0)

ent_sample_size = tk.Entry(frm_sampleSize, width=10) 
ent_sample_size.insert(tk.END,"30")   
ent_sample_size.grid(row=0, column=1, sticky='w')

lbl_sample_size_desc = tk.Label(frm_sampleSize, text="Enter the Perctange of sample", state=tk.DISABLED, relief = tk.GROOVE)
lbl_sample_size_desc.grid(row=0,column=2)

# Preview frame
prv_msg = tk.StringVar()
lbl_prv = tk.Label(frm_preview, textvariable=prv_msg)
lbl_prv.pack()

root.mainloop()

print("\nEnd Of Program")
