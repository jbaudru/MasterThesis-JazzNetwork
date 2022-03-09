import utility as uti

import networkx as nx
import dynetx as dn

import numpy as np
import pandas as pd

import powerlaw


class Network:
    def __init__(self, isDigraph = False, isDyna = False):
        self.isDigraph = isDigraph
        self.isDyna = isDyna
        if(isDigraph):
            self.G = nx.MultiGraph()
        else:
            self.G = nx.Graph()
        if(isDyna):
            self.G_Dynamic = dn.DynGraph()
        self.node_sizes = []
        self.uti = uti.Utility()
        self.isDyn = isDyna

    def clear(self):
        self.G.clear()

    def export(self, name):
        nam = "../data/" + name + ".gexf"
        if(not self.isDyna):
            nx.write_gexf(self.G, nam)
        else:
            dn.write_gexf(self.G, nam)

    def addnode(self, name):
        self.G.add_node(name)
        if(self.isDyn):
            self.G_Dynamic.add_node(name)

    def addedge(self, src, dest):
        self.G.add_edge(src, dest)

    def adddynedge(self, src, dest, time):
        if(str(time).isnumeric()): # Avoid case where there is no year in data set
            self.G_Dynamic.add_interaction(src, dest, t=time)

    def addedgeweight(self, src, dest, wt):
        self.G.add_edge(src, dest, weight=wt)

    def getnodes(self):
        return self.G.nodes

    def getdegree(self):
        return self.G.degree

    def getedges(self):
        return self.G.edges()

    def getorder(self):
        return self.G.order()

    def getgraph(self):
        return self.G

    def getdyngraph(self):
        if(self.isDyn):
            return self.G_Dynamic
        else:
            print("Error - contructor argument")
            quit()

    def getneighbours(self, node):
        lst = [n for n in self.G.neighbors(node)]
        return lst

    def computeoccudeg(self):
        occurence = {}
        d = dict(self.G.degree)
        nb_musician = 0
        for key in d:
            nb_musician += 1
            if(d[key] not in occurence):
                occurence[d[key]] = 1
            else:
                occurence[d[key]] += 1
        deg = []
        occ = []
        for i in sorted(occurence.keys()):
            deg.append(i)
            occ.append(occurence[i])
        return occ, deg, nb_musician


    def create_node(self, dic_alb_musician):
        dic_instru_mus = {}
        for k in dic_alb_musician:
            for musician in dic_alb_musician[k]:
                if(musician != "" and musician != " " and len(musician) > 2):
                    musician_name, musician_instru = self.uti.get_name_and_instru(musician)
                    musician_name = self.uti.clean_musician_name_unicode(musician_name)
                    if("(" not in musician_name and ")" not in musician_name):
                        self.addnode(musician_name)
                        #nx.set_node_attributes(G, bb, "betweenness")
                        nx.set_node_attributes(self.G, {musician_name: musician_name}, name="name")
                        nx.set_node_attributes(self.G, {musician_name: musician_instru}, name="instrument")

    def create_edge_instru(self, dic, pds):
        for keyinstru in dic:
            for instru in dic[keyinstru]:
                if(instru != keyinstru):
                    self.addedgeweight(keyinstru, instru, pds[keyinstru][instru])

    def comput_weight_instru(self, dic_mus_instru):
        dic_pds_edge = {}
        tmp_instru = {}
        for instru in dic_mus_instru:
            tmp_instru[instru] = 0
        for instru in dic_mus_instru:
            dic_pds_edge[instru] = tmp_instru.copy()
        for instru in dic_mus_instru:
            for inst in dic_mus_instru[instru]:
                dic_pds_edge[instru][inst] += 1
        return dic_pds_edge


    def create_edge(self, dic_alb_musician, dict_pds, dic_mus_year_collab):
        dic_instru_mus = {}
        for k in dic_alb_musician:
            year = dic_mus_year_collab[k]
            for musician in dic_alb_musician[k]:
                for musician2 in dic_alb_musician[k]:
                    if(musician != musician2):
                        if(musician != "" and musician != " " and len(musician) > 2):
                            if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                musician_name, musician_instru = self.uti.get_name_and_instru(musician)
                                musician_name = self.uti.clean_musician_name_unicode(musician_name)
                                musician2_name, musician2_instru = self.uti.get_name_and_instru(musician2)
                                musician2_name = self.uti.clean_musician_name_unicode(musician2_name)
                                if("(" not in musician_name and ")" not in musician_name and "(" not in musician2_name and ")" not in musician2_name):
                                    self.addedgeweight(musician_name, musician2_name, dict_pds[musician][musician2])
                                    if(not year.isnumeric()):
                                        year = ""
                                    nx.set_edge_attributes(self.G, {(musician_name, musician2_name): {"year": year}})

                                    instrument = self.uti.filter_instrument(musician_instru)
                                    instrument2 = self.uti.filter_instrument(musician2_instru)
                                    # add to dico instrument
                                    if(instrument != "unknown" and instrument2 != "unknown"):
                                        if(instrument not in dic_instru_mus):
                                            dic_instru_mus[instrument] = [instrument2]
                                        else:
                                            dic_instru_mus[instrument].append(instrument2)
        return dic_instru_mus


    def comput_weight(self, dict_alb_musician):
        dic_all_musician_tmp = {}
        for k in dict_alb_musician:
            for musician in dict_alb_musician[k]:
                if(musician not in dic_all_musician_tmp):
                    dic_all_musician_tmp[musician] = 0
        dic_all_musician = {}
        for mus in dic_all_musician_tmp:
            dic_all_musician[mus] = dic_all_musician_tmp.copy()
        for alb in dict_alb_musician:
            for musician in dict_alb_musician[alb]:
                for ms in dict_alb_musician[alb]:
                    if(ms != musician):
                        dic_all_musician[musician][ms] += 1
        return dic_all_musician


    def create_dynamic_edge(self, dic_alb_musician, G, dic_mus_year_collab):
        for k in dic_alb_musician:
            if(str(dic_mus_year_collab[k]).isnumeric()):
                time = int(dic_mus_year_collab[k])
                for musician in dic_alb_musician[k]:
                    for musician2 in dic_alb_musician[k]:
                        if(musician != musician2):
                            if(musician != "" and musician != " " and len(musician) > 2):
                                if(musician2 != "" and musician2 != " " and len(musician2) > 2):
                                    self.adddynedge(musician, musician2, time)



    def get_gamma_value(self):
        lst_deg = list(dict(self.G.degree()).values())
        res = powerlaw.Fit(np.array(lst_deg)+1, xmin=10)
        print("Gamma value : ", res.alpha)
        return res.alpha
