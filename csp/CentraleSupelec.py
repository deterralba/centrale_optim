#!/usr/bin/env python3

# 2016 - Ecole Centrale Supélec - les élèves du cours d'optimisation et leur enseignant


class CSP:
    """Implémente un solveur de programmation par contraintes
    """

    def __init__(self, domaines):
        """Crée un problème de satisfaction par contraintes
        avec n variables numérotés de 0 à n-1.

        :param domaines: liste d'ensembles. Les éléments des ensembles peuvent être de tout type.
        """
        n = len(domaines)
        self.var = range(n)
        self.dom = domaines
        self.conflict = [[] for x in self.var]
        self.assigned = [None] * n
        self.context = []
        self.nodes = 0
        self.print_tree = False
        self.maintain_AC = False

    def addConstraint(self, x, y, relation):
        """Ajoute une contrainte binaire sur le couple de variables x et y.
        :param x, y: identificateurs de variables entre 0 et n-1
        :param relation: ensemble de couple de valeurs u,v tel que
        l'affectation x := u, y := u satisfait la contrainte.
        (par abus de notation x est la variable et son indice).
        """
        self.conflict[x].append((y, relation))
        self.conflict[y].append((x, {(v,u) for (u,v) in relation}))


    def maintain_arc_consistency(self):
        self.maintain_AC = True

    def solve(self):
        """Itérateur sur toutes les solutions.

        nodes contiendra à tout moment le nombre de nœuds de l'arbre d'exploration
        print_tree indique si solve() doit afficher une ligne par nœud de l'arbre
        maintain_AC indique si solve() doit maintenir l'arc consistance
        """
        self.nodes += 1
        x = self.selectVar()
        if x is None:  # toutes les variables sont affectées
            yield self.assigned
        else:
            for u in self.dom[x]:
                self.assigned[x] = u
                depth = len([z for z in self.var if self.assigned[z] is not None])
                if self.print_tree:
                    print("%s x%i=%i" % ("  " * depth, x, u))
                history = self.save_context()
                Q = self.forward_check(x)
                if self.maintain_AC:        # établir la maintenance de l'arc constance si nécessaire
                    self.arc_consistency(Q)
                for sol in self.solve():
                    yield sol
                self.restore_context(history)
                self.assigned[x] = None

    # --- gestion de contexte

    def save_context(self):
        return len(self.context)

    def restore_context(self, history):
        while len(self.context) > history:
            x, vals = self.context.pop()
            self.dom[x] |= vals

    def remove_vals(self, x, vals):
        self.context.append((x, vals))
        self.dom[x] -= vals

    # --- exploration

    def selectVar(self):
        """choisit une variable de branchement.
        Heuristique: choisir la variable au domaine minimal

        :returns: un indice de variable ou Npne, si toutes les variables sont affectées
        """
        choice = None
        for x in self.var:
            if self.assigned[x] is None and  \
               (choice is None or len(self.dom[x]) < len(self.dom[choice])):
               choice = x
        return choice

    def forward_check(self, x):
        """Effectue la vérification en avant après une affectation à x
        """
        u = self.assigned[x]
        Q = set()
        for y, rel in self.conflict[x]:
            to_remove = set()
            for v in self.dom[y]:
                if (u, v) not in rel:
                    to_remove.add(v)
            if to_remove:
                self.remove_vals(y, to_remove)
                Q.add(y)
        return Q

    # --- arc consistance

    def arc_consistency(self, Q):
        """Le domaine des variables dans Q a été réduit.
        Maintenir l'arc consistance.
        Implémente l'algorithme AC3.
        """
        while Q:
            x = Q.pop()
            for y, relation in self.conflict[x]:
                if self.assigned[y] is None:
                    if self.revise(x, y, relation):
                        Q.add(y)


    def revise(self, x, y, relation):
        """le domaine de x vient d'être réduit.
        Vérifier si celui de y doit être réduit à son tour.
        :returns: True si le domaine de y a été réduit
        """
        to_remove = set()
        for v in self.dom[y]:
            if not self.hasSupport(y, v, x, relation):
                to_remove.add(v)
        self.remove_vals(y, to_remove)
        return to_remove

    def hasSupport(self, y, v, x, relation):
        """est-ce que l'affectation y := v a un support dans le domaine de x ?
        """
        for u in self.dom[x]:
            if (u, v) in relation:
                    return True
        return False

