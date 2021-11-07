import networkx as nx
import dynetx as dn
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap
import community as community_louvain
import numpy as np
from decimal import Decimal

import math

import network as n
import video as vid

class Gui:
    def __init__(self, graph):
        self.network = graph

    def show_info(self, num_of_node_to_prt = 10, in_q1_q2 = False, neighbors = False):
        occ, deg, nb_musician = self.network.computeoccudeg()
        d = dict(self.network.getdegree())
        print('==========================================')
        print("Clustering coefficient : ", nx.average_clustering(nx.Graph(self.network.getgraph())))
        print("Transitivity value : ", nx.transitivity(nx.Graph(self.network.getgraph())))
        partition = community_louvain.best_partition(nx.Graph(self.network.getgraph()))
        print("Number of community : ", max(partition.values())+1)
        print("Total number of nodes : ", nb_musician)
        print("Average degree : ", sum(deg)/len(deg))
        max_key = []; max_value = []
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])} # Sort dict in order way
        if(in_q1_q2):
            print('==========================================')
            print("List of nodes whose degree is between the fst. quartile and the sd. quartile :")
            d_q1_q2 = dict(list(d.items())[len(d)//4:len(d)//2])
            lst_musicien = list(islice(d_q1_q2.items(), num_of_node_to_prt))
            for mus in lst_musicien:
                print(mus[0], " : ", d_q1_q2[mus[0]])
        else:
            print('==========================================')
            print("List of most connected nodes and their degree :")
            d_top = dict(list(d.items())[-num_of_node_to_prt:])
            for mus in d_top:
                if(not neighbors):
                    print(mus, " : ", d_top[mus])
                else:
                    print(mus, self.networketneighbours(mus)[0:9])
        print('==========================================')

    def show_network(self, make_circular = False, instru = False):
        if(make_circular):
            pos = nx.circular_layout(self.network.getgraph())
        else:
            pos = nx.spring_layout(self.network.getgraph(), 2/math.sqrt(self.network.order()))
        d = dict(self.network.getdegree())
        H = nx.Graph(self.network.getgraph())
        edges = H.edges()
        if(instru):
            color_lookup = {k:v for v, k in enumerate(sorted(set(H.nodes())))}
            low, *_, high = sorted(color_lookup.values())
            norm = colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20c) #magma

            weights = [H[u][v]['weight']/200 for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1)/8 for v in d.values()], width=weights, node_color=[mapper.to_rgba(i) for i in color_lookup.values()], edge_color="#CBCBCB", with_labels=True, font_size = 10, font_color = "#303030")
        else:
            weights = [H[u][v]['weight'] for u,v in edges]
            nx.draw_networkx(H, pos=pos, node_size=[(v+1) for v in d.values()], node_color ="#5792ad", edge_color="#CBCBCB", width=weights, with_labels=True, font_size = 0.6, font_color = "black")
        plt.axis('off')
        plt.show()


    def show_distrib_pk(self):
        occ, deg, nb_musician = self.network.computeoccudeg()
        dict_occ_deg = {}; dict_pk = {}; dict_deg_gamma = {}
        lst_deg = []; lst_pk = []
        d = dict(self.network.getdegree())
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        # For each degree count the number of node of this degree
        for name in d:
            deg = d[name]
            if(deg > 2):
                if(deg not in dict_occ_deg):
                    dict_occ_deg[deg] = 1
                else:
                    dict_occ_deg[deg] += 1
        # For each degree k compute the value of P(k)
        for deg in dict_occ_deg:
            dict_pk[deg] = dict_occ_deg[deg] / nb_musician
            lst_deg.append(deg)
            lst_pk.append(dict_pk[deg])
        fig = plt.figure()
        plt.plot(lst_deg, lst_pk, '.')
        plt.xlabel('k', fontsize=12)
        plt.ylabel('P(k)', fontsize=12)
        plt.gca().invert_yaxis()
        plt.show()
        # For each degree k compute the value of gamma
        for deg in dict_occ_deg:
            if(deg != 0 and deg != 1 and dict_pk[deg] != 0):
                dict_deg_gamma[deg] = math.log(Decimal(1/dict_pk[deg]),deg)
        avg_gamma = 0
        # Compute the average value of gamma for the degree present in the network
        for deg in dict_deg_gamma:
            avg_gamma += dict_deg_gamma[deg]
        avg_gamma = avg_gamma/len(dict_deg_gamma)
        print("Average value of gamma : ", avg_gamma)


    def show_rich_club_distrib(self):
        rc = nx.rich_club_coefficient(self.network.getgraph(), normalized=True, Q=100)
        lst_deg = []; lst_rc_coef = []
        total_rc = 0
        for deg in rc:
            lst_deg.append(deg)
            lst_rc_coef.append(rc[deg])
            total_rc += rc[deg]
        print("Average rich-club coef : ", total_rc/len(rc))
        fig = plt.figure()
        plt.plot(lst_deg, lst_rc_coef, 'o-')
        fig.suptitle('Rich-club coefficient by degree', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Rich-club coefficient', fontsize=12)
        plt.show()


    def show_occurence(self):
        occ, deg, nb_musician = self.network.computeoccudeg()
        fig = plt.figure()
        plt.plot(deg, occ, 'o-')
        fig.suptitle('Number of node by degree', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Occurence', fontsize=12)
        plt.show()


    def show_clustering(self):
        H = nx.Graph(self.network.getgraph())
        gc =  H.subgraph(max(nx.connected_components(H)))
        lcc = nx.clustering(gc)
        cmap = plt.get_cmap('autumn')
        norm = plt.Normalize(0, max(lcc.values()))
        node_colors = [cmap(norm(lcc[node])) for node in gc.nodes]
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 4))
        nx.draw_spring(gc, node_size=5, node_color=node_colors, with_labels=False, ax=ax1, edge_color="#bfbfbf")
        fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax1)
        ax2.hist(lcc.values(), bins=10)
        ax2.set_xlabel('Clustering')
        ax2.set_ylabel('Frequency')
        plt.tight_layout()
        plt.show()


    def show_community(self, simple_view = False):
        d = dict(self.network.getdegree())
        fig, ax = plt.subplots(figsize=(10, 6),  dpi=600)
        edges = self.network.getgraph().edges()
        partition = community_louvain.best_partition(self.network.getgraph())
        pos = nx.spring_layout(self.network.getgraph(), 2/math.sqrt(self.network.getgraph().order())) #k=5/math.sqrt(self.G.order())
        cmap = cm.get_cmap("twilight_shifted", max(partition.values()) + 1)
        # color map pour les edges avec une valeur alpha
        edgemap = cmap(np.arange(cmap.N))
        edgemap[:,-1] = np.linspace(0.5, 1, cmap.N)
        edgemap = ListedColormap(edgemap)
        # Pour avoir les edges de la même couleur que les communautés
        cedges = []
        for node in self.network.getgraph().nodes():
            for edge in self.network.getgraph().edges(node):
                cedges.append(partition[edge[1]])
        if(simple_view):
            nx.draw_networkx(self.network.getgraph(), pos=pos, cmap=cmap, node_size=0.1, node_color=list(partition.values()), edge_color="grey", with_labels=False, width=0.05, arrows=False)
        else:
            nx.draw_networkx(self.network.getgraph(), pos=pos, node_size=[(v+1)*0.001 for v in d.values()], cmap=cmap, node_color=list(partition.values()), width=0.05, edge_color="grey", connectionstyle=f'arc3,rad=0.2', style='solid', arrowstyle='-', with_labels=True, font_size = 0.01, font_color = "white")
        ax.axis('off')
        fig.set_facecolor('black')
        plt.show()


    def show_dynamic_network(self, time, draw = False):
        V = vid.Video()
        folder = "../data/tmp_vid/"

        pos = nx.kamada_kawai_layout(self.network.getdyngraph())
        lst_year = list(time.values())
        lst_year = list(dict.fromkeys(lst_year)) #remove duplicate year
        start = lst_year[0]

        lst_nodes = self.network.getdyngraph().nodes() #get all node (a modifier si marche pas)
        final_lst_deg = dict(self.network.getgraph().degree)
        lst_deg = {}

        pa_all_time = list(nx.preferential_attachment(self.network.getdyngraph()))
        max_pa = 0
        max_txt = ""
        for it in range(0, len(pa_all_time)):
            if(pa_all_time[it][2] > max_pa):
                max_pa = pa_all_time[it][2]
                max_txt = pa_all_time[it]
        print(max_txt)

        max_pa_by_year = []
        years = []

        for j in range(0,len(lst_year)-1):
            if(lst_year[j] != "year"):
                plt.figure(figsize=(15,10), dpi=100)
                print("Creation network for year : ", lst_year[j])

                s = self.network.getdyngraph().time_slice(t_from= int(start), t_to= int(lst_year[j]))
                lst_nodes = self.network.getdyngraph().nodes(t=int(lst_year[j]))

                cur_dict_deg = dn.degree(self.network.getdyngraph(), lst_nodes, t=int(lst_year[j]))

                lst_nodes_s = s.nodes()
                cur_dict_deg_s = dn.degree(s)


                pref_att_curr_year = list(nx.preferential_attachment(s))
                max_pa_year = 0
                for it in range(0,len(pref_att_curr_year)):
                    if(pref_att_curr_year[it][2] > max_pa_year):
                        max_pa_year = pref_att_curr_year[it][2]
                print("P.A. score max by year", max_pa_year)
                max_pa_by_year.append(max_pa_year)
                years.append(lst_year[j])

                if(draw):
                    ax = plt.gca()
                    ax.margins(0.1, 0.1)
                    ax.set_title(lst_year[j])
                    nx.draw(s, pos, node_size=[v * 2 for v in cur_dict_deg_s.values()], node_color ="#5792ad", edge_color="#bfbfbf", with_labels = True, font_size = 3, font_color = "#212121", ax=ax)
                    _ = ax.axis('off')
                    name = str(lst_year[j])+".png"
                    plt.savefig(folder + name, dpi=100)
                    #plt.show()

        fig = plt.figure()
        plt.plot(max_pa_by_year, years, 'o-')
        fig.suptitle('P.A. max score by year', fontsize=16)
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Year', fontsize=8)
        plt.show()
        if(draw):
            V.create_video_from_imgs(folder, "test")
