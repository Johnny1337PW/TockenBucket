from time import time
from time import sleep
import numpy as np
import functools
import operator


class TokenBucket(object):
    def __init__(self, tokens, fill_rate, tokens2, fill_rate2):
        self.capacity = float(tokens)
        self._tokens = float(tokens)
        self.fill_rate = float(fill_rate)
        self.capacity2 = float(tokens2)
        self._tokens2 = float(tokens2)
        self.fill_rate2 = float(fill_rate2)

    def consume(self, tokens):
        TokenBucket.get_tokens(self)
        TokenBucket.get_tokens2(self)
        statetokens1 = self._tokens
        statetokens2 = self._tokens2
        if tokens <= statetokens1:
            self._tokens -= tokens
            return True,self._tokens,self._tokens2
        elif(tokens <= statetokens2):
            self._tokens2 -= tokens
            return True,self._tokens,self._tokens2
        else:
            return False,self._tokens,self._tokens2


    def consumeboth(self, tokens, tokens2):
        TokenBucket.get_tokens(self)
        TokenBucket.get_tokens2(self)
        tokensall = tokens+tokens2
        statetokens1 = self._tokens
        statetokens2 = self._tokens2
        if (tokensall <= statetokens1):
            self._tokens -= tokensall
            return True,True,self._tokens,self._tokens2
        elif (tokens<=statetokens1 and tokens2 <=statetokens2):
            self._tokens -= tokens
            self._tokens2 -= tokens2
            return True,True, self._tokens,self._tokens2
        elif(tokensall<=statetokens2):
            self._tokens2 -= tokensall
            return True,True, self._tokens,self._tokens2
        elif(tokens<=statetokens1 and tokensall>=statetokens1):
            self._tokens -= tokens
            return True, False, self._tokens,self._tokens2
        elif(tokens<=statetokens2 and tokensall>=statetokens2):
            self._tokens2 -= tokens
            return True, False, self._tokens,self._tokens2
        elif (tokens>=statetokens2 and tokens2<=statetokens2):
            self._tokens2 -= tokens2
            return False, True, self._tokens,self._tokens2
        elif (tokens>=statetokens1 and tokens2<=statetokens1):
            self._tokens -= tokens2
            return False, True, self._tokens,self._tokens2
        elif(tokensall>statetokens2):
            return False, False, self._tokens,self._tokens2

    def get_tokens(self):
        if self._tokens < self.capacity:
            self._tokens = min(self.capacity, self._tokens + self.fill_rate)
        return self._tokens

    def get_tokens2(self):
        if self._tokens2 < self.capacity2:
            self._tokens2 = min(self.capacity2, self._tokens2 + self.fill_rate2)
        return self._tokens2
    tokens = property(get_tokens)
    tokens2 = property(get_tokens2)

def get_both_tokens_nodelay(bucket1):
    return (bucket1.tokens, bucket1.tokens2)

def iter_list(a_list,textfile):
    for element in a_list:
        textfile.write(str(element)+",")
    textfile.write("\n")

def starttest(cap,frate,cap2,frate2):
    src1 = np.full(1200,1)
    #src2 = [0,0,0,0,0,0,0...]
    #src2 = [1,1,1,1,1,1,1...]
    src2 = np.full(1200,1)
    bucket = TokenBucket(cap, frate, cap2, frate2)
    f = open("dane.csv", "w")

    for x in range(0,1200):
        if (src1[x]==1 and src2[x]==1):
            print ("consumed 1,1 = ", (iter_list(list(bucket.consumeboth(0.008,0.008)),f)))
        elif (src2[x]==1):
            print ("consumed 1 = ", (iter_list(list(bucket.consume(0.008)),f)))
        elif (src1[x]==1):
            print ("consumed 1 = ", (iter_list(list(bucket.consume(0.008)),f)))
        elif (src2[x]==0 and src1[x]==0):
            iter_list(list(get_both_tokens_nodelay(bucket)),f)
    f.close()

if __name__ == '__main__':
    #starttest(CapacityTB1,FillRateTB1,CapacityTB2,FillRateTB2):
    starttest(0.008,0.01,0.66,0.005)

