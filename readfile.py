#coding = 'utf-8'
import sys


filename = "data/sichuancaiguan.txt"
f = open(filename,'r')
while True:
    line = f.readline().strip('\n')
    if line:
        print line
    else:
        break

