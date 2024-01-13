'''
Contains the Preprocess class which holds all the preprocessing actions
available within datascribe to action and log.

'''
import numpy as np
from pandas import get_dummies
from sklearn.preprocessing import (MinMaxScaler,
                                   StandardScaler)
import pandas as pd


class Preprocess:
    '''
    Class which holds all the preprocessing actions and information.

    '''
    def __init__(self) -> None:
        '''
        Initiator method

        '''
        # impute information
        self.imputed_mean_cols = []
        self.imputed_median_cols = []
        self.imputed_mode_cols = []
        self.imputed_backfill_cols = []
        self.imputed_forwardfill_cols = []
        self.imputed_constant_cols = []
        self.constant_vals = {}
        # dummy encoding information
        self.dummy_coding_cols = []
        # scaled columns
        self.all_categories_scaled = []
        # Standardised scaling data
        self.data_standardised_check = False

    def imputing_numeric_mean(self, df, columns=None):
        '''
        Imputes missing values with the mean if there are missing
        values present.  If no columns are specified, all numeric
        data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns added, use them
        if columns is not None:
            numeric_columns = columns
        # otherwise, identify numerical fields
        else:
            numeric_columns = df.select_dtypes([np.number]).columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(numeric_columns, list):
            numeric_columns = [col for col in numeric_columns
                               if df[col].isna().sum() > 0]
        elif not (isinstance(numeric_columns, str)
                  and df[numeric_columns].isna().sum() > 0):
            numeric_columns = None
        elif (isinstance(numeric_columns, str)
              and not df[numeric_columns].isna().sum() > 0):
            numeric_columns is None

        # if not an empty list
        if (numeric_columns != [] and numeric_columns is not None):
            # fill NAs with mean
            df[numeric_columns] = (df[numeric_columns]
                                   .fillna(df[numeric_columns].mean()))
            # store columns processed
            if isinstance(numeric_columns, list):
                for col in numeric_columns:
                    if col not in self.imputed_mean_cols:
                        self.imputed_mean_cols.append(col)
            else:
                if numeric_columns not in self.imputed_mean_cols:
                    self.imputed_mean_cols.append(numeric_columns)
        else:
            print("None of the columns were imputed with the mean as"
                  " there were no suitable columns or null values.")
        # return data frame
        return df

    def imputing_numeric_median(self, df, columns=None):
        '''
        Imputes missing values with the median if there are missing
        values present.  If no columns are specified, all numeric
        data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is not None:
            numeric_columns = columns
        # if no columns specified
        else:
            # identify numeric data types
            numeric_columns = df.select_dtypes([np.number]).columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(numeric_columns, list):
            numeric_columns = [col for col in numeric_columns
                               if df[col].isna().sum() > 0]
        elif not (isinstance(numeric_columns, str)
                  and df[numeric_columns].isna().sum() > 0):
            numeric_columns = None
        elif (isinstance(numeric_columns, str)
              and not df[numeric_columns].isna().sum() > 0):
            numeric_columns is None

        if numeric_columns != [] and numeric_columns is not None:
            df[numeric_columns] = (df[numeric_columns]
                                   .fillna(df[numeric_columns].median()))
            # store columns processed
            if isinstance(numeric_columns, list):
                for col in numeric_columns:
                    if col not in self.imputed_median_cols:
                        self.imputed_median_cols.append(col)
            else:
                if numeric_columns not in self.imputed_median_cols:
                    self.imputed_median_cols.append(numeric_columns)
            # return data frame
            return df
        else:
            print("None of the columns were imputed with the median as"
                  " there were no suitable columns or null values.")
            return df

    def imputing_numeric_mode(self, df, columns=None):
        '''
        Imputes the mode value in place of null values if there are
        missing values present.  If no columns are specified, all
        numeric data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is not None:
            numeric_columns = columns
        # if no columns specified
        else:
            # identify numeric data types
            numeric_columns = df.select_dtypes([np.number]).columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(numeric_columns, list):
            numeric_columns = [col for col in numeric_columns
                               if df[col].isna().sum() > 0]
        elif not (isinstance(numeric_columns, str)
                  and df[numeric_columns].isna().sum() > 0):
            numeric_columns = None
        elif (isinstance(numeric_columns, str)
              and not df[numeric_columns].isna().sum() > 0):
            numeric_columns is None
        if numeric_columns != [] or numeric_columns is not None:
            df[numeric_columns] = (df[numeric_columns]
                                   .fillna(df[numeric_columns]
                                   .mode().iloc[0]))
            # store columns processed
            if isinstance(numeric_columns, list):
                for col in numeric_columns:
                    if col not in self.imputed_mode_cols:
                        self.imputed_mode_cols.append(col)
            else:
                if numeric_columns not in self.imputed_mode_cols:
                    self.imputed_mode_cols.append(numeric_columns)
            # return data frame
            return df
        else:
            print("None of the columns were imputed with the mode as"
                  " there were no suitable columns or null values.")
            return df

    def imputing_numeric_constant(self, df, constant=0, columns=None):
        '''
        Imputes a fixed value in place of null values if there are
        missing values present.  If no columns are specified, all
        numeric data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is not None:
            numeric_columns = columns
        # if no columns specified
        else:
            # identify numeric data types
            numeric_columns = df.select_dtypes([np.number]).columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(numeric_columns, list):
            numeric_columns = [col for col in numeric_columns
                               if df[col].isna().sum() > 0]
        elif not (isinstance(numeric_columns, str)
                  and df[numeric_columns].isna().sum() > 0):
            numeric_columns = None
        elif (isinstance(numeric_columns, str)
              and not df[numeric_columns].isna().sum() > 0):
            numeric_columns is None
        if numeric_columns != [] or numeric_columns is not None:
            df[numeric_columns] = (df[numeric_columns]
                                   .fillna(constant))
            # store columns processed
            if isinstance(numeric_columns, list):
                for col in numeric_columns:
                    if col not in self.imputed_constant_cols:
                        self.imputed_constant_cols.append(col)
                    if col not in self.constant_vals.keys():
                        self.constant_vals[col] = constant
            else:
                if numeric_columns not in self.imputed_constant_cols:
                    self.imputed_constant_cols.append(numeric_columns)
                if numeric_columns not in self.constant_vals.keys():
                    self.constant_vals[numeric_columns] = constant
            # return data frame
            return df
        else:
            print("None of the columns were imputed with the constant value"
                  " as there were no suitable columns or null values.")
            return df

    def imputing_non_numeric_constant(self, df, constant='missing',
                                      columns=None):
        '''
        Imputes a fixed value in place of null values if there are
        missing values present.  If no columns are specified, all
        non-numeric data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        constant: str (default='missing')

        columns: list (default: 'missing')
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is not None:
            non_numeric_columns = columns
        # if no columns specified
        else:
            # identify numeric data types
            non_numeric_columns = (df.select_dtypes(exclude=[np.number])
                                   .columns.to_list())
        # update numeric_columns to include columns which have null
        # values
        if isinstance(non_numeric_columns, list):
            non_numeric_columns = [col for col in non_numeric_columns
                                   if df[col].isna().sum() > 0]
        elif not (isinstance(non_numeric_columns, str)
                  and df[non_numeric_columns].isna().sum() > 0):
            non_numeric_columns = None
        elif (isinstance(non_numeric_columns, str)
              and not df[non_numeric_columns].isna().sum() > 0):
            non_numeric_columns is None
        if isinstance(non_numeric_columns, str):
            non_numeric_columns = [non_numeric_columns]
        if non_numeric_columns != [] or non_numeric_columns is not None:
            # Ensure 'missing' is in the categories
            for col in non_numeric_columns:
                if df[col].dtype == 'category':
                    if constant not in df[col].cat.categories:
                        df[col] = (df[col].cat.add_categories(constant))
            df[non_numeric_columns] = (df[non_numeric_columns]
                                       .fillna(constant))
            # store columns processed
            if isinstance(non_numeric_columns, list):
                for col in non_numeric_columns:
                    if col not in self.imputed_constant_cols:
                        self.imputed_constant_cols.append(col)
                    if col not in self.constant_vals.keys():
                        self.constant_vals[col] = constant
            else:
                if non_numeric_columns not in self.imputed_constant_cols:
                    self.imputed_constant_cols.append(non_numeric_columns)
                if non_numeric_columns not in self.constant_vals.keys():
                    self.constant_vals[non_numeric_columns] = constant
            # return data frame
            return df
        else:
            print("None of the columns were imputed with the constant value"
                  " as there were no suitable columns or null values.")
            return df

    def imputing_non_numeric_mode(self, df, columns=None):
        '''
        Imputes the mode value in place of null values if there are
        missing values present.  If no columns are specified, all
        non-numeric data type columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is not None:
            non_numeric_columns = columns
        # if no columns specified
        else:
            # identify numeric data types
            non_numeric_columns = (df.select_dtypes(exclude=[np.number])
                                   .columns.to_list())
        # update numeric_columns to include columns which have null
        # values
        if isinstance(non_numeric_columns, list):
            non_numeric_columns = [col for col in non_numeric_columns
                                   if df[col].isna().sum() > 0]
        elif not (isinstance(non_numeric_columns, str)
                  and df[non_numeric_columns].isna().sum() > 0):
            non_numeric_columns = None
        elif (isinstance(non_numeric_columns, str)
              and not df[non_numeric_columns].isna().sum() > 0):
            non_numeric_columns is None
        if non_numeric_columns != [] or non_numeric_columns is not None:
            df[non_numeric_columns] = (df[non_numeric_columns]
                                       .fillna(df[non_numeric_columns]
                                       .mode().iloc[0]))
            # store columns processed
            if isinstance(non_numeric_columns, list):
                for col in non_numeric_columns:
                    if col not in self.imputed_mode_cols:
                        self.imputed_mode_cols.append(col)
            else:
                if non_numeric_columns not in self.imputed_mode_cols:
                    self.imputed_mode_cols.append(non_numeric_columns)
            # return data frame
            return df
        else:
            print("None of the columns were imputed with the mode as"
                  " there were no suitable columns or null values.")
            return df

    def imputing_backwardfill(self, df, columns=None):
        '''
        Imputes the backward fill method in place of null values if
        there are missing values present.  If no columns are specified,
        all columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is None:
            columns = df.columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(columns, list):
            columns = [col for col in columns
                       if df[col].isna().sum() > 0]
        elif not (isinstance(columns, str)
                  and df[columns].isna().sum() > 0):
            columns = None
        elif (isinstance(columns, str)
              and not df[columns].isna().sum() > 0):
            columns is None
        if columns != [] or columns is not None:
            df[columns] = (df[columns].bfill())
            # store columns processed
            if isinstance(columns, list):
                for col in columns:
                    if col not in self.imputed_backfill_cols:
                        self.imputed_backfill_cols.append(col)
            else:
                if columns not in self.imputed_backfill_cols:
                    self.imputed_backfill_cols.append(columns)
            # return data frame
            return df
        else:
            print("None of the columns were imputed with backfill as"
                  " there were no suitable columns or null values.")
            return df

    def imputing_forwardfill(self, df, columns=None):
        '''
        Imputes the forward fill method in place of null values if there
        are missing values present.  If no columns are specified, all
        columns will be used.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns is not None
        if columns is None:
            columns = df.columns.to_list()
        # update numeric_columns to include columns which have null
        # values
        if isinstance(columns, list):
            columns = [col for col in columns
                       if df[col].isna().sum() > 0]
        elif not (isinstance(columns, str)
                  and df[columns].isna().sum() > 0):
            columns = None
        elif (isinstance(columns, str)
                and not df[columns].isna().sum() > 0):
            columns is None
        if columns != [] or columns is not None:
            df[columns] = (df[columns].ffill())
            # store columns processed
            if isinstance(columns, list):
                for col in columns:
                    if col not in self.imputed_forwardfill_cols:
                        self.imputed_forwardfill_cols.append(col)
            else:
                if columns not in self.imputed_forwardfill_cols:
                    self.imputed_forwardfill_cols.append(columns)
            # return data frame
            return df
        else:
            print("None of the columns were imputed with forward fill as"
                  " there were no suitable columns or null values.")
            return df

    def dummy_encoder(self, df, columns=None):
        '''
        Encodes non-numerical fields into binary fields.

        Parameters:
        ----------
        df: Pandas DataFrame
            data frame containing dataset

        columns: list (default: None)
            a list of columns to impute

        Returns:
        -------
        Pandas Dataframe
        '''
        # if columns chosen
        if columns is not None:
            non_numeric_columns = columns
        # if no columns specified
        else:
            # convert all non-numeric categories
            non_numeric_columns = (df.select_dtypes(exclude=[np.number])
                                     .columns.to_list())
        # use pandas get_dummies to create columns
        dummies = get_dummies(df[non_numeric_columns],
                              columns=non_numeric_columns,
                              prefix=non_numeric_columns)
        # drop original columns from data frame
        df.drop(non_numeric_columns, axis=1, inplace=True)

        # store columns processed
        if isinstance(non_numeric_columns, list):
            # for every column
            for col in non_numeric_columns:
                # only add if not in list already
                if col not in self.dummy_coding_cols:
                    self.dummy_coding_cols.append(col)
        else:
            if non_numeric_columns not in self.dummy_coding_cols:
                self.dummy_coding_cols.append(non_numeric_columns)
        # return dataframe with new encoded fields added
        return pd.concat([df, dummies], axis=1)

    def scale_categories(self, df, mappings, columns):
        '''
        Transforms categories with an order into a scale to retain the
        order in the model by using the MinMaxScaler() feature in sklearn.

        Parameters:
        ----------
        df: Pandas DataFrame
            Current data frame being used for the model.

        mappings: dict or list of dict
            If a single dictionary, it maps values to numeric order
            for all columns. If a list of dictionaries,
            each dictionary maps values to numeric order for the
            corresponding column.

        columns: str or list of str
            If a single column, the function scales that column.
            If a list of columns, the function scales each column.

        Returns:
        -------
        pandas DataFrame
            Updated data frame with columns scaled.
        '''
        # Ensure columns is a list
        if not isinstance(columns, list):
            columns = [columns]

        # Ensure mappings is a list of dictionaries
        if not isinstance(mappings, list):
            mappings = [mappings] * len(columns)

        for column, mapping in zip(columns, mappings):
            # Maps scale values to column in df
            df[column] = df[column].map(mapping)

            # Data type of column updated to integer
            df.astype({column: pd.Int8Dtype()})

            # Scaler initiated
            scaler = MinMaxScaler()

            # Fit scaler to data in column
            col_scaled = scaler.fit_transform(df[column].values.reshape(-1, 1))

            # Drop original column from data frame
            df.drop(column, axis=1, inplace=True)

            # Update data frame by joining scaled column onto data frame
            df = df.join(pd.DataFrame(col_scaled, columns=[column]))
            df = df.astype({column: float})

        # store columns processed
        if isinstance(columns, list):
            # for every column
            for col in columns:
                # only add if not in list already
                if col not in self.all_categories_scaled:
                    self.all_categories_scaled.append(col)
        else:
            if columns not in self.all_categories_scaled:
                self.all_categories_scaled.append(columns)
        # Return updated data frame
        return df

    def standardise_data(self, X_train, X_test):
        '''
        Data is converted to a similar scale by subtracting the mean and
        dividing by standard deviation for every feature.

        The resulting standardised data has a mean of 0 and a standard
        deviation of 1.

        A new scaling object is created to normalise the training set
        and is then applied to the training and test sets.

        Parameters:
        ----------
        scribe: Scribe object
            Object from Scribe class which holds all data summary and
            processing information.

        X_train: list
            list containing train split of dataset

        X_test: list
            list containing test split of dataset

        Returns:
        -------
        list: train_std

        list: test_std
        '''
        # initialise a new scaling object for normalising input data
        sc = StandardScaler()

        # set up the scaler just on the training set
        sc.fit(X_train)

        # apply the scaler to the training and test sets
        train_std = sc.transform(X_train)
        test_std = sc.transform(X_test)

        # update attribute to True
        self.data_standardised_check = True

        # return lists of standardised data
        return train_std, test_std

    def imputing_commentary(self):
        '''
        Creates commentary for any imputing methods which have been used
        on the dataset.

        Returns:
        -------
        str: text commentary
        '''
        # list of impute attributes in preprocesses
        impute_methods = [self.imputed_mean_cols,
                          self.imputed_median_cols,
                          self.imputed_mode_cols,
                          self.imputed_backfill_cols,
                          self.imputed_forwardfill_cols,
                          self.imputed_constant_cols]

        methods = ['mean value', 'median value', 'mode value',
                   'back fill method', 'forward fill method', 'constant']
        # empty list to include commentary
        commentary = []

        for index, approach in enumerate(impute_methods):
            # check whether impute was used
            if approach != []:
                if methods[index] == 'constant':
                    if len(approach) > 1:
                        num = 'values'
                    else:
                        num = 'value'
                    fields = " and ".join([", ".join(approach[:-1]),
                                          approach[-1]]
                                          if len(approach) > 2
                                          else approach)
                    constant_values = [str(self.constant_vals[col])
                                       for col in approach]
                    method = (f'the following constant {num}: '
                              f'{", ".join(constant_values)}')
                else:
                    # provide the following output
                    fields = " and ".join([", ".join(approach[:-1]),
                                          approach[-1]]
                                          if len(approach) > 2
                                          else approach)

                    method = methods[index]

                # use impute_text_formatter() to create text
                text = self.impute_text_formatter(fields, method)
                # add to commentary list
                commentary.append(text)
        if len(commentary) > 1:
            # join text together
            full_commentary = ' '.join(commentary)
        elif len(commentary) == 1:
            full_commentary = commentary[0]
        else:
            print('No missing values imputed according to log.')
        # return full_commentary
        return full_commentary

    def impute_text_formatter(self, fields, method):
        '''
        Creates text for commentary on imputing missing values.

        Parameters:
        ----------
        fields: str
            string variable which specifies the field or fields in the
            dataset used for imputing method.

        method: str
            string variable which advises on the impute method.

        Returns:
        -------
        str: text for commentary
        '''
        text = f"Null values in {fields} were imputed with the {method}."

        return text

    def check_imputes_step(self):
        '''
        Checks whether any imputing has taken place.

        Returns:
        -------
        boolean
        '''
        list_of_imputes = [self.imputed_mean_cols, self.imputed_median_cols,
                           self.imputed_mode_cols, self.imputed_backfill_cols,
                           self.imputed_forwardfill_cols,
                           self.imputed_constant_cols]
        # check if any list is not empty
        any_non_empty = any(lst for lst in list_of_imputes if lst)

        # return result
        return any_non_empty

    def dummy_encoding_commentary(self):
        '''
        Creates commentary for any dummy encoding methods which have
        been used on the dataset.

        Returns:
        -------
        str: text commentary

        '''
        # empty list to include commentary
        commentary = None

        # check whether impute mean was used
        if self.dummy_coding_cols != []:
            # provide the following output
            fields = " and ".join([", ".join(self.dummy_coding_cols[:-1]),
                                  self.dummy_coding_cols[-1]]
                                  if len(self.dummy_coding_cols) > 2
                                  else self.dummy_coding_cols)
            # create text
            text = f"One-hot encoding was used on {fields} using the "\
                   f"pandas `get_dummies` method."

            # add to commentary variable
            commentary = text
        # return commentary
        return commentary

    def check_dummy_encoding(self):
        '''
        Checks whether any dummy encoding has taken place.

        Returns:
        -------
        boolean
        '''
        # check if any list is not empty
        any_non_empty = any(self.dummy_coding_cols)

        # return result
        return any_non_empty

    def cat_scaling_commentary(self):
        '''
        Creates commentary for any category scaling which have
        been used on the dataset.

        Returns:
        -------
        str: text commentary

        '''
        # empty list to include commentary
        commentary = None

        # check whether impute mean was used
        if self.all_categories_scaled != []:
            # provide the following output
            fields = " and ".join([", ".join(self.all_categories_scaled[:-1]),
                                  self.all_categories_scaled[-1]]
                                  if len(self.all_categories_scaled) > 2
                                  else self.all_categories_scaled)
            if len(self.all_categories_scaled) > 1:
                num = "were"
            else:
                num = "was"
            # create text
            text = f"The order of {fields} {num} retained by mapping the "\
                   f"order of the values and using the `MinMaxScaler()`"\
                   f" method from the `sklearn` package to create a scale "\
                   f"between 0 and 1."

            # add to commentary variable
            commentary = text
        # return commentary
        return commentary

    def check_cats_scaled(self):
        '''
        Checks whether any ordered categories have been scaled.

        Returns:
        -------
        boolean
        '''
        # check if any list is not empty
        any_non_empty = any(self.all_categories_scaled)

        # return result
        return any_non_empty
