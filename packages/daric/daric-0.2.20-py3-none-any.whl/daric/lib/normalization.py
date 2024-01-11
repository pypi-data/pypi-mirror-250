import matplotlib
matplotlib.use('Agg')
import re, os, sys
import pandas as pd
import numpy as np
import pyBigWig
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.linear_model import HuberRegressor
warnings.simplefilter(action='ignore')
import typer
import pkgutil
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import calculation

def read_in_PIS(df):
    pcs = {} # {'chrom':{start:pc1}}
    for index, row in df.iterrows():
        chrom = row[0]
        start = row[1]
        if chrom not in pcs.keys():
            pcs[chrom] = {}
        pcs[chrom][start] = row[3]
    return pcs


def normalize(
    sample1_name: str = typer.Option(..., "--sample1", "-m", help="name of sample1, e.g. name of the cell-type"),
    sample2_name: str = typer.Option(..., "--sample2", "-n", help="name of sample2"),
    PIS1: str = typer.Option(..., "--sample1_PIS", "-p", help="the PIS track(s) for sample1. Multiple files, like replicates, can be separated by comma without space."),
    PIS2: str = typer.Option(..., "--sample2_PIS", "-q", help="the PIS track(s) for sample2. Multiple files, like replicates, can be separated by comma without space."),
    fraction: float = typer.Option(0.15, "--fraction", "-f", help="A value between 0 and 1. Genomic regions whose residual PIS locate in the top and bottom XX fraction are excluded in building the MAnorm model to infer the systematic scaling differences between the two samples."),    
    reso: int = typer.Option(..., "--reso", "-r", help="an integer representing the genomic resolution for compartment bins in the PIS track, in bp"),
    species: str = typer.Option(..., "--species", "-s", help="species (mm9, mm10, hg19, hg38)"),
    outDir: str = typer.Option("./", "--outdir", "-o", help="output directory")
    ):


    outname = sample1_name + '-vs-' + sample2_name

    # read in chromosome size information from file.
    try:
        chromSizeData = pkgutil.get_data("daric", "data/"+species+'_chrom.size.txt')
        chromSizes = calculation.read_in_chromsize(chromSizeData)
    except IOError:
        sys.exit(species+"_chrom.size.txt is not found. Please retry after adding this file to the data folder within daric.")
    del chromSizes['chrY']

    # initiate a dataframe to store the PIS
    outDF = pd.DataFrame()
    chroms = []
    starts = []
    ends = []
    for chrom in chromSizes.keys():
        num = chromSizes[chrom]//reso
        for i in range(num - 1):
            start = int(i * reso)
            end = int(start + reso)

            chroms.append(chrom)
            starts.append(start)
            ends.append(end)
    outDF['chrom'] = pd.Series(chroms)
    outDF['start'] = pd.Series(starts)
    outDF['end'] = pd.Series(ends)

    # read in the PIS for sample 1
    sample1s = PIS1.split(',')
    print("Reading in replicates for sample 1...")
    print(sample1s)
    for i in range(len(sample1s)):

        sample = sample1s[i]
        pisDF = pd.read_csv(sample, sep='\t', header=None)
        pis = read_in_PIS(pisDF)

        scores = []
        for index, row in outDF.iterrows():
            chrom = row['chrom']
            start = row['start']
            try:
                if start in pis[chrom].keys():
                    scores.append(pis[chrom][start])
                else:
                    scores.append('NA')
            except:
                scores.append('NA')
        outDF[sample1_name+'_rep'+str(i+1)] = pd.Series(scores)


    # read in the PIS for sample 2
    sample2s = PIS2.split(',')
    print("Reading in replicates for sample 2...")
    print(sample2s)
    for i in range(len(sample2s)):
        sample = sample2s[i]
        pisDF = pd.read_csv(sample, sep='\t', header=None)
        pis = read_in_PIS(pisDF)

        scores = []
        for index, row in outDF.iterrows():
            chrom = row['chrom']
            start = row['start']
            try:
                if start in pis[chrom].keys():
                    scores.append(pis[chrom][start])
                else:
                    scores.append('NA')
            except:
                scores.append('NA')
        outDF[sample2_name+'_rep'+str(i+1)] = pd.Series(scores)

    
    # get the average delta scores from replicates
    print("Working on the residual of PIS between samples...")
    outDF=outDF.replace('NA',np.nan).dropna(axis = 0, how = 'any')
    sample1_num = len(sample1s)
    sample2_num = len(sample2s)

    avgScores1 = outDF[sample1_name+'_rep1']
    if sample1_num > 1:
        for i in range(1, sample1_num):
            avgScores1 = avgScores1 + outDF[sample1_name+'_rep'+str(i+1)]
    avgScores1 = avgScores1/sample1_num
    outDF[sample1_name] = avgScores1

    avgScores2 = outDF[sample2_name+'_rep1']
    if sample2_num > 1:
        for i in range(1, sample2_num):
            avgScores2 = avgScores2 + outDF[sample2_name+'_rep'+str(i+1)]
    avgScores2 = avgScores2/sample2_num
    outDF[sample2_name] = avgScores2

    outDF['M'] = avgScores2 - avgScores1
    outDF['A'] = (avgScores2 + avgScores1)/2


    # define genomic regions as the background to extract the scaling relationship between the two samples.
    # here the regions whose "M" value is within the 15%-85% are selected as the background.
    lower_cut = outDF['M'].quantile(q=fraction)
    higher_cut = outDF['M'].quantile(q=1-fraction)
    m_values = np.array(outDF['M'])
    a_values = np.array(outDF['A'])
    mask = (m_values >= lower_cut) & (m_values <= higher_cut)

    # apply regression
    print("Building the MA model and write the normalized PIS files...")
    huber = HuberRegressor()
    huber.fit(a_values[mask].reshape(-1, 1), m_values[mask])
    intercept = huber.intercept_
    slope = huber.coef_[0]
    outDF['normed_M'] = outDF['M'] - (intercept + slope * outDF['A'])
    outDF.loc[:, ['chrom', 'start', 'end', sample1_name]].to_csv(outDir+'/'+outname+'_'+sample1_name+'_avg_PIS.bedGraph', sep='\t', index=False, header=False)
    outDF.loc[:, ['chrom', 'start', 'end', sample2_name]].to_csv(outDir+'/'+outname+'_'+sample2_name+'_avg_PIS_before-norm.bedGraph', sep='\t', index=False, header=False)
    outDF.loc[:, ['chrom', 'start', 'end', 'M']].to_csv(outDir+'/'+outname+'_deltaPIS.before-norm.bedGraph', sep='\t', index=False, header=False)
    outDF.loc[:, ['chrom', 'start', 'end', 'normed_M']].to_csv(outDir+'/'+outname+'_deltaPIS.bedGraph', sep='\t', index=False, header=False)
    outDF[sample2_name+'_after-norm'] = outDF[sample1_name] + outDF['normed_M']
    outDF.loc[:, ['chrom', 'start', 'end', sample2_name+'_after-norm']].to_csv(outDir+'/'+outname+'_'+sample2_name+'_avg_PIS_after-norm.bedGraph', sep='\t', index=False, header=False)
    outDF.to_csv(outDir+'/'+outname+'.txt', sep='\t', index=False)


    # statistical analyses. only works when there are more than two replicates in each condition.
    if sample1_num > 1 and sample2_num > 1:
        print("Statistical analysis...")

        delta1s = [] # list of within-condition differences for sample1
        for i in range(sample1_num):
            scores1 = outDF[sample1_name+'_rep'+str(i+1)]
            for j in range(sample1_num):
                scores2 = outDF[sample1_name+'_rep'+str(j+1)]
                if i != j:
                    deltas = scores1 - scores2
                    delta1s.append(deltas)

        delta2s = [] # list of within-condition differences for sample2
        for i in range(sample2_num):
            scores1 = outDF[sample2_name+'_rep'+str(i+1)]
            for j in range(sample2_num):
                scores2 = outDF[sample2_name+'_rep'+str(j+1)]
                if i != j:
                    deltas = scores1 - scores2
                    delta2s.append(deltas)

        bgDeltas = []
        for i in range(len(delta1s)):
            for j in range(len(delta2s)):
                bgDeltas.extend(list((delta1s[i] + delta2s[j])/2))

        mean = np.mean(bgDeltas)
        std = np.std(bgDeltas)

        sns.set(style='ticks', font_scale=1.6)
        plt.figure(figsize=(8,6))
        plt.hist(bgDeltas, bins=100, range=(-2.0,2.0), density=True, color='k')
        plt.xlabel("delta PIS")
        plt.title('mean='+str("{:.3f}".format(mean))+', std='+str("{:.3f}".format(std)))
        plt.savefig(outDir+'/'+outname+'_background_distribution_for_delta-PIS.png', dpi=300, bbox_inches = 'tight')

        pvalues = {}
        for index, row in outDF.iterrows():
            bgDist = scipy.stats.norm(mean,std)
            if row['normed_M'] > 0:
                p = -1 * np.log10(1 - bgDist.cdf(row['normed_M']))
            else:
                p = -1 * np.log10(bgDist.cdf(row['normed_M']))
            
            if p > 20:
                p = 20
            pvalues[index] = p
        outDF['p_value'] = pd.Series(pvalues)
        outDF.loc[:, ['chrom', 'start', 'end', 'p_value']].to_csv(outDir+'/'+outname+'_p-value.bedGraph', sep='\t', index=False, header=False)
    
    print("Done!")