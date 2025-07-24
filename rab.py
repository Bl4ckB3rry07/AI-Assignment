class RabbitState:
    def __init__(self, con):
        self.con = con  

    def goalTest(self):
        return self.con == 'RRR_LLL'

    def moveGen(self):
        successors = []
        s = list(self.con)
        i = s.index('_')
        for move in [-1, 1, -2, 2]:
            j = i + move
            if 0 <= j < len(s):
                if (move == -1 and s[j] == 'L') or \
                   (move == 1 and s[j] == 'R') or \
                   (move == -2 and s[j] == 'L' and s[i - 1] in ['L', 'R']) or \
                   (move == 2 and s[j] == 'R' and s[i + 1] in ['L', 'R']):
                    new_con = s[:]
                    new_con[i], new_con[j] = new_con[j], new_con[i]
                    successors.append(RabbitState(''.join(new_con)))
        return successors

    def __eq__(self, other):
        return isinstance(other, RabbitState) and self.con == other.con

    def __hash__(self):
        return hash(self.con)

    def __repr__(self):
        return self.con

