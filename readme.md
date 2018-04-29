# Glossary Term Extraction from the CrowdRe Dataset

This is the code used to extract and analyze glossary term candidates from the CrowdRE dataset in
the conference paper proposal by Gemkow, Conzelmann, Hartig and Vogelsang.

The file "Extended Report.pdf" presents an extended version of our findings that also discusses the effects of varying elements of our processing pipelines on the extracted glossary term candidates.

The paper, and this code, builds on the CrowdRE dataset:
P. K. Murukannaiah, N. Ajmeri, and M. P. Singh, “The smarthome crowd requirements dataset,” https://crowdre.github.io/murukannaiah-smarthome-requirements-dataset/ , Apr. 2017.

## Replicating the analysis

0. Install the prerequisite packages nltk (for language processing) and openpyxl (for Excel export) in the Python environment that you will be using.
Please note that nltk needs to be installed including the WordNet corpus; it may be necessary to execute "nltk.download('wordnet')" in the Python shell
after downloading the package.

1. Download or clone this repository to your local machine.

2. Download the csv version of the dataset from the url mentioned above and place the requirements.csv file in the data folder.

3. Execute the src/analysis.py file in a Python 3 interpreter

The results of the analysis will be output to the console.

## How the analysis works

The main workhorse of the analysis script is the function glossary_extraction in the file pipeline.py. Through its parameters, this function allows
to vary each step in the pipeline along the alternatives described in the paper. In general, for each comparison, analysis.py runs this function twice
with different pipeline configurations and then compares the outputs.

NB: We do not focus on the immedate effects of changing a pipeline step (i.e. the words directly removed by a filter), but on the change of the ultimate
pipeline output caused by changing a pipeline step. This is important since changes in the middle of the pipeline may have important repercussions on
later steps (e.g. when ommitting stemming, many important concepts are later removed by the statistical filter because each individual form occurs to
rarely in the dataset to fulfill the frequency criterion).

## Re-using intermediate results

Training a PoS tagger and PoS-tagging the requirements are computationally expensive steps that should not be re-run every time an analysis in the
later stages of the pipeline is changed. Therefore, both the tagger itself and the tagged requirements are saved as pickle files in the temp folder.
As a default, the glossary_extraction function starts with the PoS-tagged requirements. By setting the tag_mode parameter, you can enforce a new
PoS-tagging using the existing tagger, or training and applying a new tagger from scratch. If you want to analyse changes in the very early pipeline
steps (e.g. tokenization), this is necessary since the pre-computed tagged requirements will not reflect the consequences of such changes.

Note that the temp folder also contains an intermediate result from analyzing the WordNet corpus for comparison (filter_index.pickle). It should
not be necessary to re-run this benchmark creation, although the code to do so is included in indexfilter.py for completeness.