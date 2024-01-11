# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daric', 'daric.data', 'daric.lib']

package_data = \
{'': ['*']}

install_requires = \
['HTSeq>=0.12.4,<0.13.0',
 'hmmlearn>=0.2.6,<0.3.0',
 'matplotlib==3.3.4',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyBigWig>=0.3.18,<0.4.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.6.2,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['daric = daric.main:app']}

setup_kwargs = {
    'name': 'daric',
    'version': '0.2.20',
    'description': 'DARIC, a computational framework to find quantitatively differential compartments from Hi-C data',
    'long_description': '<div align="center">\n\n  <img src="img/daric_logo.png" alt="logo" width="300" height="auto" />\n  <h1>DARIC is just published at BMC Genomics! See more details [here](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-023-09675-w) </h1>\n  <p>\n    A computational framework to find <span style="color:red"> ***quantitatively***</span> differential compartments between Hi-C datasets\n  </p>\n\n[![version](https://img.shields.io/badge/daric-v0.2.18-brightgreen)](https://img.shields.io/badge/daric-v0.2.18-brightgreen)\n[![Downloads](https://pepy.tech/badge/daric)](https://pepy.tech/project/daric)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n\n<div align="left">\n\n\n`DARIC`, or Differential Analysis for genomic Regions\' Interaction with Compartments, is a computational framework to identify the quantitatively differential compartments from Hi-C-like data. For more details about the design and implementation of the framework, please check our paper published at [BMC Genomics](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-023-09675-w).\n\n# About DARIC\n## 1. Preferential Interaction Score\nPIS is used for measuring the compartmentalization type and strength for a genomic bin at a selected resolution. PIS is defined as the log-transformed ratio of the average interactions with compartments A to B.\n\n<img src="img/PreferentialScore.png" alt="PIS" width="800" height="auto" />\n\n## 2. DARIC pipeline\nDARIC includes the following four steps to identify genomic domains with quantitatively differential compartmentalization changes.\n\n1. Calculation of the genome-wide PIS for the samples;\n2. Smoothing of PIS in each sample to remove technical noises;\n3. Normalization.\n4. Identifying differential domains by a Hidden Markov Model and performing statistical analyses. \n\n<img src="img/PIS_comparison_method_horizontal.png" alt="pipeline" width="800" height="auto" />\n\n\n# Installation\n1. Install with `pip`.\n\t+ `$ pip install daric`\n\t+ To test the installation, please type `$ daric --help` in shell to see if help messages pop out.\n\n# Required files to start a DARIC analysis\nIt requires two types of information to start a DARIC analysis: (1) Compartment type information, i.e. PC1 values from [HOMER](http://homer.ucsd.edu/homer/interactions2/HiCpca.html) or eigenvectors from [Juicer](https://github.com/aidenlab/juicer). (2) Normalized contact matrice for each chromosome resulted from juicertools. \n\n## 1. PC1 track or eigenvectors\nThe compartment type information can be the PC1 values or eigenvalues for each genomic bin in .bigwig format. By default, a positive value represents that the associated genomic bin is in active compartment A, and a negative value represents inactive compartment B. \n\n## 2. Normalized contact matrice\nDARIC requires to take the OE normalized contact matrice for each individual chromasome from juicertools. Specifically, these contact matrice can be obtained by the following command. \n\n```\njava -jar juicer_tools.1.7.5_linux_\nx64_jcuda.0.8.jar dump oe KR sample.hic $i $i BP 50kb sample_OE_matrix\n# i is chromsome number, please see details in the juciertools github page. \n```\nThe normalized contact matrix will be in the `sample_OE_matrix` folder. The path of `sample_OE_matrix` will be used in the PIS calculation command below.\n\n\n# Usage\n`DARIC` is composed of three commands: `calculate`, `normalize`, and `runhmm`. \n\n## 1. Calculation of PIS\n---\nPIS, or Preferential Interaction Score, is a metric that we used to evaluate the relative interaction strength between the A and B compartments. `calculate` is the command to calculate the PIS:\n\n\n\n```\nUsage: daric calculate [OPTIONS]\n\nOptions:\n  -n, --name TEXT     sample names used for output  [required]\n  -p, --pc1 TEXT      the PC1 bigwig file for compartments  [required]\n  -m, --hic TEXT      the directory with the o/e interaction matrice in sparse format. Note that it has to be the output from juicer dump.  [required]\n  -r, --reso INTEGER  the genomic resolution (in bp) for compartment bins and hic file  [required]\n  -s, --species TEXT  species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT   path for output directory  [default: ./]\n  --help              Show this message and exit.\n```\nPlease note that the resolution of the contact matrice in `-m` parameter has to be the same as the value assigned by `-r`. The resolution or bin size in the PC1 track (i.e. `-p`) can be different from the assigned resolution. Resolution of the output PIS is determined by `-r`.\n\n## 2. Normalization of two PIS tracks\n---\nWe borrowed the idea of MAnorm, a normalization method designed for normalizing ChIP-seq datasets, to normalize the PIS data. `normalize` is the command for this task:\n\n```\nUsage: daric normalize [OPTIONS]\n\nOptions:\n  -m, --sample1 TEXT      name of sample1, e.g. name of the cell-type\n                          [required]\n\n  -n, --sample2 TEXT      name of sample2  [required]\n  -p, --sample1_PIS TEXT  the PIS track(s) for sample1. Multiple files, like\n                          replicates, can be separated by comma without space.\n                          [required]\n  -q, --sample2_PIS TEXT  the PIS track(s) for sample2. Multiple files, like\n                          replicates, can be separated by comma without space.\n                          [required]\n  -f, --fraction FLOAT    A value between 0 and 1. Genomic regions whose\n                          residual PIS locate in the top and bottom XX\n                          fraction are excluded in building the MAnorm model\n                          to infer the systematic scaling differences between\n                          the two samples.  [default: 0.15]\n\n  -r, --reso INTEGER      an integer representing the genomic resolution for\n                          compartment bins in the PIS track, in bp  [required]\n\n  -s, --species TEXT      species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT       output directory  [default: ./]\n  --help                  Show this message and exit.\n```\n\n## 3. Identification of differential comparments\n`runhmm` is the command to identify the quantitatively differential compartments and perform statistical analyses. \n\n```\nUsage: daric runhmm [OPTIONS]\n\nOptions:\n  -n, --comparison TEXT  the name for the comparison  [required]\n  -f, --deltaPIS TEXT    the delta scores for different comparisons. Multiple\n                         files should be separated by comma  [required]\n\n  -r, --reso INTEGER     an integer representing the genomic resolution for\n                         compartment bins in the PIS track, in bp  [required]\n\n  -s, --species TEXT     species (mm9, mm10, hg19, hg38)  [required]\n  -o, --outdir TEXT      output directory  [default: ./]\n  --help                 Show this message and exit.\n\n```\n# Citation\nIf you find DARIC useful in your research, please cite our paper [here](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-023-09675-w).',
    'author': 'Yan Kai',
    'author_email': 'smilekai@gwmail.gwu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
