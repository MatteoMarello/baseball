import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idmap = {}
        self.bestSol = []
        self.bestScore = 0

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

    def getBestPath(self, id):
        self.bestSol = []
        self.bestScore = 0
        parziale = [self._idmap[id]]
        rimanenti= list(self._idmap.values())
        rimanenti.remove(self._idmap[id])
        scoreAtt = int(self._idmap[id].totale)
        self._recurs(parziale, scoreAtt)
        stringaArchi = ""
        archi = self.getArchiRicorsione()
        for arco in archi:
            stringaArchi += f"_____{arco}____"
        return len(self.bestSol), stringaArchi, self.bestScore

    def _recurs(self, parziale, scoreAtt):
        if scoreAtt > self.bestScore:
            self.bestScore = scoreAtt
            self.bestSol = list(parziale)
        ultimo = parziale[-1]
        for n in self._grafo.neighbors(ultimo):
            if n not in parziale:
                if n.totale < ultimo.totale:
                    parziale.append(n)
                    nuovaScore = scoreAtt + n.totale
                    self._recurs(parziale, nuovaScore)
                    parziale.remove(n)

    def getArchiRicorsione(self):
        listapesi = []
        for i in range(len(self.bestSol) - 1):  # Nota il -1 per evitare IndexError
            u = self.bestSol[i]
            v = self.bestSol[i + 1]
            peso = self._grafo[u][v]['weight']
            listapesi.append(f"peso: {peso}")
        return listapesi









