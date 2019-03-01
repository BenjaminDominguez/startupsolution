

class User(object):
    def __init__(self, stars):
        self.stars = stars

    def calculate_score(self):
        score = 0
        ranking_weights = {
        1: -2,
        2: -1,
        3: 0,
        4: 1,
        5: 2
        }
        for review in self.stars:
            score += ranking_weights[review]
        return score

u = User([1, 2, 3, 1, 5])
print(u.calculate_score())
