'''
Contains functions for loading example datasets
'''

import pandas as pd
import os
import sys
from datascribe.scribe import Scribe
import numpy as np

example_dataset = 'data/ae_data.csv'
example_processed_dataset = 'data/ae_processed.csv'


def load_ed_example():
    '''
    This data has been taken from the NHS A&E synthetic dataset
    available at https://shorturl.at/dlGXY

    This subset of data is from calendar year 2016
    (01/01/2016 - 31/12/2016) for Provider ID 15273.

    Every row is a single attendance log for the provider.  There are
    various columns advising on different features for the particular
    attendance.

    The returned data frame does not use a particular column for the
    index.

    Data frame shape = (106102, 13)

    Returns
    -------
    pandas.DataFrame
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, example_dataset)
    df = clean_up_data(path)
    return df


def clean_up_data(data):
    '''
    Cleans up the data types etc for ED example dataset

    Params:
    ------
    data: csv file
        csv file containing ED data

    Returns:
    pandas.Dataframe
    '''
    cols = ['IMD_Decile_From_LSOA', 'Age_Band', 'Sex', 'AE_Arrive_Date',
            'AE_Arrive_HourOfDay', 'AE_Time_Mins', 'AE_HRG',
            'AE_Num_Diagnoses', 'AE_Num_Investigations', 'AE_Num_Treatments',
            'AE_Arrival_Mode', 'Provider_Patient_Distance_Miles',
            'Admitted_Flag']

    data_types = {
        'IMD_Decile_From_LSOA': pd.Int8Dtype(),
        'Age_Band': 'category',
        'Sex': 'category',
        'AE_Arrive_HourOfDay': 'category',
        'AE_Time_Mins': pd.Int32Dtype(),
        'AE_HRG': 'category',
        'AE_Num_Diagnoses': pd.Int32Dtype(),
        'AE_Num_Investigations': pd.Int32Dtype(),
        'AE_Num_Treatments': pd.Int32Dtype(),
        'AE_Arrival_Mode': 'category',
        'Provider_Patient_Distance_Miles': pd.Float32Dtype(),
        'Admitted_Flag': pd.Int8Dtype()
    }

    df = (pd.read_csv(data, dtype=data_types, usecols=cols)
            .assign(AE_Arrive_Date=lambda x:
                    pd.to_datetime(x['AE_Arrive_Date'], format='%Y-%m-%d')))

    return df


def load_preprocessed_ed_example():
    '''
    This function loads a processed version of the dataset which can be
    loaded unprocessed from datasets with the function
    'load_ed_example()'.

    This data has been taken from the NHS A&E synthetic dataset
    available at https://shorturl.at/dlGXY

    This subset of data is from calendar year 2016
    (01/01/2016 - 31/12/2016) for Provider ID 15273.

    Every row is a single attendance log for the provider.  There are
    various columns advising on different features for the particular
    attendance.  The features have been processed to numerical to work
    in machine learning models for logistic regression.  preprocessing
    included creating dummies for categories and scaling ordered
    categories as well as imputing missing values.

    The returned data frame does not use a particular column for the
    index.

    Data frame shape = (106102, 13)

    Returns
    -------
    pandas.DataFrame
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, example_processed_dataset)
    df = pd.read_csv(path).astype('float32')
    return df


def load_ed_scribe_processed():
    '''
    Returns both the Scribe instance and data frame processed in
    the first two notebooks within the documentation for datascribe.

    '''
    block_print()
    # load ED attendances example
    df = load_ed_example()

    # specify folder directory
    file_loc = 'output'

    # define what the rows are called (singular, plural)
    row_description = ("attendance", "attendances")

    # create a Scribe object called scriber
    s = Scribe(df, dir=file_loc, row_descriptor=row_description)

    # summary info
    # create a dictionary of the information you wish to include
    column_mapping = {
        'Sex': {'friendly_text': 'Gender',
                'values_to_replace': {1: 'Male',
                                      2: 'Female',
                                      3: 'Indeterminate',
                                      4: 'Unknown',
                                      '<NA>': 'Missing',
                                      np.nan: 'Missing'}},
        'IMD_Decile_From_LSOA': {'friendly_text': 'IMD Decile from LSOA',
                                 'values_to_replace': {'<NA>': 'Missing',
                                                       np.nan: 'Missing'}},
        'Age_Band': {'friendly_text': 'Age Band',
                     'values_to_replace': {'<NA>': 'Missing',
                                           np.nan: 'Missing'}},
        'AE_Arrive_Date': {'friendly_text': 'Arrival Date',
                           'values_to_replace': None},
        'AE_Arrival_Mode': {'friendly_text': 'Arrival Mode',
                            'values_to_replace': {'<NA>': 'Missing',
                                                  np.nan: 'Missing'}},
        'AE_HRG': {'friendly_text': 'HRG Tariff Grouping',
                   'values_to_replace': {'<NA>': 'Missing',
                                         np.nan: 'Missing'}},
        'AE_Num_Treatments': {'friendly_text': 'Number of Treatments',
                              'values_to_replace': None},
        'AE_Num_Investigations': {'friendly_text': 'Number of Investigations',
                                  'values_to_replace': None},
        'AE_Num_Diagnoses': {'friendly_text': 'Number of Diagnosis',
                             'values_to_replace': None},
        'AE_Time_Mins': {'friendly_text': 'Time in A&E (mins)',
                         'values_to_replace': None},
        'AE_Arrive_HourOfDay': {'friendly_text': 'Arrival Hour of the Day',
                                'values_to_replace': None},
        'Provider_Patient_Distance_Miles': {'friendly_text': 'Provider ID',
                                            'values_to_replace': None},
        'Admitted_Flag': {'friendly_text': 'Admission Status',
                          'values_to_replace': {0: 'Not Admitted',
                                                1: 'Admitted',
                                                '<NA>': 'Not Known',
                                                np.nan: 'Missing'}}}

    # add to column_mapping attribute
    s.column_mapping = column_mapping
    # specify dependent variable you wish to use to split summary tables
    d_var = 'Admitted_Flag'

    # create a summary table of all the categories
    s.summaries.summary_table(d_var=d_var, dtype='c1',
                              output_type='img', dp=2, show=False)
    # summary table of numerical fields
    s.summaries.summary_table(d_var=d_var, dtype='n',
                              output_type='md', dp=2, show=False)

    # preprocessing - imputing
    cols_for_mean = 'Provider_Patient_Distance_Miles'
    df = s.preprocessing.imputing_numeric_mean(df, cols_for_mean)
    cols_for_median = 'IMD_Decile_From_LSOA'
    df = s.preprocessing.imputing_numeric_median(df, cols_for_median)
    cols_for_mode_num = 'Admitted_Flag'
    df = s.preprocessing.imputing_numeric_mode(df, cols_for_mode_num)
    cols_mode_cat = 'AE_Arrive_HourOfDay'
    df = s.preprocessing.imputing_non_numeric_mode(df, cols_mode_cat)
    col_constant = 'Sex'
    df = s.preprocessing.imputing_non_numeric_constant(df,
                                                       columns=col_constant)
    df = s.preprocessing.imputing_non_numeric_constant(df,
                                                       constant='Nothing',
                                                       columns='AE_HRG')

    # preprocessing - scaling
    # specify columns
    cols_for_scaling = ['Age_Band', 'AE_Arrive_HourOfDay', 'AE_HRG']
    # specify mappings for above columns
    cols_scale_map = [{'1-17': 1, '18-24': 2,
                       '45-64': 3, '25-44': 4,
                       '65-84': 5, '85+': 6},
                      {'01-04': 1, '05-08': 2, '09-12': 3,
                       '13-16': 4, '17-20': 5, '21-24': 6},
                      {'Nothing': 1, 'Low': 2, 'Medium': 3, 'High': 4}]
    # call method to scale
    df = s.preprocessing.scale_categories(df, cols_scale_map,
                                          cols_for_scaling)
    # preprocessing - dummies
    cols_for_dummies = ['Sex', 'AE_Arrival_Mode']
    df = s.preprocessing.dummy_encoder(df, cols_for_dummies)

    df.drop(columns=['AE_Arrive_Date'], inplace=True)

    # return data frame and Scribe object
    enable_print()
    return df, s


def load_ed_scribe_processed_modeled():
    '''
    Returns the Scribe instance processed with example Emergency
    Department dataset from NHS synthetic dataset.

    Returns:
    -------
    s: Scribe object containing model and preprocessing

    '''
    block_print()
    df, s = load_ed_scribe_processed()
    # stratified k fold
    n_splits = 10
    s.model.k_fold(n_splits=n_splits)
    # split dataset
    X = df.drop('Admitted_Flag', axis=1)
    y = df['Admitted_Flag']
    test_size = 0.3
    s.model.split_dataset(X, y, test_size=test_size, stratify=y)
    # standarize input
    X_train, X_test = \
        s.preprocessing.standardise_data(s.model.splitted_data['X_train'],
                                         s.model.splitted_data['X_test'])

    s.model.splitted_data['X_train'] = X_train
    s.model.splitted_data['X_test'] = X_test
    # define model
    params = {'random_state': [42],
              'solver': ['lbfgs', 'sag']}
    s.model.regression_model(params=params)
    # train model
    s.model.fit()
    # test model
    s.model.predict()
    enable_print()
    return s


def load_ed_scribe_evaluated():
    '''
    Returns the Scribe instance processed with example Emergency
    Department dataset from NHS synthetic dataset.

    Returns:
    -------
    s: Scribe object containing preprocessing, model and metrics.

    '''
    block_print()
    s = load_ed_scribe_processed_modeled()

    s.metrics.mae()
    s.metrics.mse()
    s.metrics.r2score()
    s.metrics.confusionmatrix()
    s.metrics.roc()
    s.metrics.prec_rec_f1_score()
    enable_print()
    return s


def block_print():
    '''
    Blocks print messages when re-running previously described code.
    '''
    sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
    '''
    Re-enables print messages when re-run of previously described code
    is complete.
    '''
    sys.stdout = sys.__stdout__
