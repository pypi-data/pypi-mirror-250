import unittest
import pandas as pd
import os

from datascribe.scribe import Scribe
from datascribe.summary_stats import (is_date,
                                      format_date)


class SummaryStatsTest(unittest.TestCase):

    def setUp(self):
        initial_df = pd.DataFrame({
            'Variable1': [10, 20, 30, 10, 20],
            'Variable2': ['A', 'B', 'A', 'A', 'A'],
            'Variable3': [1.1, 2.2, 3.3, 4.4, 5.5]

        })
        output_dir = r'tests'
        self.s = Scribe(initial_df, output_dir)

    def test_plot_table(self):
        '''
        tests whether the plot table method creates an image file output

        '''
        data = pd.DataFrame({
            'Variable': ['A', 'B', 'C'],
            'Category1': [10, 20, 30],
            'Category2': [40, 50, 60]
        })
        data.set_index('Variable', inplace=True)
        filename = 'test_plot_table'
        self.s.summaries.plot_table(data, filename)

        # Check if the file exists
        image_path = f'{self.s.dir}/images/{filename}.png'
        self.assertTrue(os.path.exists(image_path),
                        f"Image file '{image_path}' does not exist.")

    def test_summarise_categories_false(self):
        '''
        tests whether a categorical table does not load into tables
        attribute if no categories available

        '''
        print("summaries categories test")
        d_var = 'Variable2'  # only categorical field
        self.s.summaries.summarise_categories(d_var=d_var, output_type='md')
        result = 'detailed_categories_summary_table'
        self.assertFalse(result in self.s.summaries.tables.keys())

    def test_summarise_categories_true(self):
        '''
        tests whether a categorical table loads into tables
        attribute if one category available
        '''
        d_var = 'Variable1'
        self.s.summaries.initial_df['Variable2'].astype('category')
        print(self.s.summaries.initial_df.info())
        self.s.summaries.summarise_categories(d_var=d_var, output_type='md')
        result = 'detailed_categories_summary_table'
        self.assertTrue(result in self.s.summaries.tables.keys())

    def test_summarise_numerical(self):
        d_var = 'Variable2'
        self.s.summaries.summary_table(d_var, dtype='n', output_type='md',
                                       dp=2)
        result = 'numerical_summary_table'
        self.assertTrue(result in self.s.summaries.tables.keys())

    def test_summarise_all(self):
        d_var = 'Variable2'
        self.s.summaries.summary_table(d_var, dtype='all', output_type='md',
                                       dp=2)
        result = 'summary_table_all'
        self.assertTrue(result in self.s.summaries.tables.keys())

    def test_is_date(self):
        date_str = '2022-01-01 12:34:56'
        result = is_date(date_str)
        self.assertTrue(result)

        not_date_str = 'Not a date'
        result = is_date(not_date_str)
        self.assertFalse(result)

    def test_format_date(self):
        date_str = '2022-01-01 12:34:56'
        result = format_date(date_str)
        self.assertEqual(result, '01/01/2022')
        not_date_str = 'Not a date'
        result = format_date(not_date_str)
        self.assertEqual(result, not_date_str)

    def test_check_get_friendly_text(self):
        '''
        Checks whether the column mapping method works

        '''
        data = pd.DataFrame({
            'Variable': ['A', 'B', 'C'],
            'Category1': [10, 20, 30],
            'Category2': [40, 50, 60]})
        df, cols, names = self.s.summaries.get_friendly_text(data,
                                                             'Variable',
                                                             all)
        self.assertListEqual(data.columns.to_list(), names)

    def test_check_get_friendly_text_maps(self):
        '''
        Checks whether the column mapping method works with mapping

        '''
        col = ['Variable', 'Category1', 'Category2']
        alt = ['Letters', 'First 30', 'Second 30']
        self.s.create_mappings(col, friendly_names=alt)
        data = pd.DataFrame({
            'Variable': ['A', 'B', 'C'],
            'Category1': [10, 20, 30],
            'Category2': [40, 50, 60]})
        df, cols, names = self.s.summaries.get_friendly_text(data, 'Category1',
                                                             'c')
        self.assertNotEqual(cols, names)


if __name__ == '__main__':
    unittest.main()
