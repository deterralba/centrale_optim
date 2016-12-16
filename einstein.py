import random

class Nationality:
    norvegien = 'norvegien'
    espagnol = 'espagnol'
    ukranien = 'ukranien'
    japonais = 'japonais'
    anglais = 'anglais'

    @classmethod
    def random(cls):
        return random.choice([Nationality.norvegien, Nationality.espagnol, Nationality.ukranien, Nationality.japonais, Nationality.anglais])

    @classmethod
    def set(cls):
        return {Nationality.norvegien, Nationality.espagnol, Nationality.ukranien, Nationality.japonais, Nationality.anglais}

class Color:
    blue = 'blue'
    blanc = 'blanc'
    jaune = 'jaune'
    vert = 'vert'
    rouge = 'rouge'

    @classmethod
    def random(cls):
        return random.choice([Color.blanc, Color.blue, Color.jaune, Color.vert, Color.rouge])

    @classmethod
    def set(cls):
        return {Color.blanc, Color.blue, Color.jaune, Color.vert, Color.rouge}

class Boisson:
    lait = 'lait'
    cafe = 'cafe'
    the = 'the'
    vin = 'vin'
    other = 'other'

    @classmethod
    def random(cls):
        return random.choice([Boisson.lait, Boisson.cafe, Boisson.the, Boisson.vin, Boisson.other])

    @classmethod
    def set(cls):
        return {Boisson.lait, Boisson.cafe, Boisson.the, Boisson.vin, Boisson.other}

class Animal:
    cheval = 'cheval'
    zebre = 'zebre'
    chien = 'chien'
    escargot = 'escargot'
    renard = 'renard'

    @classmethod
    def random(cls):
        return random.choice([Animal.chien, Animal.zebre, Animal.cheval, Animal.escargot, Animal.renard])

    @classmethod
    def set(cls):
        return {Animal.chien, Animal.zebre, Animal.cheval, Animal.escargot, Animal.renard}

class Cigarette:
    chest = 'chest'
    kools = 'kools'
    gitanes = 'gitanes'
    cravens = 'cravens'
    old = 'old'

    @classmethod
    def random(cls):
        return random.choice([Cigarette.chest, Cigarette.kools, Cigarette.gitanes, Cigarette.cravens, Cigarette.old])

    @classmethod
    def set(cls):
        return {Cigarette.chest, Cigarette.kools, Cigarette.gitanes, Cigarette.cravens, Cigarette.old}

class Home:
    def __init__(self, id, color, nationality, cigarette, boisson, animal):
        self.id = id
        self.color = color
        self.nationality = nationality
        self.cigarette = cigarette
        self.boisson = boisson
        self.animal = animal

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.id, self.color, self.nationality, self.cigarette, self.boisson, self.animal)

def get_rand(set):
    el = random.sample(set, 1)[0]
    set -= {el}
    return el

class Solution:
    def __init__(self, list_homes):
        self.id = {home.id: home for home in list_homes}
        self.color = {home.color: home for home in list_homes}
        self.nationality = {home.nationality: home for home in list_homes}
        self.cigarette = {home.cigarette: home for home in list_homes}
        self.boisson = {home.boisson: home for home in list_homes}
        self.animal = {home.animal: home for home in list_homes}
        self.list_homes = list_homes

    def __str__(self):
        return '\n'.join((str(home) for home in self.list_homes))

    @classmethod
    def random(cls):
        list_homes = []
        colors = Color.set()
        nationalities = Nationality.set()
        cigarettes = Cigarette.set()
        boissons = Boisson.set()
        animals = Animal.set()
        # print(colors, nationalities, cigarettes, boissons, animals)
        for i in range(1, 6):
            l = [get_rand(item) for item in (colors, nationalities, cigarettes, boissons, animals)]
            home = Home(i, *l)
            list_homes.append(home)
        return Solution(list_homes)

def brute_force_gen():
    for id in range(1, 5):
        for color in Color.set():
            for nationality in Nationality.set():
                for cigarette in Cigarette.set():
                    for boisson in Boisson.set():
                        for animal in Animal.set():
                            yield Solution()

def check_sol(sol):
    constr = [
	# Le norvégien habite la première maison,
        sol.id[1].nationality == Nationality.norvegien,

	# La maison à coté de celle du norvégien est bleue,
	(sol.nationality[Nationality.norvegien].id == sol.color[Color.blue].id + 1) or
            (sol.nationality[Nationality.norvegien].id == sol.color[Color.blue].id - 1),

	# L’habitant de la troisième maison boit du lait,
        sol.id[3].boisson == Boisson.lait,

	# L’anglais habite la maison rouge,
        sol.nationality[Nationality.anglais].color == Color.rouge,

	# L’habitant de la maison verte boit du café,
        sol.color[Color.vert].boisson == Boisson.cafe,

	# L’habitant de la maison jaune fume des Kools,
        sol.color[Color.jaune].cigarette == Cigarette.kools,

	# La maison blanche se trouve juste après la verte,
        sol.color[Color.blanc].id == sol.color[Color.vert].id + 1,
    ]
    '''

	# L’espagnol a un chien,
        sol.nationality[Nationality.espagnol].animal == Animal.chien,

	# L’ukrainien boit du thé,
        # sol.nationality[Nationality.ukranien].boisson == Boisson.the,

	# Le japonais fume des cravens,
        sol.nationality[Nationality.japonais].cigarette == Cigarette.cravens,

	# Le fumeur de old golds a un escargot,
        sol.cigarette[Cigarette.old].animal == Animal.escargot,

	# Le fumeur de gitanes boit du vin,
        sol.cigarette[Cigarette.gitanes].boisson == Boisson.vin,

	# Un voisin du fumeur de Chesterfields a un renard,
	(sol.cigarette[Cigarette.chest].id == sol.animal[Animal.renard].id + 1) or
            (sol.cigarette[Cigarette.chest].id == sol.animal[Animal.renard].id - 1),

        # Un voisin du fumeur de Kools a un cheval.
	(sol.cigarette[Cigarette.kools].id == sol.animal[Animal.cheval].id + 1) or
            (sol.cigarette[Cigarette.kools].id == sol.animal[Animal.cheval].id - 1),
    ]'''
    return all(constr)

if __name__ == '__main__':
    sol = Solution.random()

    i = 0
    while not check_sol(sol):
        i += 1
        sol = Solution.random()
        if i % 100000 == 0:
            print(i)

    print(sol)
