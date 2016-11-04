from collections import defaultdict


class Matcher(object):
    def __init__(self, patts, args):
        self.patts = patts
        self.args = args
        self.matches = defaultdict(list)

    def match_ends(self):
        '''
        Matches unambiguous end patterns.

        returns: None.
        '''
        max_overlap = min(len(self.patts), len(self.args))
        for i, (patt, arg) in enumerate(zip(self.patts, self.args)):
            if not self.assign_match(patt, arg):
                break
        if i == max_overlap + 1:
            self.patts = self.patts[i:]
            self.args = self.args[i:]
            return
        for j, (patt, arg) in enumerate(zip(reversed(self.patts), reversed(self.args))):
            if not self.assign_match(patt, arg):
                break
        self.patts = self.patts[i:len(self.patts)-j]
        self.args = self.args[i:len(self.args)-j]
        return

    def assign_match(self, patt, *args):
        '''
        Assigns args to patt.

        returns: bool, True if assignment sucessful.
        '''
        if patt.capacity[0] > len(args):
            return False
        if patt.capacity[1] < len(args):
            return False
        if all(patt.matchQ(arg) for arg in args):
            self.matches[patt.name] = args
            return True
        return False

    def push_right(self, pos, arg=None):
        '''
        Pushes the matching to the right where possible.

        x_  y_  z__       x_  y_  z__
         |   |   |   ->    |   |   |
        [a] [b] [c]       []  [a] [b, c]

        Args:
          pos: int, position from which to push
          arg: argument to move right (optional)

        Returns: bool, whether push suceeded.
        '''
        cur_patt = self.patts[pos]

        if arg is None:
            arg = self.matches[cur_patt.name].pop()

        if pos + 1 >= len(self.patts):
            return False
        next_patt = self.patts[pos + 1]
        if not next_patt.matchQ(arg):
            return False
        if next_patt.capacity[1] == len(self.matches[next_patt.name]):
            if not self.push_right(pos + 1):
                return False
        self.matches[next_patt.name].insert(0, arg)
        return True

    def match(self):
        '''
        Assign a matching.

        Returns: bool, whether sucessful.
        '''
        if not self.patts:
            return not self.args

        # assign each pattern
        i = len(self.patts) - 1
        while i >= 0:
            patt = self.patts[i]
            for _ in range(patt.capacity[0]):
                while self.args:
                    arg = self.args.pop()
                    if patt.matchQ(arg):
                        self.matches[patt.name].insert(0, arg)
                        break
            if len(self.matches[patt.name]) < patt.capacity[0]:
                return False
            i -= 1

        # assign left over args
        patt = self.patts[0]
        match = self.matches[patt.name]
        while self.args:
            arg = self.args.pop()
            if not patt.matchQ(arg):
                return False
            if patt.capacity[1] == len(match):
                if not self.push_right(0):
                    return False
            match.insert(0, arg)

        return True
