'''
Contains the Scribe object for datascribe.

'''

from datascribe.workflow import Workflow
from datascribe.outputs import (convert_md_to_docx,
                                tidy_up_images)
from datascribe.summary_stats import Summary_stats
from urllib.parse import quote
import os
import numpy as np
from datascribe.feature_engineering import Preprocess
from datascribe.model import Model
from datascribe.metrics import Metrics


class Scribe:
    '''
    Class which holds the log of steps
    '''
    def __init__(self, initial_df, dir, dataset_name='dataset',
                 row_descriptor=("row", "rows"),
                 col_descriptor=("field", "fields")):
        '''
        Initiator method for Scribe.

        Parameters:
        ----------
        initial_df: pd.Dataframe
            Initial dataset being used in analysis.

        dir: str
            directory path to folder to use for output of any image
            files and final .md or .docx file

        dataset_name: str (default: 'dataset')
            string variable containing a name for the dataset.

        row_descriptor: tuple (default: ("row", "rows"))
            A string tuple which provides the singular and plural term
            in which to describe the rows.  This is to personalise the
            output.

        col_descriptor: tuple (default: ("col", "cols"))
            A string tuple which provides the singular and plural term
            in which to describe the columns.  This is to personalise
            the output.

        '''
        self.dir = dir
        self.row_descriptor = row_descriptor
        self.col_descriptor = col_descriptor
        self.dataset_name = dataset_name
        self.column_mapping = None
        # stores any text commentary
        self.commentary_loc = {}
        # stores the location of any image files
        self.visuals_loc = {}
        # summary_stats class
        self.summaries = Summary_stats(self, initial_df)
        # adding preprocessing as composition
        self.preprocessing = Preprocess()
        # adding model as composition
        self.model = Model()
        # adding metrics as composition
        self.metrics = Metrics(self)
        # workflow object to create hold workflow image creation aspects
        self.workflow = Workflow(self)

        # create self.dir if not already existing
        self.make_dir()

    def make_dir(self):
        '''
        Makes self.dir directory if it does not exist already.

        '''
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            print(f"Directory '{self.dir}' created.")
        else:
            print(f"Directory '{self.dir}' already exists.")

    def clean_up_images(self):
        '''
        Cleans up any images created for the log.

        '''
        # location of image folder for this class
        img_dir = f"{self.dir}/images"
        # use method in outputs to remove folder and its contents
        tidy_up_images(self, img_dir, output_img_files=False)

    def output_process(self, file_name,
                       title='Data Processing Summary', file_type='md',
                       output_img_files=True):
        '''
        Outputs the file.

        Parameters:
        ----------
        file_name: string
            Name for main output file (excluding file extension).

        title: string (default: Data Processing Summary)
            Main heading for the main output file

        file_type: string (default: 'md')
            Specifies the file type to export final document.

        output_img_files: boolean (default: True)
            Indicates whether to remove separate image files

        '''
        # variable for md filename (can't store in output folder in
        # output folder's current location)
        md_file_path = f"{self.dir}/{file_name}.md"

        # image folder location depending on output type
        if file_type == 'docx':
            img_file_path = f"{self.dir}/images"
        elif file_type == 'md':
            img_file_path = "images"

        # Create the images folder if it doesn't exist
        os.makedirs(img_file_path, exist_ok=True)

        # data to add
        markdown_title = f"# {title}\n\n"
        initial_desc = f"## Overview of Dataset Used\n\n"\
                       f"{self.summaries.initial_descriptors()}\n\n"

        # summary tables
        # categorical
        if 'categories_summary_table' in self.visuals_loc:
            cat_sum_file = os.path.basename(self.visuals_loc
                                            ['categories_summary_table'])
            cat_sum_img_path = f"{img_file_path}/{cat_sum_file}"
            # update spaces in file path to %20
            cat_sum_table = f"### Categorical Data Summary\n\n"\
                            f"![Summary table of categorical information]"\
                            f"({quote(cat_sum_img_path)})\n\n"
        # if a markdown table
        elif 'categories_summary_table' in self.summaries.tables:
            cat_sum_md = self.summaries.tables['categories_summary_table']
            cat_sum_table = f"### Categorical Data Summary\n\n"\
                            f"{cat_sum_md}\n\n"
        # if no table has been created, variable is None
        else:
            cat_sum_table = None

        # detailed categories
        if 'detailed_categories_summary_table' in self.visuals_loc:
            cat2_sum_file = (os
                             .path
                             .basename(self.visuals_loc
                                       ['detailed_categories_summary_table']))
            cat2_sum_img_path = f"{img_file_path}/{cat2_sum_file}"
            # update spaces in file path to %20
            cat2_sum_table = f"### Detailed Categorical Data Summary\n\n"\
                             f"![Summary table of categorical data]"\
                             f"({quote(cat2_sum_img_path)})\n\n"
        # if a markdown table
        elif 'categories_summary_table' in self.summaries.tables:
            cat2_sum_md = self.summaries.tables['categories_summary_table']
            cat2_sum_table = f"### Categorical Data Summary\n\n"\
                             f"{cat2_sum_md}\n\n"
        # if no table has been created, variable is None
        else:
            cat2_sum_table = None

        # numerical
        if 'numerical_summary_table' in self.visuals_loc:
            num_sum_file = (os
                            .path
                            .basename(self.
                                      visuals_loc['numerical_summary_table']))
            num_sum_img_path = f"{img_file_path}/{num_sum_file}"

            # update spaces in file path to %20
            num_sum_table = f"### Numerical Data Summary\n\n"\
                            f"![Summary table of numerical information]"\
                            f"({quote(num_sum_img_path)})\n\n"

        elif 'numerical_summary_table' in self.summaries.tables:
            num_sum_md = self.summaries.tables['numerical_summary_table']
            num_sum_table = f"### Numerical Data Summary\n\n"\
                            f"{num_sum_md}\n\n"
        # if no workflow has been created, variable is None
        else:
            num_sum_table = None

        # all
        if 'summary_table_all' in self.visuals_loc:
            all_sum_file = os.path.basename(self.visuals_loc
                                            ['summary_table_all'])
            all_sum_img_path = f"{img_file_path}/{all_sum_file}"

            # update spaces in file path to %20
            all_sum_table = f"### Data Summary Table\n\n"\
                            f"![Summary table of dataset]"\
                            f"({quote(all_sum_img_path)})\n\n"

        elif 'summary_table_all' in self.summaries.tables:
            all_sum_md = self.summaries.tables['summary_table_all']
            all_sum_table = f"### Numerical Data Summary\n\n"\
                            f"{all_sum_md}\n\n"
        # if no workflow has been created, variable is None
        else:
            all_sum_table = None

        # check preprocessing
        preprocessing_log = []
        # check for imputing
        if self.preprocessing.check_imputes_step() is True:
            pp_text = self.preprocessing.imputing_commentary()
            preprocessing_log.append(pp_text)
        # check for dummy encoding
        if self.preprocessing.check_dummy_encoding() is True:
            pp_text = self.preprocessing.dummy_encoding_commentary()
            preprocessing_log.append(pp_text)
        # check for scaled categories
        if self.preprocessing.check_cats_scaled() is True:
            pp_text = self.preprocessing.cat_scaling_commentary()
            preprocessing_log.append(pp_text)

        # join preprocessing commentary if any done
        if len(preprocessing_log) > 1:
            preprocessing_text = ' '.join(preprocessing_log)
        elif len(preprocessing_log) == 1:
            preprocessing_text = preprocessing_log[0]
        else:
            preprocessing_text = None

        # check for model
        if self.model.check_model_exists() is True:
            model_text = self.model.model_commentary()
        else:
            model_text = None

        # if there's a workflow diagram stored in images
        if 'workflow' in self.visuals_loc:
            workflow_file = os.path.basename(self.visuals_loc['workflow'])
            workflow_img_path = f"{img_file_path}/{workflow_file}"
            # use workflow_img_path
            # update spaces in file path to %20
            workflow = f"### Data Processing Workflow\n\n"\
                       f"![Workflow diagram of data processing]"\
                       f"({quote(workflow_img_path)})\n\n"
        # if no workflow has been created, variable is None
        else:
            workflow = None

        # check for metrics methods
        if self.metrics.check_metrics_step() is True:
            metrics_text = self.metrics.metrics_commentary()
        else:
            metrics_text = None

        # check for confusion matrix
        if 'confusion matrix' in self.visuals_loc.keys():
            c_matrix = os.path.basename(self.visuals_loc['confusion matrix'])
            c_matrix_path = f"{img_file_path}/{c_matrix}"
            # use workflow_img_path
            # update spaces in file path to %20
            cm = f"### Confusion Matrix Plot\n"\
                 f"\n![Confusion Matrix Plot]"\
                 f"({quote(c_matrix_path)})\n\n"
        else:
            cm = None

        # check for confusion matrix
        if 'roc curve' in self.visuals_loc.keys():
            roc_curve = os.path.basename(self.visuals_loc['roc curve'])
            roc_curve_path = f"{img_file_path}/{roc_curve}"
            # use workflow_img_path
            # update spaces in file path to %20
            roc = f"### Receiver Operating Characteristic (ROC) Curve\n\n"\
                  f"![Receiver Operating Characteristic (ROC) Curve plot]"\
                  f"({quote(roc_curve_path)})\n\n"
        else:
            roc = None

        # write to md file
        # Open the file in write mode
        with open(md_file_path, "w", encoding="utf-8") as f:
            # write the various input into the file
            f.write(markdown_title)
            f.write(initial_desc)
            # write summary tables
            if cat_sum_table is not None:
                f.write(cat_sum_table)
                f.write("\n\n")
            if cat2_sum_table is not None:
                f.write(cat2_sum_table)
                f.write("\n\n")
            if num_sum_table is not None:
                f.write(num_sum_table)
                f.write("\n\n")
            if all_sum_table is not None:
                f.write(all_sum_table)
                f.write("\n\n")

            # if there is preprocessing text
            if preprocessing_text is not None:
                f.write("## Preprocessing the dataset\n\n"
                        f"{preprocessing_text}\n\n")
            # if there is model text
            if model_text is not None:
                f.write("## Model Used\n\n")
                f.write(f"{model_text}\n\n")

            # if there is a workflow diagram
            if workflow is not None:
                f.write(workflow)
                f.write("\n\n")
            # if there is text for the metrics
            if metrics_text is not None:
                f.write("## Reviewing the model\n\n")
                f.write(metrics_text)
                f.write("\n\n")
            # if there is a confusion matrix
            if cm is not None:
                f.write(cm)
                f.write("\n\n")
            # if there is a roc curve
            if roc is not None:
                f.write(roc)
                f.write("\n\n")
        # close the file
        f.close()

        # if the file type chosen is docx
        if file_type == 'docx':
            # create variable for docx file path
            docx_file_path = f"{self.dir}/{file_name}.docx"
            # use convert_md_to_docx function in outputs.py
            convert_md_to_docx(md_file_path, docx_file_path)
            # print notification that content has been saved.
            print(f"Word file has been written to {self.dir}.")
        # if file type is not docx print alternative complete message
        else:
            print(f"Markdown has been written to {self.dir}.")
        if os.path.exists(self.dir):
            tidy_up_images(self, img_file_path, output_img_files)

    def create_mappings(self, cols: list, friendly_names: list = None,
                        friendly_values: dict = None, missing_val=None):
        '''
        Creates a nested dictionary of information on the data frame
        which is used to create summary information.

        Parameters:
        cols: list
            list of columns in the data frame.

        friendly_names: list (default: None)
            list of alternative column names to improve output
            readability (must be in same order as the cols list)

        friendly_values: nested dictionary (default: None)
            dictionary of keys (columns as named in the data frame)
            and values which are key value pairs, where the key
            refers to the existing value in the dataframe, and the
            value refers to the preferred value for outputs where
            this would improve readability.

        missing_val: dictionary (default: 'Missing')
            dictionary of key, value pairs where the key refers to
            the columns as named in the data frame, and the values
            refer to the preferred representation of a null value in
            the column when displayed in summaries.  Used for
            categorical information (not for imputing).

        Returns:
        -------
        nested dictionary: mappings for the pd.Dataframe columns

        '''
        column_mappings = {}

        for i, col in enumerate(cols):
            # define 'friendly_text'
            if friendly_names is None:
                friendly_text = col
            else:
                friendly_text = friendly_names[i]

            # define 'values_to_replace'
            if friendly_values is not None:
                if col in friendly_values.keys():
                    friendly_values = friendly_values[col]
                else:
                    friendly_values = None
            else:
                friendly_values = None

            # add column information to main dict
            column_mappings[col] = {'friendly_text': friendly_text,
                                    'values_to_replace': friendly_values}

            if missing_val is not None:
                friendly_values[np.nan] = missing_val
                friendly_values['<NA>'] = missing_val
        # update attribute
        self.column_mapping = column_mappings
