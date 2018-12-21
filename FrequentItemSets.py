import random

"""
Start of A-Priori
"""
class A_Priori:
    def get_baskets(self, filename):
        baskets = []
        with open(filename) as f:
            for line in f:
                items = line.strip().split(' ')
                baskets.append([ int(i) for i in items ])
        return baskets

    #-------------------------------------------------------------
    def fis1(self, baskets, threshold):
        freq = {}
        frequent_items = {}
        for basket in baskets:
            for item in basket:
                if item not in freq:
                    freq[item] = 0
                freq[item] += 1
                if freq[item] > threshold:
                    frequent_items[item] = freq[item]
        return frequent_items

    #-------------------------------------------------------------
    def fis2(self, baskets, f1, threshold):
        freq = {}
        frequent_items = {}
        for basket in baskets:
            for i in range(len(basket)):
                for j in range(i+1, len(basket)):
                    if basket[i] in f1 and basket[j] in f1:
                        a, b = min(basket[i], basket[j]),  max(basket[i], basket[j])
                        if (a,b) not in freq:
                            freq[(a,b)] = 0
                        freq[(a,b)] += 1
                        if freq[(a,b)] > threshold:
                            frequent_items[(a,b)] = freq[(a,b)]
        return frequent_items
    #-------------------------------------------------------------

    #-------------------------------------------------------------
    def fis3(self, baskets, f2, threshold):
        freq = {}
        frequent_items = {}
        for basket in baskets:
            for i in range(len(basket)):
                for j in range(i+1, len(basket)):
                    for k in range(j+1, len(basket)):
                        if (basket[i], basket[j]) in f2 and (basket[i], basket[k]) in f2:
                            a, c = min(basket[i], basket[j], basket[k]),  max(basket[i], basket[j], basket[k])
                            b = basket[i]+basket[j]+basket[k]-(a+c)
                            if (a,b,c) not in freq:
                                freq[(a,b,c)] = 0
                            freq[(a,b,c)] += 1
                            if freq[(a,b,c)] > threshold:
                                frequent_items[(a,b,c)] = freq[(a,b,c)]
        return frequent_items
    #-------------------------------------------------------------

    def a_priori(self, filename):
        #-------------------------------------------------------------
        # PHASE 1
        #-------------------------------------------------------------
        Baskets = self.get_baskets(filename)
        t = 0.005 * len(Baskets)

        print('Phase 1 begins with threshold', t)
        FIS_1 = self.fis1(Baskets, t)
        for k,v in FIS_1.items():
            print(k,v)
        print('There are', len(FIS_1), 'sets.')

        #-------------------------------------------------------------
        # PHASE 2
        #-------------------------------------------------------------
        print('Phase 2 begins with threshold', t)
        FIS_2 = self.fis2(Baskets, FIS_1, t)
        for k, v in FIS_2.items():
            print(k, v)
        print('There are', len(FIS_2), 'sets.')

        #-------------------------------------------------------------
        # PHASE 3
        #-------------------------------------------------------------
        print('Phase 3 begins with threshold', t)
        FIS_3 = self.fis3(Baskets, FIS_2, t)
        for k, v in FIS_3.items():
            print(k, v)
        print('There are', len(FIS_3), 'sets.')
    #-------------------------------------------------------------

"""
End of A-Priori
""" 


#---------------------------------------------------------------------------------------------------



"""
Start of PCY
"""

# CountPair Class for the Count Filter starts here
class CountPair:
    def __init__(self, m):
        self.m = m
        self.Table = [0]*m
        self.a = random.randint(2,1000)
        self.b = random.randint(2,1000)
        self.c = random.randint(2,1000)
        
    #-------------------------------------------------------------
    def hash(self, pair):
        return (pair[0]*self.a + pair[1]*self.b + (pair[2]*self.c if len(pair) == 3 else 0)) % self.m

    #-------------------------------------------------------------
    def add(self, pair):
        i = self.hash(pair)
        self.Table[i] += 1

    #-------------------------------------------------------------
    def clear(self):
        self.Table = [0]*self.m

    #-------------------------------------------------------------
    def is_candidate(self, pair, t):
        i = self.hash(pair)
        return self.Table[i] > t

    #-------------------------------------------------------------
    def compact(self, t):
        for i in range(len(self.Table2)):
            if self.Table[i] > t:
                self.Table2[i] = True

                
# CountPair Class for the Count Filter ends here                
#---------------------------------------------------------------------------------------------------



class PCY:
    def get_baskets(self, filename):
        baskets = []
        with open(filename) as f:
            for line in f:
                items = line.strip().split(' ')
                baskets.append([ int(i) for i in items ])
        return baskets

    #-------------------------------------------------------------
    def fis1(self, baskets, threshold):
        freq = {}
        frequent_items = {}
        cf = CountPair(100000)
        for basket in baskets:
            for i in range(len(basket)):
                item = basket[i]
                if item not in freq:
                    freq[item] = 0
                freq[item] += 1
                if freq[item] > threshold:
                    frequent_items[item] = freq[item]

                # PCY heuristic
                for j in range(i+1, len(basket)):
                    a, b = min(basket[i], basket[j]),  max(basket[i], basket[j])
                    cf.add((a,b))

        return frequent_items, cf

    #-------------------------------------------------------------
    def fis2(self, baskets, f1, cf, threshold):
        freq = {}
        frequent_items = {}
        cf_2 = CountPair(100000)
        for basket in baskets:
            for i in range(len(basket)):
                for j in range(i+1, len(basket)):
                    a, b = min(basket[i], basket[j]),  max(basket[i], basket[j])
                    if (basket[i] in f1) and (basket[j] in f1) and cf.is_candidate((a,b),threshold):
                        if (a,b) not in freq:
                            freq[(a,b)] = 0
                        freq[(a,b)] += 1
                        if freq[(a,b)] > threshold:
                            frequent_items[(a,b)] = freq[(a,b)]

                        # PCY heuristic
                        for k in range(i+2, len(basket)):
                            a, c = min(basket[i], basket[j], basket[k]),  max(basket[i], basket[j], basket[k])
                            b = basket[i]+basket[j]+basket[k]-(a+c)
                            cf_2.add((a,b,c))
        return frequent_items, cf_2
    #-------------------------------------------------------------

    #-------------------------------------------------------------
    def fis3(self, baskets, f2, cf, threshold):
        freq = {}
        frequent_items = {}
        for basket in baskets:
            for i in range(len(basket)):
                for j in range(i+1, len(basket)):
                    for k in range(j+1, len(basket)):
                        a, c = min(basket[i], basket[j], basket[k]),  max(basket[i], basket[j], basket[k])
                        b = basket[i]+basket[j]+basket[k]-(a+c)
                        if (basket[i], basket[j]) in f2 and (basket[i], basket[k]) in f2 and cf.is_candidate((a,b,c),threshold):
                            if (a,b,c) not in freq:
                                freq[(a,b,c)] = 0
                            freq[(a,b,c)] += 1
                            if freq[(a,b,c)] > threshold:
                                frequent_items[(a,b,c)] = freq[(a,b,c)]
        return frequent_items
    #-------------------------------------------------------------

    def pcy(self, filename):
        #-------------------------------------------------------------
        # PHASE 1
        #-------------------------------------------------------------
        Baskets = self.get_baskets(filename)
        t = 0.005 * len(Baskets)

        print('Phase 1 begins with threshold', t)
        FIS_1, cf = self.fis1(Baskets, t)
        for k,v in FIS_1.items():
            print(k,v)
        print('There are', len(FIS_1), 'sets.')

        #-------------------------------------------------------------
        # PHASE 2
        #-------------------------------------------------------------
        print('Phase 2 begins with threshold', t)

        FIS_2, cf_2 = self.fis2(Baskets, FIS_1, cf, t)
        for k, v in FIS_2.items():
            print(k, v)
        print('There are', len(FIS_2), 'sets.  Threshold is', t)
        print('PCY helps us to look at only', len([x for x in cf.Table if x > t]), "item sets.")

        #-------------------------------------------------------------
        # PHASE 3
        #-------------------------------------------------------------
        print('Phase 3 begins with threshold', t)

        FIS_3 = self.fis3(Baskets, FIS_2, cf_2, t)
        for k, v in FIS_3.items():
            print(k, v)
        print('There are', len(FIS_3), 'sets.  Threshold is', t)
        print('PCY helps us to look at only', len([x for x in cf_2.Table if x > t]), "item sets.")
    #-------------------------------------------------------------
"""
End of PCY
"""
