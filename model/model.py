import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idmap = {}

    def get_year(self):
        return DAO.getYears()

    def get_squadre(self,year):
        return DAO.getSquadre(year)

    def build_graph(self,anno):
        self._grafo.clear()
        self._idmap.clear()
        nodi = DAO.getNodi(anno)
        for n in nodi:
            self._idmap[n.ID] = n
        self._grafo.add_nodes_from(nodi)
        from itertools import combinations
        for u, v in combinations(nodi, 2):
            self._grafo.add_edge(u, v, weight = u.totale + v.totale)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def get_s(self):
        return self._grafo.nodes()

    def get_details2(self, teamid):
        team = self._idmap[teamid]
        listaStampare=[]
        vicini = self._grafo.neighbors(team)
        for vicino in vicini:
            peso = self._grafo[team][vicino]['weight']
            listaStampare.append((team, vicino, peso))
        listaStampare.sort(key=lambda x: x[2], reverse=True)
        listadef = []
        for elemento in listaStampare:
            listadef.append(f"_____ nodo di arrivo {elemento[1]}, peso: {elemento[2]}____")
        return listadef




