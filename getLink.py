#!/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------------------
# Function: extract link file for circos to visualization by given gff and collinear file generated by MCScanX.
# -------------------------------------------------------------------------------------------------------------
import getopt
import sys
import re


def getoptfromcmd():
    opts, args = getopt.getopt(sys.argv[1:], "-c:-g:-o:")
    for opt_name, opt_value in opts:
        if opt_name == "-c":
            collinearpath = opt_value
        if opt_name == "-g":
            gffpath = opt_value
        if opt_name == "-o":
            linkpath = opt_value
    return collinearpath, gffpath, linkpath


def getlink(collinearpath, gffpath, linkpath):
    postable = {}
    with open(gffpath, "rt") as fp:
        for rec in fp:
            chrname = rec.strip().split("\t")[0]
            genename = rec.strip().split("\t")[1]
            start = rec.strip().split("\t")[2]
            end = rec.strip().split("\t")[3]
            postable[genename] = [chrname, start, end]
    linklist = []
    with open(collinearpath, "rt") as fp:
        for line in fp:
            if not line.startswith("#"):
                gene1_chr = postable[re.split("\s+", line)[3]][0]
                gene1_start = postable[re.split("\s+", line)[3]][1]
                gene1_end = postable[re.split("\s+", line)[3]][2]
                gene2_chr = postable[re.split("\s+", line)[4]][0]
                gene2_start = postable[re.split("\s+", line)[4]][1]
                gene2_end = postable[re.split("\s+", line)[4]][2]
                linklist.append([gene1_chr, gene1_start, gene1_end, 
                        gene2_chr, gene2_start, gene2_end])
    with open(linkpath, "wt") as fp:
        for link in linklist:
            fp.write(" ".join(link)+"\n")

            
if __name__ == '__main__':
   collinearpath, gffpath, linkpath = getoptfromcmd()
   getlink(collinearpath, gffpath, linkpath)
