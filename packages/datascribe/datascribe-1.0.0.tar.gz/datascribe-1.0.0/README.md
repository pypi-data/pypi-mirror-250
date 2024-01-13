# datascribe: useful tools to help you document and describe data processing and modelling

datascribe has been developed to assist data scientists in documenting and describing data analysis, processing and modelling.

## Vision for datascribe

1. Assist users in documenting the dataset they are using.

2. Assist users in documenting the preprocessing and subsequent analysis they perform on datasets.

3. Provide summary text, images and tables in an editable format (markdown and Microsoft Word) tool.

4. Help users document research and analyses well so that it is transparent and repeatable.

## Features:

1. Creation of basic summary paragraphs with supporting markdown tables or table images to describe initial dataset information.

2. Implementation of key feature engineering tools from `sklearn` in tandem with producing a log of steps taken to process and analyse the dataset.

3. Ability to produce a workflow diagram via `graphviz` to help visualise the data processing and modelling workflow.

## How to explore datascribe



## Installing the virtual environment

Details of the conda virtual environment are available here: `binder/environment.yml`

Open the repo in a terminal (Mac/Linux) or anaconda prompt (Windows)

Navigate to the correct directory.

Create the environment with the following command:

```bash
conda env create -f binder/environment.yml
```
     
Activate the environment with the following command:

```bash
conda activate datascribe
```  

It is strongly recommended that you install a conda environment to avoid dependency conflicts. 

### Dependencies

This project relies on the following external dependencies:

- [Graphviz](https://graphviz.gitlab.io/download/): Used for creating visualizations in the workflow.

### Installing Dependencies

#### Graphviz

Make sure you have Graphviz installed on your system. You can download it from the [official Graphviz website](https://graphviz.gitlab.io/download/) or install it using your package manager:

##### Linux (e.g., Ubuntu)

```bash
sudo apt-get install graphviz
```

