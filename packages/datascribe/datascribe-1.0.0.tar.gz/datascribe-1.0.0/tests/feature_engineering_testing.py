'''
Unit testing for feature_engineering.py

'''

import unittest
import pandas as pd
from sklearn.datasets import load_iris

from datascribe.scribe import Scribe


class FeatureEngineeringTests(unittest.TestCase):

    def setUp(self):
        self.output_dir = r'tests'
        data = {
            'Category': ['A', None, 'C', 'A', 'B', 'A', 'C', 'B', 'C', 'A'],
            'Value1': [10, 20, 30, 40, 50, 60, 70, 80, 90, None],
            'Value2': [5, 15, 25, 45, 45, None, 65, 75, 85, 95]
        }
        self.df = pd.DataFrame(data)
        self.s = Scribe(self.df, self.output_dir)

    def test_imputing_numeric_mean(self):
        '''
        tests whether the imputing numeric mean function returns the
        data frame as expected and updates the imputed_mean_cols
        attribute in class

        '''
        cols = ['Value1']
        result_df = (self.s.preprocessing.
                     imputing_numeric_mean(self.df, columns=cols))
        expected_df = pd.DataFrame({'Category': ['A', None, 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, 50],
                                    'Value2': [5, 15, 25, 45, 45, None, 65, 75,
                                               85, 95]})
        self.assertIn('Value1', self.s.preprocessing.imputed_mean_cols)
        # Add assertions to check if imputed_mean_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_numeric_median(self):
        '''
        tests whether the imputing numeric median function returns the
        data frame as expected and updates the imputed_median_cols
        attribute in class

        '''
        column_names = ['Value1']
        result_df = (self.s.preprocessing.
                     imputing_numeric_median(self.df, columns=column_names))
        expected_df = pd.DataFrame({'Category': ['A', None, 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, 50],
                                    'Value2': [5, 15, 25, 45, 45, None, 65, 75,
                                               85, 95]})
        self.assertIn('Value1', self.s.preprocessing.imputed_median_cols)
        # Add assertions to check if imputed_median_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_numeric_mode(self):
        '''
        tests whether the imputing numeric mode function returns the
        data frame as expected and updates the imputed_mode_cols
        attribute in class
        '''
        column_names = ['Value2']
        result_df = (self.s.preprocessing.
                     imputing_numeric_mode(self.df, columns=column_names))
        expected_df = pd.DataFrame({'Category': ['A', None, 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, None],
                                    'Value2': [5, 15, 25, 45, 45, 45, 65, 75,
                                               85, 95]})
        self.assertIn('Value2', self.s.preprocessing.imputed_mode_cols)
        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_numeric_constant(self):
        '''
        tests whether the imputing numeric constant function returns the
        data frame as expected and updates the imputed_constant_cols
        attribute in class

        '''
        column_names = ['Value2']
        constant_value = 10
        result_df = (self.s.preprocessing.
                     imputing_numeric_constant(self.df, columns=column_names,
                                               constant=constant_value))
        expected_df = pd.DataFrame({'Category': ['A', None, 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, None],
                                    'Value2': [5, 15, 25, 45, 45, 10, 65, 75,
                                               85, 95]})
        self.assertIn('Value2', self.s.preprocessing.imputed_constant_cols)
        (self.assertEqual(constant_value,
                          [value for key, value in
                           self.s.preprocessing.constant_vals.items()
                           if key in column_names][0]))
        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_non_numeric_constant(self):
        '''
        tests whether the imputing non-numeric constant function returns
        the data frame as expected and updates the imputed_constant_cols
        attribute in class

        '''
        column_names = ['Category']
        constant_value = 'missing'
        result_df = (self.s.preprocessing.
                     imputing_non_numeric_constant(self.df,
                                                   columns=column_names,
                                                   constant=constant_value))
        expected_df = pd.DataFrame({'Category': ['A', 'missing', 'C', 'A', 'B',
                                                 'A', 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, None],
                                    'Value2': [5, 15, 25, 45, 45, None, 65, 75,
                                               85, 95]})
        self.assertIn('Category', self.s.preprocessing.imputed_constant_cols)
        self.assertEqual(constant_value,
                         [value for key, value in
                          self.s.preprocessing.constant_vals.items()
                          if key in column_names][0])

        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_non_numeric_mode(self):
        '''
        tests whether the imputing non-numeric constant function returns
        the data frame as expected and updates the imputed_mode_cols
        attribute in class

        '''
        column_names = ['Category']
        result_df = (self.s.preprocessing.
                     imputing_non_numeric_mode(self.df, columns=column_names))
        expected_df = pd.DataFrame({'Category': ['A', 'A', 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, None],
                                    'Value2': [5, 15, 25, 45, 45, None, 65, 75,
                                               85, 95]})
        self.assertIn('Category', self.s.preprocessing.imputed_mode_cols)
        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_backwardfill(self):
        '''
        tests whether the imputing backwardfill method returns
        the data frame as expected and updates the imputed_backfill_cols
        attribute in class

        '''
        column_names = ['Category', 'Value2']
        result_df = (self.s.preprocessing.
                     imputing_backwardfill(self.df, columns=column_names))
        expected_df = pd.DataFrame({'Category': ['A', 'C', 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, None],
                                    'Value2': [5, 15, 25, 45, 45, 65, 65, 75,
                                               85, 95]})
        self.assertEqual(column_names,
                         self.s.preprocessing.imputed_backfill_cols)
        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df, expected_df,
                                      check_dtype=False, check_exact=False)

    def test_imputing_forwardfill(self):
        '''
        tests whether the imputing forwardfill method returns
        the data frame as expected and updates the
        imputed_forwardfill_cols attribute in class

        '''
        column_names = ['Category', 'Value1']
        result_df = (self.s.preprocessing.
                     imputing_forwardfill(self.df, columns=column_names))
        expected_df = pd.DataFrame({'Category': ['A', 'A', 'C', 'A', 'B', 'A',
                                                 'C', 'B', 'C', 'A'],
                                    'Value1': [10, 20, 30, 40, 50, 60, 70, 80,
                                               90, 90],
                                    'Value2': [5, 15, 25, 45, 45, None, 65, 75,
                                               85, 95]})
        self.assertEqual(column_names,
                         self.s.preprocessing.imputed_forwardfill_cols)
        # Add assertions to check if imputed_mode_cols attribute is
        # updated correctly
        pd.testing.assert_frame_equal(result_df,
                                      expected_df,
                                      check_dtype=False,
                                      check_exact=False)

    def test_dummy_encoder(self):
        """
        Test dummy_encoder method in Preprocess class.

        Ensure that non-numeric columns are encoded correctly.
        """
        # Test data
        data = {'Category': ['A', 'B', 'A', 'C', 'B'],
                'Value1': [10, 20, 30, 40, 50]}
        self.df = pd.DataFrame(data)
        self.scribe = Scribe(self.df, self.output_dir)

        # Call the method
        result = self.s.preprocessing.dummy_encoder(self.df.copy(),
                                                    columns=['Category'])
        result_cols = result.columns.to_list()
        self.assertNotIn('Category', result_cols)
        expected_new_cols = ['Category_A', 'Category_B', 'Category_C']
        for col in expected_new_cols:
            self.assertIn(col, result_cols)

    def test_scale_categories(self):
        '''
        tests whether the scale_categories method in class creates
        the expected pandas Dataframe result and in
        all_categories_scaled attribute

        '''
        mapping = {'A': 1, 'B': 2, 'C': 3}
        column = 'Category'

        # Expected scaled result
        expected_result = pd.DataFrame({'Value1': [10, 20, 30, 40, 50, 60,
                                                   70, 80, 90, 100],
                                        'Value2': [5, 15, 25, 35, 45, 55,
                                                   65, 75, 85, 95],
                                        'Category': [0.0, 0.5, 1.0, 0.0,
                                                     0.5, 0.0, 1.0, 0.5,
                                                     1.0, 0.0]})

        # Call the method
        df = (self.s.preprocessing.
              imputing_non_numeric_constant(self.df, constant='B',
                                            columns=[column]))
        result = self.s.preprocessing.scale_categories(df, mapping, column)
        # Assert the result
        self.assertIn(column, self.s.preprocessing.all_categories_scaled)
        pd.testing.assert_series_equal(result[column],
                                       expected_result[column])

    def test_standardise_data(self):
        '''
        tests whether the standardise data method runs and changes the
        boolean attribute data_standardise_check becomes True

        '''
        X, y = load_iris(return_X_y=True)
        X = pd.DataFrame(X)
        X_train = X.sample(frac=0.7)
        X_test = X.drop(X_train.index, axis=0)
        result_train, result_test = (self.s.preprocessing.
                                     standardise_data(X_train, X_test))
        self.assertTrue(self.s.preprocessing.data_standardised_check)

    def test_imputing_commentary(self):
        '''
        tests whether the commentary for columns with imputed values
        is returned as a string.

        '''
        col = ['Category']
        self.s.preprocessing.imputing_non_numeric_constant(self.df,
                                                           columns=col)
        result = self.s.preprocessing.imputing_commentary()
        self.assertIsInstance(result, str)

    def test_impute_text_formatter(self):
        '''
        tests whether the impute text formatter returns expected text

        '''
        fields = 'Category A'
        method = 'mode value'
        result = self.s.preprocessing.impute_text_formatter(fields, method)
        expected = "Null values in Category A were imputed with the "\
                   "mode value."
        self.assertEqual(result, expected)

    def test_check_imputes_step(self):
        '''
        tests whether False appears when no items in imputed attribute
        lists and then whether it returns True if there are items

        '''
        result_1 = self.s.preprocessing.check_imputes_step()
        self.assertFalse(result_1)
        self.s.preprocessing.imputed_constant_cols = ['Cat A']
        result_2 = self.s.preprocessing.check_imputes_step()
        self.assertTrue(result_2)

    def test_dummy_encoding_commentary(self):
        '''
        tests whether a string is produces if dummy coding has taken
        place

        '''
        # test data
        data = {'Category': ['A', 'B', 'A', 'C', 'B'],
                'Value1': [10, 20, 30, 40, 50]}
        self.df = pd.DataFrame(data)
        self.scribe = Scribe(self.df, self.output_dir)
        self.s.preprocessing.dummy_encoder(self.df.copy(),
                                           columns=['Category'])
        result = self.s.preprocessing.dummy_encoding_commentary()
        self.assertIsNotNone(result)

    def test_dummy_encoding_check(self):
        '''
        tests whether check_dummy_encoding returns False when none
        taken place and then True after it has taken place

        '''
        result_1 = self.s.preprocessing.check_dummy_encoding()
        self.assertFalse(result_1)

        # test data
        data = {'Category': ['A', 'B', 'A', 'C', 'B'],
                'Value1': [10, 20, 30, 40, 50]}
        self.df = pd.DataFrame(data)
        self.scribe = Scribe(self.df, self.output_dir)
        self.s.preprocessing.dummy_encoder(self.df.copy(),
                                           columns=['Category'])

        result_2 = self.s.preprocessing.check_dummy_encoding()
        self.assertTrue(result_2)

    def test_cat_scaling_commentary(self):
        '''
        tests whether the commentary is produces in
        cat_scaling_commentary method in class if scaling completed

        '''
        mapping = {'A': 1, 'B': 2, 'C': 3}
        column = 'Category'

        df = (self.s.preprocessing.
              imputing_non_numeric_constant(self.df, constant='B',
                                            columns=[column]))
        self.s.preprocessing.scale_categories(df, mapping, column)

        result = self.s.preprocessing.cat_scaling_commentary()
        expected = "The order of Category was retained by mapping the "\
                   "order of the values and using the `MinMaxScaler()`"\
                   " method from the `sklearn` package to create a scale "\
                   "between 0 and 1."
        self.assertEqual(result, expected)

    def test_check_cats_scaled(self):
        '''
        tests whether the check_cats_scaled method in class returns
        False when it has not taken place and True when it has

        '''
        result_1 = self.s.preprocessing.check_cats_scaled()
        self.assertFalse(result_1)

        mapping = {'A': 1, 'B': 2, 'C': 3}
        column = 'Category'

        # Call the method
        df = (self.s.preprocessing.
              imputing_non_numeric_constant(self.df, constant='B',
                                            columns=[column]))
        self.s.preprocessing.scale_categories(df, mapping, column)

        result_2 = self.s.preprocessing.check_cats_scaled()
        self.assertTrue(result_2)


if __name__ == '__main__':
    unittest.main()
