# User Guide Documentation: Contents

The user guide provides information and demonstrations on how to use the `datascribe` package using the logistic regression modelling of the NHS A&E synthetic dataset (NHS England, 2019).

* [01 Summary of Dataset](./01_summary_of_dataset.ipynb)

* [02 Feature Engineering](./02_feature_engineering_summaries.ipynb)

* [03 Making the Model](./03_making_the_model.ipynb)

* [04 Describing Analyses](./04_describing_analyses.ipynb)

* [05 Workflow Diagram](05_workflow_diagram.ipynb)

* [06 Exporting the Ouput](./06_exporting_output.ipynb)

A summary of every notebook is below.

## 01 Summary of Dataset

This notebook shows you how to:

* Load the example Emergency Department (ED) dataset
* Create a Scribe instance from `datascribe`
* View the summary information
* Produce summary tables as an image file or markdown table
* Remove unwanted output image files

## 02 Feature Engineering

This notebook shows you how to log the following preprocessing steps using the Scribe object:

* Imputing missing values
* Scaling categorical data which has an order
* Dummy coding categorical fields

## 03 Making the Model

This notebook shows you how to log the creation of a model using the Scribe object (currently only available for a logistic regression Stratified K fold with Grid Search CV at this version).

## 04 Describing Analyses

This notebook shows you how to create and log the following performance metrics and visuals:

* Mean Absolute Error
* Mean Squared Error
* R2 score
* Confusion matrix (visual)
* Precision, recall and f1 score
* Receiver operating characteristic (ROC) curve (visual)

## 05 Workflow Diagram

This notebook shows you how to produce a workflow diagram visual, utilising the `graphviz` package.

## 06 Exporting the Ouput

This notebook shows you how to export the log to a markdown (.md) or Word document (.docx) format.

## References

NHS ENGLAND. 2019. A&E Synthetic Data [Online]. Available: https://www.data.england.nhs.uk/dataset/a-e-synthetic-data/resource/81b068e5-6501-4840-a880-a8e7aa56890e [Accessed 15 November 2023].
