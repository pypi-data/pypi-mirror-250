import re, os, sys
import pandas as pd
import numpy as np
import HTSeq
import scipy
import scipy.ndimage
import pyBigWig
from scipy.optimize import curve_fit
import math
import warnings
import typer
warnings.simplefilter(action='ignore')
import pkgutil
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def read_in_gaps(gapData):
    """
    Read in the gaps information from the gap bed file.
    input: gapData, binary strings returned from pkgutil.get_data
    return: gaps interval, organized by chrom

    """
    gaps = {} #{chrom:[gap1, gap2,...]}
    lines = gapData.decode().split('\n')
    for line in lines:
        sline = line.strip().split('\t')
        chrom = sline[0]
        start = int(sline[1])
        end = int(sline[2])
        iv = HTSeq.GenomicInterval(chrom, start, end, '.')
        if chrom not in gaps.keys():
            gaps[chrom] = []
        gaps[chrom].append(iv)
    return gaps

def read_in_chromsize(chromSizeData):
    """
    Read in the chromosome size information from the chrom-size file.
    Input: chromSizeData
    Return: chromsizes = {'chrXX':int}
    """
    chromSizes = {} # {'chrXX':int}
    lines = chromSizeData.decode().split('\n')
    for line in lines:
        sline = line.strip().split('\t')
        chrom = sline[0]
        chromSize = int(sline[1])
        chromSizes[chrom] = chromSize
    return chromSizes



def read_in_PC1(pcPath, gaps, chromSizes, reso):
    """
    Read in the PC1 bigwig files.
    Return: pcs[iv] = 'A' or 'B'
    """
    pc1bw = pyBigWig.open(pcPath)

    # binning the genome and initiate the pc1 values for genome
    pcs1 = {} # pcs1={'iv':'A' or 'B' or 0}

    if gaps != None:
        for chrom in list(set(chromSizes.keys()).intersection(dict(pc1bw.chroms()).keys())):
            numBins = chromSizes[chrom]//reso
            for i in range(numBins):
                iv = HTSeq.GenomicInterval(chrom, i*reso, i*reso+reso, '.')
                overlapped = 0
                if chrom in gaps.keys():
                    for gap in gaps[chrom]:
                        if iv.overlaps(gap):
                            overlapped = 1
                            break
                if overlapped == 0:
                    try:
                        pc1value = pc1bw.stats(chrom, i*reso, i*reso+reso, type='mean')[0]
                    except:
                        pc1value = 0
                    if pc1value is not None:
                        if pc1value > 0:
                            pcs1[iv] = 'A'
                        else:
                            pcs1[iv] = 'B'
    else:
        for chrom in list(set(chromSizes.keys()).intersection(dict(pc1bw.chroms()).keys())):
            numBins = chromSizes[chrom]//reso
            for i in range(numBins):
                iv = HTSeq.GenomicInterval(chrom, i*reso, i*reso+reso, '.')
                try:
                    pc1value = pc1bw.stats(chrom, i*reso, i*reso+reso, type='mean')[0]
                except:
                    pc1value = 0
                if pc1value is not None:
                    if pc1value > 0:
                        pcs1[iv] = 'A'
                    else:
                        pcs1[iv] = 'B'
    return pcs1


def initiate_array_for_interactions(pcs1):
    """
    Use the genomic intervals with PC1 values to initiate a dictionary to store 
    the interactions for preferential score calculation.
    """
    scores = {} # {iv:{'A':[], 'B':[]}}
    for iv in pcs1.keys():
        scores[iv] = {}
        scores[iv]['A'] = []
        scores[iv]['B'] = []
    return scores

def read_in_oe_matrix(mtrPrefix, chrom, reso, pcs1, scores):

    """
    Read in the oe matrix to fill the values of scores from "initiate_array_for_interactions".
    """
    mtrFile = mtrPrefix+'/'+chrom+'.txt'

    file_exists = os.path.exists(mtrFile)

    if file_exists:
        print('Working in '+chrom+'...')

        mtr = open(mtrFile, 'r')
        for line in mtr:
            sline = line.strip().split('\t')
            bin1 = int(sline[0])
            bin2 = int(sline[1])
            oe = float(sline[2])

            iv1 = HTSeq.GenomicInterval(chrom, bin1, bin1 + reso, '.')
            iv2 = HTSeq.GenomicInterval(chrom, bin2, bin2 + reso, '.')

            if iv1 in pcs1.keys() and iv2 in pcs1.keys():
                Type1 = pcs1[iv1]
                Type2 = pcs1[iv2]
                if iv1 in scores.keys() and iv2 in scores.keys():
                    scores[iv1][Type2].append(oe)
                    scores[iv2][Type1].append(oe)
                if iv1 in scores.keys() and iv2 not in scores.keys():
                    scores[iv1][Type2].append(oe)
                if iv2 in scores.keys() and iv1 not in scores.keys():
                    scores[iv2][Type1].append(oe)
        mtr.close()
    else:
        print(chrom+".txt file does not exist in "+mtrPrefix+". Skipping..." )
    return scores

def count_bins_in_each_compartment(pcs1):
    """
    Calculate the number of bins for A and B compartment for each chromosome
    """
    numbers = {}
    for iv in pcs1.keys():
        chrom = iv.chrom
        if chrom not in numbers.keys():
            numbers[chrom] = {}
            numbers[chrom]['A'] = 0
            numbers[chrom]['B'] = 0
        if pcs1[iv] == 'A':
            numbers[chrom]['A'] += 1
        elif pcs1[iv] == 'B':
            numbers[chrom]['B'] += 1
    return numbers

def gauss(x,mu,sigma,A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)


def calculate(
    sample: str = typer.Option(..., "--name", "-n", help="sample names used for output"),
    pcPath: str = typer.Option(..., "--pc1", "-p", help="the PC1 bigwig file for compartments"),
    mtrPrefix: str = typer.Option(..., "--hic", "-m", help="the directory with the o/e interaction matrice in sparse format. Note that it has to be the output from juicer dump."),
    reso: int = typer.Option(..., "--reso", "-r", help="the genomic resolution (in bp) for compartment bins and hic file"),
    species: str = typer.Option(..., "--species", "-s", help="species (mm9, mm10, hg19, hg38)"),
    outDir: str = typer.Option("./", "--outdir", "-o", help="path for output directory")
    ):

    # read in chromosome size information from file.
    try:
        chromSizeData = pkgutil.get_data("daric", "data/"+species+'_chrom.size.txt')
        chromSizes = read_in_chromsize(chromSizeData)
        chroms = list(chromSizes.keys())
    except IOError:
        sys.exit(species+"_chrom.size.txt is not found. Please retry after adding this file to the data folder within daric.")
    chroms.remove('chrY')

    # read in the genome gap information
    try:
        gapData = pkgutil.get_data("daric", "data/"+species+'_gap.bed')
        gaps = read_in_gaps(gapData)
    except IOError:
        gaps = None
        print(species+"_gap.bed file is not found. Continue without excluding the gap regions...")

    # create the output directory if it is not existed.
    if not os.path.isdir(outDir):
        os.mkdir(outDir)

    pcs1 = read_in_PC1(pcPath, gaps, chromSizes, reso)
    scores = initiate_array_for_interactions(pcs1)

    for chrom in chroms:
        scores = read_in_oe_matrix(mtrPrefix, chrom, reso, pcs1, scores)

    numbers = count_bins_in_each_compartment(pcs1)
    print('Writing the raw PIS track...')
    outfile = open(outDir+'/'+sample+'_PIS_raw.bedGraph', 'w')
    for iv in scores.keys():
        if len(scores[iv]['A']) > 0 and len(scores[iv]['B']) > 0:
            a = np.sum(pd.Series(scores[iv]['A']).dropna())/numbers[iv.chrom]['A']
            b = np.sum(pd.Series(scores[iv]['B']).dropna())/numbers[iv.chrom]['B']
            score = np.log2(a) - np.log2(b)

            if not math.isnan(score) and not math.isinf(score):
                outline = '\t'.join([iv.chrom, str(iv.start), str(iv.end), str(score)])
                outfile.write(outline+'\n')
    outfile.close()


    # smooth the signal
    print("Writing the smoothed PIS track...")
    df = pd.read_csv(outDir+'/'+sample+'_PIS_raw.bedGraph', sep='\t', header=None, names=['chrom', 'start', 'end', 'score'])
    dfs = []
    for chrom in chroms:
        chromDF = df[df['chrom'] == chrom]
        if chromDF.shape[0] > 0:
            print("Smoothing PIS data on "+chrom+" ...")
            chromDF.sort_values(by='start', ascending=True, inplace=True)
            chromDF.reset_index(drop=True, inplace=True)
            rawScores = np.array(chromDF['score'])
            chromDF['smoothed_score'] = pd.Series(scipy.ndimage.gaussian_filter1d(rawScores, sigma=1, mode='reflect', cval=0.0))
            dfs.append(chromDF)
    df = pd.concat(dfs, ignore_index=True)
    df.loc[:, ['chrom', 'start', 'end', 'smoothed_score']].to_csv(outDir+'/'+sample+'_PIS_smoothed.bedGraph', sep='\t', header=False, index=False)

    print("Done!")