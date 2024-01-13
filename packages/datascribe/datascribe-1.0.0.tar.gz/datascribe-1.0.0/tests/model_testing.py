'''
Unit testing for model.py file

'''

import unittest
import numpy as np
from sklearn.datasets import load_iris  # to test model

from datascribe.scribe import Scribe


class ModelTests(unittest.TestCase):
    def setUp(self) -> None:
        output_dir = r'images/tests'
        # initial dataset dummy for Scribe instance (actual model from
        # load_iris from sklearn)
        data = {
            'Category': [9, 2, 8, 6, 9, 2, 8, 6, 3, 1],
            'Value1': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'Value2': [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
            'Target': [1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
        }
        self.X, self.y = load_iris(return_X_y=True)
        self.s = Scribe(data, output_dir)

        self.params = {"random_state": [42], "max_iter": [5000],
                       "solver": ["lbfgs", "sag", "saga", "newton-cg"]}

    def test_k_fold(self):
        '''
        tests that the k_fold method in the class processes a Stratified
        K fold by checking that it produces the number of expected folds

        '''
        n_splits = 5
        self.s.model.k_fold(n_splits=n_splits)
        num_folds = 0
        for i, (train_index,
                test_index) in enumerate(self.s.model.kfold
                                         .split(self.X, self.y)):
            num_folds += 1
        self.assertEqual(n_splits, num_folds)

    def test_split_dataset(self):
        '''
        Checks that the the split_dataset method in the class loads four
        np.ndarrays into the class' splitted_data attribute

        '''
        self.s.model.split_dataset(self.X, self.y, stratify=self.y)
        self.assertIsInstance(self.s.model.splitted_data['X_train'],
                              np.ndarray)
        self.assertIsInstance(self.s.model.splitted_data['X_test'],
                              np.ndarray)
        self.assertIsInstance(self.s.model.splitted_data['y_train'],
                              np.ndarray)
        self.assertIsInstance(self.s.model.splitted_data['y_test'],
                              np.ndarray)


    def test_regression_model(self):
        '''
        tests whether the expected regression model (GridSearchCV) is
        created

        '''
        result = None
        self.s.model.regression_model(self.params)
        for k, v in self.s.model.__dict__.items():
            if k == 'model':
                if 'GridSearchCV' in str(v):
                    result = 'GridSearchCV'
        self.assertEqual(result, "GridSearchCV")

    def test_fit(self):
        '''
        tests whether the test dataset can be fitted to the model or not
        - if the method errors, error message printed and test fails
        '''
        self.s.model.split_dataset(self.X, self.y, stratify=self.y)
        self.s.model.regression_model(params=self.params)
        try:
            self.s.model.fit()
            result = True
        except Exception as e:
            error, result = e, False
            print(f"Error message: {error}")
        self.assertTrue(result)

    def test_predict(self):
        '''
        tests whether the the fit method in Model class produces a
        np.ndarray into the y_pred attribute

        '''
        n_splits = 2
        self.s.model.k_fold(n_splits=n_splits)
        self.s.model.split_dataset(self.X, self.y, stratify=self.y)
        self.s.model.regression_model(params=self.params)
        self.s.model.fit()
        self.s.model.predict()
        self.assertTrue(isinstance(self.s.model.y_pred, np.ndarray))

    def test_check_model_exists_false(self):
        '''
        tests whether the model' check_model_exists method returns False
        when there is no model in class

        '''
        self.assertFalse(self.s.model.check_model_exists(),
                         'Class doesn\'t have a saved model')

    def test_check_model_exists_true(self):
        '''
        tests whether the model' check_model_exists method returns True
        when there is a model in model_type attribute

        '''
        self.s.model.model_type = 'LR_GCV_skf'
        self.assertTrue(self.s.model.check_model_exists(),
                        'Class doesn\'t have a saved model')

    def test_model_commentary(self):
        '''
        tests whether the model commentary is produced when the
        model_type attribute is not None

        '''
        self.s.model.model_type = 'LR_GCV_skf'
        self.s.model.split = 0.2
        self.s.model.k_num = 5
        text = self.s.model.model_commentary()
        self.assertIsNotNone(text)


if __name__ == '__main__':
    unittest.main()
