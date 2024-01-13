import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.api.types import (is_numeric_dtype,
                              is_string_dtype)
import os
from natsort import natsorted
from datetime import datetime


class Summary_stats():
    '''
    class which provides summary information on initial dataframe.

    '''
    def __init__(self, scribe, initial_df):
        '''
        Initiator method for Initial_summaries.

        Parameters:
        ----------
        scribe: class
            class which holds workflow information

        initial_df: pd.Dataframe
            Initial dataset being used in analysis.

        '''
        self.scribe = scribe
        self.initial_df = initial_df.copy()
        self.tables = {}

    def initial_descriptors(self):
        '''
        Describes the characteristics of the initial dataset.

        '''
        # describe the shape of the initial dataset
        df_shape = self.initial_df.shape
        row_desc = self.scribe.row_descriptor
        col_desc = self.scribe.col_descriptor
        # check whether the rows and columns have more
        row_name = row_desc[0] if df_shape[0] == 1 else row_desc[1]
        col_name = col_desc[0] if df_shape[1] == 1 else col_desc[1]

        # describe the fields missing data
        nulls = self.initial_df.isna().sum()
        null_bd = []
        for index, val in nulls.items():
            if val != 0:
                null_bd.append(f"{index} ({val})")
        if null_bd != []:
            null_summary = " and ".join([", ".join(null_bd[:-1]), null_bd[-1]]
                                        if len(null_bd) > 2 else null_bd)

            output = f"The dataset consisted of {'{:,}'.format(df_shape[0])} "\
                     f"{row_name} and "\
                     f"{'{:,}'.format(df_shape[1])} {col_name}. The following"\
                     f" {col_name} contained null values: {null_summary}."\

        else:
            output = f"The dataset consisted of {'{:,}'.format(df_shape[0])} "\
                     f"{row_name} and {'{:,}'.format(df_shape[1])} {col_name}"\
                     f". The dataset contained no null values."
        return output

    def plot_table(self, data, filename, show=True, dp=0):
        '''
        Plots the summary statistics table onto a matplotlib axis and
        exports to a .png image file in the output folder.

        The output file location is saved into the Scribe object's
        visuals_loc attribute as a dictionary entry.

        Parameters:
        ----------
        data: pd.Dataframe
            Dataframe containing the summary statistics to be displayed.

        filename: str
            string variable to determine name of output image.

        show: boolean (default=True)
            Optional argument to prevent a preview of the image
            appearing (the image file will still be saved).

        '''
        # extract column names from data frame
        columns = data.columns.to_list()
        # add blank item at start of list for index space
        columns.insert(0, '        ')
        # create variable column_names from columns list
        column_names = columns
        # calculate number of columns
        ncols = len(columns)
        # if number of columns is more than 10, rotate headings by 45 deg
        if ncols > 5:
            rotation_text = 45
        else:
            rotation_text = 0
        # calculate number of rows
        nrows = data.shape[0]
        # add item at start of list for index space
        if ncols > len(column_names):
            column_names.insert(0, 'Variable')
        # use existing index names
        index_names = data.index.to_list()
        # if image folder not yet made, create it
        img_folder = f"{self.scribe.dir}/images"
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        # file name
        output_file = f'{img_folder}/{filename}.png'

        # locate longest word in index
        max_index_length = max(len(str(index)) for index in index_names)
        # if longest word in index values is shorter than word 'Variables',
        # use the length of 'Variables' instead for max_index_length
        if max_index_length < len(column_names[0]):
            max_index_length = len(column_names)
        # calculate width required for column containing indexes
        index_width = max_index_length * 0.1
        # set figure width
        fig_width = ncols * 1.1

        # create fig and ax at print quality level (dpi 300)
        fig = plt.figure(figsize=(fig_width + index_width, nrows*0.5), dpi=300)
        ax = plt.subplot()

        # set y axis view limit
        ax.set_ylim(0, nrows + 1)
        # Check if there is only one column
        if ncols == 1:
            # if only one column, set positions to the center
            positions = np.array([fig_width / 2])
        else:
            # if multiple columns, create positions for columns
            positions = np.linspace(index_width + 0.25, fig_width
                                    + index_width - 0.75, ncols)

        # add table's main text
        for i in range(nrows):
            # add indexes to left of plot
            ax.annotate(
                xy=(0, i + 0.5),
                text=str(index_names[i]),
                ha='left',
                va='center',
                weight='bold'
            )
            # iterate through every column (exclude first column as it
            # creates space for the index)
            for j, column in enumerate(columns[1:]):
                # centre text
                ha = 'center'
                # if value is Nonetype show '-'
                if data[column].iloc[i] is None:
                    text_label = '-'
                    weight = 'normal'
                # if value is a date format
                elif is_date(data[column].iloc[i]):
                    # format date to dd/mm/yyyy
                    text_label = format_date(data[column].iloc[i])
                    weight = 'normal'
                # if value is a string data type
                elif (is_string_dtype(data[column].iloc[i]) or
                        isinstance(data[column].iloc[i], str)):
                    # copy to plot as it is
                    text_label = data[column].iloc[i]
                    weight = 'normal'
                # if column is mean or std and it's a number
                elif ((': mean' in column or ': std' in column)
                      and (is_numeric_dtype(data[column].iloc[i])
                           or isinstance(data[column].iloc[i],
                                         (int, float)))):
                    if pd.isna(data[column].iloc[i]):
                        text_label = '-'
                        weight = 'normal'
                    else:
                        # format to dp variable decimal places and add
                        # commas
                        text_label = f"{data[column].iloc[i]:,.{dp}f}"
                        weight = 'normal'
                # show whole numbers and add commas for other numbers
                elif (is_numeric_dtype(data[column].iloc[i])
                        or isinstance(data[column].iloc[i], (int, float))):
                    text_label = f'{data[column].iloc[i]:,.0f}'
                    weight = 'normal'
                # all other values - plot '-' as likely to be null values
                else:
                    text_label = '-'
                    weight = 'normal'
                # annotate these specifications to the plot
                ax.annotate(
                    xy=(positions[j], i + 0.5),
                    text=text_label,
                    ha=ha,
                    va='center',
                    weight=weight
                )

        # add 'Variable' as heading for index in plot
        ax.annotate(
            xy=(0, nrows + 0.25),
            text=column_names[0],
            ha='left',
            va='bottom',
            weight='bold'
        )
        # iterate through column names and add to plot
        for index, c in enumerate(column_names[1:]):
            ha = 'center'
            ax.annotate(
                xy=(positions[index], nrows + 0.25),
                text=column_names[index + 1],
                ha=ha,
                va='bottom',
                weight='bold',
                rotation=rotation_text
            )

        # add dividing lines
        # add dark grey line under headings
        ax.plot([0, positions[-1]], [nrows, nrows], lw=1, color='darkgray',
                marker='', zorder=4)
        # add grey dashed line between rows
        for x in range(1, nrows):
            ax.plot([0, positions[-1]], [x, x], lw=0.8, color='gray', ls=':',
                    zorder=3, marker='')

        # do not show plot axis
        ax.set_axis_off()
        # use tight layout
        plt.tight_layout()

        # save figure in output folder at print quality (300 dpi)
        plt.savefig(
            output_file,
            dpi=300,
            bbox_inches='tight'
        )

        # show the plot, unless argument 'show' has been set to False
        if show is True:
            plt.show()
        else:
            plt.close()

        # return location of summary stats .png location
        self.scribe.visuals_loc[filename] = output_file

    def summarise_categories(self, d_var, output_type: str = 'md', show=True):
        '''
        Creates the detailed summary information for categorical
        information in a data frame using the initial pandas Dataframe
        which was passed into the Scribe object.

        The result depends on the output type:

        - If output is 'md', the code for the markdown table is saved
        into the `tables` attribute as a dictionary item.

        - If the output is 'img', the plot_table() function will be
        run to convert the table into an image file using matplotlib.

        Parameters:
        ----------
        d_var: str
            String variable which is the dependent variable in model

        output_type: str (default: 'md')
            specifies whether to output as an image .png file (img) or
            markdown (md) table.

        show: boolean (default = True)
            Indicator on whether to show output if .png file is output.

        '''
        # make a copy of the initial data frame
        df = self.initial_df.copy()
        # check there are further categorical fields
        if (df.drop(columns=d_var).
            select_dtypes(include=['category', 'object']).
                columns.empty is True):
            error = ("Unable to produce categorical table as no categorical"
                     " fields to summarise.")
            print(error)
            return

        # variable to call final table
        final_output = 'detailed_categories_summary_table'

        # use get_friendly_text() function to retrieve category items
        df, cat_keys, fr_names = self.get_friendly_text(df, d_var,
                                                        dtype='c')

        # convert categorical columns to category type
        df[cat_keys] = df[cat_keys].astype(str)

        # Create a dictionary to map old column names to new column names
        columns_mapping = dict(zip(cat_keys, fr_names))

        # Rename columns using the rename method
        df.rename(columns=columns_mapping, inplace=True)

        # Replace values in dependent variable column
        try:
            # read as string
            df[d_var] = df[d_var].astype(str)
            # obtain original values
            original = [str(i)
                        for i in
                        self.scribe.column_mapping[d_var]
                        ['values_to_replace'].keys()]
            # obtain replacement values
            new_val = [str(i)
                       for i in
                       self.scribe.column_mapping[d_var]
                       ['values_to_replace'].values()]
            # replace values
            df[d_var].replace(original, new_val, inplace=True)
            # if there is a friendly text form for the dependent variable,
            # rename the variable and column in the data frame
            if self.scribe.column_mapping[d_var]['friendly_text'] is not None:
                df.rename(columns={d_var: self.scribe.column_mapping[d_var]
                                   ['friendly_text']}, inplace=True)
                d_var = self.scribe.column_mapping[d_var]['friendly_text']
        except Exception as e:
            print(f"Using existing values for dependent variable. ({e})")

        # create a column called 'Count' to count the rows when df pivoted
        df['Count'] = 1

        # empty list to store multiple data frames
        dfs = []
        # for every categorical column
        for cat in fr_names:
            if cat != d_var:
                # create a pivot table with the columns being the dependent
                # variable
                pvted = df.pivot_table(values='Count', columns=d_var,
                                       index=cat, aggfunc='sum')
                # add a column 'Variable' to highlight which field the data
                # came from
                pvted['Variable'] = cat
                # remove index
                pvted.reset_index(inplace=True)
                # rename the column holding the categorical value as
                # 'Categories'
                pvted.rename(columns={cat: "Categories"}, inplace=True)
                # use natorted() to sort 'Categories' in order
                sorted_order = natsorted(pvted.index,
                                         key=lambda x: pvted['Categories'][x])
                # sort the data frame based on the sorted order
                pvted = pvted.loc[sorted_order].reset_index(drop=True)
                # add data frame to list of data frames
                dfs.append(pvted)
        # if more than one data frame
        if len(dfs) > 1:
            # join together the list of data frames
            result_df = pd.concat(dfs, ignore_index=True, axis=0)
        else:
            result_df = dfs[0]
        # set 'Variable' and 'Categories' as a MultiIndex to get columns on
        # left side
        result_df.set_index(['Variable', 'Categories'], drop=True,
                            inplace=True)
        # reset index
        md_df = result_df.reset_index(inplace=True)
        # fill empty values with zero
        md_df = result_df.fillna(0)
        # save markdown code to variable
        output = md_df.to_markdown(index=False)

        # if output_type is 'md' for markdown, save markdown code to tables
        # attribute in Scribe object
        if output_type == 'md':
            self.tables[final_output] = output
        # if image file output, continue
        else:
            # reverse order (as image processing inputs bottom-up)
            md_df = md_df[::-1]
            # create new index column by joining values in 'Variable' and
            # 'Categories'
            new_index = (md_df['Variable']
                         .astype(str) + ": " + md_df['Categories']
                         .astype(str))
            # insert new index as first column
            md_df.insert(0, 'var', new_index)
            # drop 'Variable' and 'Categories' columns
            md_df.drop(columns=['Variable', 'Categories'], inplace=True)
            # empty dictionary to store columns to use in final data frame
            final_cols = {}
            # for every column in md_df
            for col in md_df.columns.to_list():
                # if column is new index (called 'var')
                if col == 'var':
                    # extract list of values for index
                    idx = md_df[col].to_list()
                # otherwise, add to final_cols list
                else:
                    final_cols[col] = md_df[col].to_list()
            # create output_df data frame using idx and final_cols
            output_df = pd.DataFrame(index=idx, data=final_cols)
            # use plot_table() function to produce image file
            self.plot_table(output_df, final_output, show=show)

    def summary_table(self, d_var, output_type: str = 'md',
                      dtype='all', dp=0, show=True):
        '''
        Creates the summary information for all information in a
        data frame using pandas inbuilt .describe() method.

        The default is to show all fields.  However, the user can decide
        on specifying categorical or numerical as well.

        The result depends on the output type:

        - If output is 'md', the code for the markdown table is saved
          into the Scribe `tables` attribute as a dictionary item.

        - If the output is 'img', the plot_table() function will be run
          to convert the table into an image file using matplotlib.

        Parameters:
        ----------
        d_var: str
            String variable which is the dependent variable in model

        output_type: str (default: 'md')
            specifies whether to output as an image .png file (img) or
            markdown (md) table.

        dtype: str (default: all)
            string variable specifying whether to output
            'categorical' ('c1'), detailed categorical ('c2'),
            'numerical' ('n') or 'all' data types

        dp: int
            Integer advising on number of decimal points for certain
            statistics (currently mean and std for numerical data types)

        show: boolean (default = True)
            Indicator on whether to show output if .png file is output.

        '''
        # make a copy of the initial data frame
        df = self.initial_df.copy()
        # check d_var is a field
        if d_var not in df.columns.to_list():
            print("Dependent Variable input not in data frame.")
            return
        # check if any categorical left if categories only chosen
        if (dtype in ('c1', 'c2', 'category') and df.drop(columns=d_var).
                select_dtypes(include='category').columns.empty is True):
            error = ("Unable to produce categorical table as no categorical"
                     "fields to summarise.")
            print(error)
            return
        # check whether if numerical and d_var taken out there are
        # fields left
        elif (dtype in ('n', 'numerical') and df.drop(columns=d_var).
                select_dtypes(exclude='category').columns.empty is True):
            error = ("Unable to produce numerical table as no numerical"
                     "fields to summarise.")
            print(error)
            return
        elif (dtype == 'all'
              and df.drop(columns=d_var).columns.empty is True):
            error = ("Unable to produce table as no other "
                     "fields available to summarise.")
            print(error)
            return

        if dtype == 'c2':
            self.summarise_categories(d_var, output_type=output_type)
        else:
            # variable to call final table depending on data type
            if dtype == 'c1' or dtype == 'category':
                final_output = 'categories_summary_table'

            elif dtype == 'n' or dtype == 'numerical':
                final_output = 'numerical_summary_table'
            else:
                final_output = 'summary_table_all'

            # retrieve friendly text using friendly_text() method
            df, columns, fr_names = self.get_friendly_text(df, d_var,
                                                           dtype='all')

            # Replace values in dependent variable column
            try:
                df[d_var] = df[d_var].astype(str)
                original = [str(i) for i in
                            self.scribe.column_mapping[d_var]
                            ['values_to_replace'].keys()]

                new_val = [str(i) for i in self.scribe.column_mapping[d_var]
                           ['values_to_replace'].values()]

                df[d_var].replace(original, new_val, inplace=True)
            except Exception as e:
                print(f"Using existing values for dependent variable. ({e})")

            # retrieve unique values in the dependent variable column
            unique_d_var_vals = df[d_var].unique().tolist()
            # replace column names with friendly text versions
            df.columns = fr_names
            # replace dependent variable to its friendly text name
            if (self.scribe.column_mapping is not None
                    and d_var in self.scribe.column_mapping.keys()):
                if (self.scribe.column_mapping[d_var]['friendly_text']
                        is not None):
                    d_var = self.scribe.column_mapping[d_var]['friendly_text']
            # if selected 'category' items only
            if dtype == 'c1' or dtype == 'category':
                # filter describe() method in pandas to category only
                grouped_describe = (df.groupby(d_var)
                                    .describe(include='category').T)
            # if selected 'numerical' items only
            elif dtype == 'n' or dtype == 'numerical':
                # filter to number and integer data types in describe() method
                grouped_describe = (df.groupby(d_var)
                                    .describe(include=[np.number,
                                                       np.integer]).T)
            # otherwise, include everything in describe() method
            else:
                grouped_describe = df.groupby(d_var).describe(include='all').T
            # reset index
            grouped_describe.reset_index(inplace=True)
            # rename MultiIndex columns to 'Variable' and 'Statistic'
            grouped_describe.rename(columns={'level_0': 'Variable',
                                             'level_1': 'Statistic'},
                                    inplace=True)
            # if data type is 'all', then limit to key metrics to avoid really
            # long table
            if dtype == 'all' or dtype == 'n' or dtype == 'numerical':
                stats_to_keep = ['count', 'unique', 'top', 'mean', 'std']

                grouped_describe = grouped_describe[grouped_describe
                                                    ['Statistic']
                                                    .isin(stats_to_keep)]

            # Pivot the DataFrame
            pivoted_df = grouped_describe.pivot_table(index='Variable',
                                                      columns='Statistic',
                                                      values=unique_d_var_vals,
                                                      aggfunc='first')

            # Flatten the MultiIndex columns
            pivoted_df.columns = [f'{col[0]}: {col[1]}'
                                  for col in pivoted_df.columns]

            # Reset the index to make 'level_0' a regular column
            pivoted_df.reset_index(inplace=True)

            # create new index
            new_idx = pivoted_df['Variable'].to_list()
            # create new list of columns
            col_names = pivoted_df.columns.to_list()
            # blank dictionary to log columns
            col_vals = {}
            # iterate through columns
            for col in col_names[1:]:
                # retrieve values for column
                vals = pivoted_df[col].to_list()
                # append values to col_vals list
                col_vals[col] = vals

            # create new data frame with new_idx and col_vals
            new_df = pd.DataFrame(index=new_idx, data=col_vals)
            # create markdown version
            new_df_md = new_df.to_markdown(index=True)

            # if markdown output_type, store in tables attribute of Scribe
            # object
            if output_type == 'md':
                self.tables[final_output] = new_df_md
            # if image file output, continue
            else:
                # reverse order (as image processing inputs bottom-up)
                new_df.sort_index(ascending=False,
                                  inplace=True)
                # use plot_table() function to produce image output
                self.plot_table(new_df, final_output, show=show, dp=dp)

    def get_friendly_text(self, df, d_var, dtype):
        '''
        Retrieves the friendly text for column names and values where
        specified in column_mappings in the Scribe object.

        Parameters:
        ----------
        scribe: Scribe object
            Object from Scribe class which holds all data summary and
            processing information.

        df: Pandas DataFrame
            data frame holding the dataset

        d_var: str
            dependent variable being used in analysis

        dtype: str
            specifies whether to prepare data for detailed categorical
            summary ('c') or any other summaries ('all')

        Returns:
        -------
        pd.Dataframe: data frame with any replaced values updated in it

        list: cols_to_use
            list of data frame columns

        list: friendly_names - list of 'friendly names' for columns in
        data frame

        '''
        # create empty lists for columns to use and friendly names
        friendly_names = []
        cols_to_use = []
        # add columns to a list
        cols = df.columns.to_list()
        # if no column mappings, return current column names and existing
        # data frame
        if (self.scribe.column_mapping == {}
                or self.scribe.column_mapping is None):
            if dtype == 'c':
                new_df = df.select_dtypes(include=['category', 'object'])
                new_df[d_var] = df[d_var]
                df = new_df
                cols = new_df.columns.to_list()
            return df, cols, cols
        # if dtype 'c' chosen
        elif dtype == 'c':
            cols = (df.select_dtypes(include=['category', 'object']).
                    columns.to_list())
            cols.append(d_var)
            # iterate through cols list
            for col in cols:
                # if column in column_mapping attribute of Scribe object
                if col in self.scribe.column_mapping.keys() and col != d_var:
                    # if no friendly_text in mapping, but the data type is
                    # categorical, append current column name to
                    # friendly_names as well as cols_to_use
                    if (self.scribe.column_mapping[col]['friendly_text']
                            is None):
                        friendly_names.append(col)
                        cols_to_use.append(col)
                    # if there is a friendly_text in mapping, append to
                    # friendly_names list and add column to cols_to_use
                    else:
                        friendly_names.append(self.scribe.column_mapping[col]
                                              ['friendly_text'])
                        cols_to_use.append(col)
                    # if there are values in 'values_to_replace' in mapping
                    if (self.scribe.column_mapping[col]['values_to_replace']
                            is not None):
                        # locate original value
                        original = [str(i) for i in
                                    self.scribe.column_mapping[col]
                                    ['values_to_replace']
                                    .keys()]
                        # locate replacement value
                        new_val = [str(i) for i in
                                   self.scribe.column_mapping[col]
                                   ['values_to_replace'].values()]
                        # replace values
                        df[col].replace(original, new_val, inplace=True)
                else:
                    cols_to_use
        # if selected dtype is 'all
        elif dtype == 'all' or dtype == 'n':
            # iterate through cols list
            for col in cols:
                # if column in column_mapping attribute of Scribe object
                if col in self.scribe.column_mapping.keys():
                    # if no friendly_text in mapping, add column to
                    # friendly_names list
                    if (self.scribe.column_mapping[col]['friendly_text']
                            is None):
                        friendly_names.append(col)
                    # if there is a friendly_text in mapping, append to
                    # friendly_names list
                    else:
                        friendly_names.append(self.scribe.column_mapping[col]
                                              ['friendly_text'])
                    # if there are values in 'values_to_replace' in mapping
                    if (self.scribe.column_mapping[col]['values_to_replace']
                            is not None):
                        # make dependent variable a string
                        df[d_var] = df[d_var].astype(str)
                        # locate original value
                        original = [str(i) for i in
                                    self.scribe.column_mapping[col]
                                    ['values_to_replace']
                                    .keys()]
                        # locate replacement value
                        new_val = [str(i) for i in
                                   self.scribe.column_mapping[col]
                                   ['values_to_replace'].values()]
                        # replace values
                        df[col].replace(original, new_val, inplace=True)
                # otherwise, add column to friendly_names list
                else:
                    friendly_names.append(col)
                    cols_to_use.append(col)
            else:
                cols_to_use = cols

        return df, cols_to_use, friendly_names


# other functions relevant to summary stats
def is_date(value, date_format="%Y-%m-%d %H:%M:%S"):
    '''
    Checks whether the value is in a particular date time format.

    Parameters:
    ----------
    value: str
        string variable which is to be checked it fits the date time
        format

    date_format: str (default: "%Y-%m-%d %H:%M:%S")
        string variable which specifies the date time format to check

    Returns:
    -------
    boolean: indicator of whether it matches (True) or does not (False)
    '''
    # try to match value with date format- if it works, then return True
    try:
        datetime.strptime(str(value), date_format)
        return True
    # if errors, return False
    except ValueError:
        return False


def format_date(value, input_format="%Y-%m-%d %H:%M:%S",
                output_format="%d/%m/%Y"):
    '''
    Formats the date field in a pandas Dataframe table.

    Parameters:
    ----------
    value: datetime object

    input_format: string (default: "%Y-%m-%d %H:%M:%S")
        datetime format of current value

    output_format: string (default: "%d/%m/%Y")
        datetime format for output

    Returns:
    -------
    string: formatted date string or original value if unable to update.
    '''
    try:
        # try to convert the value to a datetime object
        date_obj = datetime.strptime(str(value), input_format)

        # format the datetime object to the desired output format
        formatted_date = date_obj.strftime(output_format)

        # convert the formatted date to a string
        formatted_date_str = str(formatted_date)
        return formatted_date_str
    except ValueError:
        # if the conversion fails, return the original value
        return value
