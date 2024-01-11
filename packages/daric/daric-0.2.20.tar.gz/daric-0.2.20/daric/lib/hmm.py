import matplotlib
matplotlib.use('Agg')
import re, os, sys
import numpy as np
import scipy
from hmmlearn import hmm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import HTSeq
import pkgutil
warnings.simplefilter(action='ignore')
import typer
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import calculation


def runhmm(
    comparison: str = typer.Option(..., "--comparison", "-n", help="the name for the comparison"),
    deltaPIS_tracks: str = typer.Option(..., "--deltaPIS", "-f", help="the delta scores for different comparisons. Multiple files should be separated by comma"),
    reso: int = typer.Option(..., "--reso", "-r", help="an integer representing the genomic resolution for compartment bins in the PIS track, in bp"),
    species: str = typer.Option(..., "--species", "-s", help="species (mm9, mm10, hg19, hg38)"),
    outDir: str = typer.Option("./", "--outdir", "-o", help="output directory")
    ):

    samples = deltaPIS_tracks.split(',')
    print(samples)

    nStates = 4

    # read in chromosome size information from file.
    try:
        chromSizeData = pkgutil.get_data("daric", "data/"+species+'_chrom.size.txt')
        chromSizes = calculation.read_in_chromsize(chromSizeData)
        chroms = list(chromSizes.keys())
    except IOError:
        sys.exit(species+"_chrom.size.txt is not found. Please retry after adding this file to the data folder within daric.")
    chroms.remove('chrY')


    pc1s = []
    lengths = []
    pcDFs = []
    for sample in samples:
        pcDF = pd.read_csv(sample,sep="\t", header=None, names=['chrom', 'start', 'end', 'delta-score'])
        pcDF['sample'] = sample
        pcDFs.append(pcDF)

        for chrom in chroms:
            if chrom in list(pcDF['chrom']):
                chromPC1s = [[i] for i in list(pcDF[pcDF['chrom'] == chrom]['delta-score'])]
                pc1s += chromPC1s
                lengths.append(len(chromPC1s))


    model = hmm.GaussianHMM(n_components=nStates, covariance_type="full", n_iter=500)

    model.fit(pc1s, lengths)
    print("Mean delta PIS values for each state:")
    print(model.means_)

    stateMeans = pd.DataFrame({'State': list(range(nStates)), 'Mean_signal': list(model.means_[:,0])})
    stateMeans.set_index('State', drop=True, inplace=True)
    stateMeans.sort_values(by='Mean_signal', ascending=True, inplace=True)


    if nStates == 4: 
        Types = dict(zip(list(stateMeans.index), ['Strong-', 'Weak-', 'Weak+', 'Strong+']))
        state_colors = {'Strong+':'#d7191c', 'Strong-':'#2b83ba', 'Weak+':'#fdae61', 'Weak-':'#abdda4'}
    elif nStates == 2:
        Types = dict(zip(list(stateMeans.index), ['Decreased', 'Increased']))
        state_colors = {'Increased':'#d7191c', 'Decreased':'#2b83ba'}
    print(Types)
    print("State emission matrix and figure are saved to the output directory...")
    stateMeans['Type'] = pd.Series(Types)
    stateMeans.set_index('Type', inplace=True)
    stateMeans.to_csv(outDir+"/"+comparison+"_Model_HMM="+str(nStates)+".emission.txt", sep='\t')
    
    # plot the emission matrix
    sns.set(style="whitegrid", font_scale=1.8)
    plt.figure(figsize=(3,6))
    sns.heatmap(stateMeans,annot=True,vmin=-0.5, vmax=0.5, fmt=".2f", cmap="coolwarm")
    plt.yticks(rotation=0)
    plt.ylabel('')
    plt.xlabel('')
    plt.title('Emission matrix')
    plt.savefig(outDir+"/"+comparison+"_Model_HMM="+str(nStates)+"_states.emission.png", dpi=300, bbox_inches = "tight")
    plt.savefig(outDir+"/"+comparison+"_Model_HMM="+str(nStates)+"_states.emission.svg", dpi=300, bbox_inches = "tight")

    # get the transition matrix
    stateNames = [Types[k] for k in sorted(Types.keys())]
    TransMat = pd.DataFrame(model.transmat_, index=stateNames, columns=stateNames)
    TransMat = TransMat.loc[['Strong-', 'Weak-', 'Weak+', 'Strong+'], ['Strong-', 'Weak-', 'Weak+', 'Strong+']]
    print("State transition probability matrix and figure are saved to the output directory...")
    print(TransMat)
    TransMat.to_csv(outDir+"/"+comparison+"_Model_states_HMM="+str(nStates)+".transition.txt", sep='\t')
    
    # plot the transition matrix
    plt.figure(figsize=(7,6))
    sns.heatmap(TransMat,annot=True,vmin=0, vmax=1.0, cmap="Purples",fmt=".2f")
    plt.yticks(rotation=0)
    plt.title('Transition probability')
    plt.savefig(outDir+"/"+comparison+"_Model_HMM="+str(nStates)+"_states.transition.png", dpi=300, bbox_inches = "tight")
    plt.savefig(outDir+"/"+comparison+"_Model_HMM="+str(nStates)+"_states.transition.svg", dpi=300, bbox_inches = "tight")


    states_int = model.predict(pc1s, lengths)
    mpcDF = pd.concat(pcDFs, ignore_index=True)


    dfs = []
    for sample in samples:
        pcDF = mpcDF[mpcDF['sample'] == sample]
        for chrom in chroms:
            chromDF = pcDF[pcDF['chrom'] == chrom]
            chromDF.sort_values(by='start', inplace=True, ascending=True)
            dfs.append(chromDF)

    df = pd.concat(dfs, ignore_index=True)
    df.reset_index(drop=True, inplace=True)
    df['state'] = pd.Series(states_int)

    # write the interpreted states to bed file in fixed bedgraph format
    for sample in samples:
        name = sample.strip('_deltaPIS.bedGraph').split('/')[-1]
        outfile = open(outDir+'/'+name+"_HMM="+str(nStates)+".fixed-step.bed", 'w')
        tdf = df[df['sample'] == sample]
        state_counts = {}
        for index, row in tdf.iterrows():
            state_color = state_colors[Types[row['state']]]
            if Types[row['state']] not in state_counts.keys():
                state_counts[Types[row['state']]] = 0
            state_counts[Types[row['state']]] += 1
            eles = [row['chrom'], str(row['start']), str(row['end']), str(Types[row['state']]), str('0.0'), str('.'), str(row['start']), str(row['end']), state_color]
            outline = '\t'.join(eles)+'\n'
            outfile.write(outline)
        outfile.close()
        
        outfile1 = open(outDir+'/'+name+'_state-coverage_HMM='+str(nStates)+".txt", 'w')
        for state in state_counts.keys():
            outline = state + '\t' + str(state_counts[state]/sum(state_counts.values())) + '\n'
            outfile1.write(outline) 
        outfile1.close()

        # plot the state coverage matrix
        print("State coverage matrix and figures are saved to the output directory...")
        covDF = pd.read_csv(outDir+'/'+name+'_state-coverage_HMM='+str(nStates)+".txt", sep='\t', header=None, index_col=0)
        covDF = covDF.loc[['Strong-', 'Weak-', 'Weak+', 'Strong+'], :]
        sns.set(style="whitegrid", font_scale=1.8)
        plt.figure(figsize=(3,6))
        sns.heatmap(covDF,annot=True,vmin=0, vmax=0.5, cmap="Oranges")
        plt.yticks(rotation=0)
        plt.title('State coverage')
        plt.xlabel('')
        plt.ylabel('')
        plt.savefig(outDir+'/'+name+'_state-coverage_HMM='+str(nStates)+".png", dpi=300, bbox_inches = "tight")
        plt.savefig(outDir+'/'+name+'_state-coverage_HMM='+str(nStates)+".svg", dpi=300, bbox_inches = "tight")


        # write the interpreted states to bed file in variable-step bedgraph format
        tempDF = pd.read_csv(outDir+'/'+name+"_HMM="+str(nStates)+".fixed-step.bed", sep='\t', header=None)
        tempDF[tempDF[3] == 'Strong-'].to_csv("Strong-.bed", sep='\t', header=False, index=False)
        tempDF[tempDF[3] == 'Strong+'].to_csv("Strong+.bed", sep='\t', header=False, index=False)
        command = "bedtools merge -d 1 -i Strong-.bed > "+name+"_HMM="+str(nStates)+".Strong-.bed"
        os.system(command)
        command = "bedtools merge -d 1 -i Strong+.bed > "+name+"_HMM="+str(nStates)+".Strong+.bed"
        os.system(command)


        # statistical analysis

        # p-value tracks are assumed to be in the same directory as the deltaPIS tracks. If not, need to rearrange.
        pvalueTrack = sample.split('_deltaPIS')[0]+'_p-value.bedGraph'
        if not os.path.exists(pvalueTrack):
            print(pvalueTrack+" is not found. If p-value track exists, please make sure it is in the same directory as the delta PIS track.")
            print("statistical analysis skipped...")
            command = "mv "+name+"_HMM="+str(nStates)+".Strong+.bed "+outDir
            os.system(command)
            command = "mv "+name+"_HMM="+str(nStates)+".Strong-.bed "+outDir
            os.system(command)
            os.system("rm Strong+.bed")
            os.system("rm Strong-.bed")
        else:
            print("statistical analysis on "+name+"...")
            pDF = pd.read_csv(pvalueTrack, sep='\t', header=None)
            pBins = {} #{'chrom':{iv1:p_value1}}
            for index, row in pDF.iterrows():
                chrom = row[0]
                start = row[1]
                end = row[2]
                p_value = row[3]
                iv = HTSeq.GenomicInterval(chrom, start, end, '.')
        
                if chrom not in pBins.keys():
                    pBins[chrom] = {}

                pBins[chrom][iv] = p_value
            for Type in ['Strong+', 'Strong-']:
                sigdf = pd.read_csv(name+"_HMM="+str(nStates)+"."+Type+".bed", header=None, sep='\t')
                outfile = open(outDir+'/'+name+"_HMM="+str(nStates)+"."+Type+".bed", 'w')
                for index, row in sigdf.iterrows():
                    chrom = row[0]
                    start = row[1]
                    end = row[2]
                    num = (end - start)//reso
                    scores = []
                    for i in range(num):
                        iv = HTSeq.GenomicInterval(chrom, start+i*reso, start+i*reso+reso, '.')
                        if iv in pBins[chrom].keys():
                            scores.append(pBins[chrom][iv])
                    if np.max(scores) >= 2:
                        outline = '\t'.join([chrom, str(start), str(end)])
                        outfile.write(outline+'\n')
                outfile.close()
            os.system("rm Strong+.bed")
            os.system("rm Strong-.bed")
            os.system("rm "+name+"_HMM="+str(nStates)+".Strong+.bed")
            os.system("rm "+name+"_HMM="+str(nStates)+".Strong-.bed")
    print("Done!")
