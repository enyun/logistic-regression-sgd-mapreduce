#!/usr/bin/env python

import collections, math, sys, json, urllib2, os

def main():
    W = collections.defaultdict(float)
    model = urllib2.urlopen(os.environ['MODEL'])
    for f, w in json.loads(model.readline().strip()).items():
        W[f] = w
    for line in sys.stdin:
        x = json.loads(line)
        sigma = sum([W[j] * x["features"][j] for j in x["features"].keys()])
        p = 1. / (1. + math.exp(-sigma)) if -100. < sigma else sys.float_info.min
        prediction = 1 if 0. < sum([W[j] * x["features"][j] for j in x["features"].keys()]) else 0
        print '%d\t%d' % (prediction, x["class"])
    
if __name__ == '__main__':
    main()
