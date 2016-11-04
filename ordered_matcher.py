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

    def push_left(self, pos, arg=None):
        '''
        Pushes the matching to the left where possible.
                pos
                 |
                 v

         x__ y_  z_      x__  y_ z_
         |   |   |  ->   |    |  |
         a   b   c       a,b  c

        Args:
          pos: int, position from which to push
          arg: argument to move left (optional)

        Returns: bool, whether push suceeded.
        '''
        cur_patt = self.patts[pos]

        if arg is None:
            try:
                arg = self.matches[cur_patt.name].pop(0)
            except IndexError:
                return False

        if pos < 1:
            return False
        prev_patt = self.patts[pos - 1]
        if not prev_patt.matchQ(arg):
            return False
        if prev_patt.capacity[1] == len(self.matches[prev_patt.name]):
            if not self.push_left(pos - 1):
                return False
        self.matches[prev_patt.name].append(arg)
        return True

    def match(self):
        '''
        Assign a matching.

        Returns: bool, whether sucessful.
        '''
        if not self.patts:
            return not self.args

        args = list(reversed(self.args))

        # assign each pattern
        for i, patt in enumerate(self.patts):
            for _ in range(patt.capacity[0]):
                while args:
                    arg = args.pop()
                    if patt.matchQ(arg):
                        self.matches[patt.name].insert(0, arg)
                        break
                    else:
                        self.push_left(i, arg)
            if len(self.matches[patt.name]) < patt.capacity[0]:
                # ran out of args
                return False

        # assign left over args
        patt = self.patts[-1]
        match = self.matches[patt.name]
        while args:
            arg = args.pop()
            if not patt.matchQ(arg):
                return False
            if patt.capacity[1] == len(match):
                if not self.push_left(len(self.patts) - 1):
                    return False
            match.append(arg)

        return True
