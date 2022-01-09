from time import time
from time import sleep
import functools
import operator

class TokenBucket(object):
    """An implementation of the token bucket algorithm.
    
    >>> bucket = TokenBucket(80, 0.5)
    >>> print bucket.consume(10)
    True
    >>> print bucket.consume(90)
    False
    """
    def __init__(self, tokens, fill_rate, tokens2, fill_rate2):
        """tokens is the total tokens in the bucket. fill_rate is the
        rate in tokens/second that the bucket will be refilled."""
        self.capacity = float(tokens)
        self._tokens = float(tokens)
        self.fill_rate = float(fill_rate)
        self.capacity2 = float(tokens2)
        self._tokens2 = float(tokens2)
        self.fill_rate2 = float(fill_rate2)

    def consume(self, tokens):
        if tokens <= self.tokens:
            self._tokens -= tokens
        else:
            if tokens <= self.tokens2:
                self._tokens2 -= tokens
            else:
                return False,self._tokens2,self._tokens
        return True,self._tokens2,self._tokens

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
    src1 = [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]
    src2 = [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]
    bucket = TokenBucket(cap, frate, cap2, frate2)
    f = open("D:/Pliki Studia/SEM5/SWUS/Projekt/dane.csv", "w")

    for x in range(0,30):
        if (src1[x]==1 and src2[x]==1):
            print ("consumed 1,1 = ", (iter_list(list(bucket.consumeboth(1,2)),f)))
            sleep(0.2)
        elif (src2[x]==1):
            print ("consumed 1 = ", (iter_list(list(bucket.consume(2)),f)))
            sleep(0.2)
        elif (src1[x]==1):
            print ("consumed 1 = ", (iter_list(list(bucket.consume(1)),f)))
            sleep(0.2)
        elif (src2[x]==0 and src1[x]==0):
            iter_list(list(get_both_tokens_nodelay(bucket)),f)
            sleep(0.2)
    f.close()

if __name__ == '__main__':
    
    starttest(5,0.25,10,0.25)

    """
    bucket = TokenBucket(80, 1) 
    print "tokens =", bucket.tokens
    print "consume(80) =", bucket.consume(80)
    print "consume(10) =", bucket.consume(10)

    print "tokens =", bucket.tokens

    print "tokens =", bucket.tokens
    print "consume(90) =", bucket.consume(90)
    print "tokens =", bucket.tokens
    """
