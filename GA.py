from band import *
from player import *
import schematax as sx
import random
class SA(object):
    def __init__(self,func = all_ones,n=10,p=16,mu=0.1,s=0,e=False):
        """
        n: number of indvs
        p: number of bits for each indv
        mu: mutation rate
        s: selction type: 0 = roullete whel
        e: eleitism.
        """ 
        self.n = n
        self.p = p
        self.mu = mu
        self.s = s
        self.e = e
        self.schemata =[]

        self.pop = [] #current pop go here
        self.best = '' #stores best overall indivdual
        self.bests = [] #stores best individual from each gen
        self.best_f = -float('inf') #the fittness of the best overal indivdual

        self.av_f = [] #stores the average fitness of each population

        self.func = func
        self.player = player()
    def init_pop(self):
        notes = range(len(self.player.cur_scale))
        beats = range(len(self.player.beats)))
        self.pop = [[(random.choice(beats), random.choice(notes)) for _ in xrange(self.p)] for _ in xrange(self.n)]
    
    def mutate(self,indv):
        new = []
        for (b,n) in indv:
            b += 1 % len(self.player.beats)
            n += 1 % len(self.player.notes)
            new.append(b,n)
        return new
        
        pivot = random.randint(0,self.p)

        son = ma[:pivot] + da[pivot:]
        daught = da[:pivot] + ma[pivot:]

        return [son,daught]
    
    def eval_pop(self):
        import time
        import numpy
        self.fs = {}
        bestp = ''
        bestpf = -float('inf')
        for indv in self.pop:
            self.player.play(indv)
            mel_old = server.signal['mel']
            first = len(mel_old)
            time.sleep(25)
            mel_new = server.signal['mel']
            f = numpy.mean(mel_new[first:])
            print "calmness readings: " + str(mel_new[first:])
            print "Fitness of genome, " + indv + " is: " + str(f)
            self.fs[indv] = f

            if f > self.best_f:
                self.best = indv
                self.best_f = f

            if  f > bestpf:
                bestp = indv
                bestpf = f

        self.bests.append(bestp)
        self.av_f.append(np.mean(self.fs.values()))

    def roulette_wheel(self):
        max = sum(self.fs.values())

        pick = random.uniform(0,max)

        current = 0

        for indv in self.fs.keys():
            current += self.fs[indv]
            if current > pick:
                return indv


    def select(self):
        if self.s == 0:
            return self.roulette_wheel()

            


    def make_next_gen(self):
        self.eval_pop()
        new = []
        if self.e:
            new.append(self.bests[-1])
        while len(new) <= self.n:
            mum = self.select()
            dad = self.select()

            new +=  [self.mutate(x) for x in self.crossover(mum,dad)]
        self.pop = new

    def run(self,steps=100):
        self.init_pop()
        for i in range(steps):
            print "gen: ",i
            self.make_next_gen()
            print self.bests
            print self.best



