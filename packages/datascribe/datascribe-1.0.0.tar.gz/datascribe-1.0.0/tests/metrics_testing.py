import unittest
import numpy as np
import pandas as pd
import os
from datascribe.scribe import Scribe


class TestMetrics(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame({
            'Variable1': [10, 20, 30],
            'Variable2': ['A', 'B', 'A'],
            'Variable3': [1.1, 2.2, 3.3]})
        dir = 'tests'
        self.s = Scribe(df, dir)
        self.s.model.y_pred = np.array([0, 0, 0, 1])
        self.s.model.splitted_data['y_test'] = pd.Series([0, 0, 1, 1])

    def test_MAE(self):
        '''
        testing the result of the mean absolute error method.

        '''
        result = self.s.metrics.mae()
        self.assertAlmostEqual(result, 0.25, places=2)

    def test_MSE(self):
        '''
        testing the result of the mean standard error method.

        '''
        result = self.s.metrics.mse()
        self.assertAlmostEqual(result, 0.25, places=2)

    def test_r2score(self):
        '''
        testing the result of the r2 score method.

        '''
        result = self.s.metrics.r2score()
        print(result)
        self.assertEqual(result, 0.0)

    def test_confusionmatrix_shape(self):
        '''
        testing the shape of the resulting confusion matrix is correct.

        '''
        self.s.metrics.confusionmatrix()
        result = self.s.metrics.metrics_methods['confusion matrix']
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (2, 2))

    def test_confusionmatrix_result(self):
        '''
        testing the result of the confusion matrix is correct

        '''
        self.s.metrics.confusionmatrix()
        result = self.s.metrics.metrics_methods['confusion matrix']
        expected = np.array([[2, 0], [1, 1]], dtype='int64')
        self.assertTrue(np.array_equal(result, expected))

    def test_roc_image(self):
        '''
        testing the ROC image is output to image folder
        '''
        self.s.metrics.confusionmatrix()
        output_file = "tests/images/confusion matrix.png"
        self.assertTrue(os.path.exists(output_file))

    def test_ROC_result(self):
        '''
        testing the AUROC result of roc() method returns correct result.
        '''
        self.s.metrics.roc()
        result = self.s.metrics.metrics_methods['roc curve']
        self.assertTrue(isinstance(result, float))

    def confusion_matrix_image(self):
        '''
        testing the confusion matrix outputs to mage folder

        '''
        output_file = "tests/images/roc curve.png"
        self.assertTrue(os.path.exists(output_file))

    def test_metrics_commentary(self):
        '''
        testing the metric commentary for a metric is in the string
        output for all commentary

        '''
        self.s.metrics.mae()
        commentary = self.s.metrics.metrics_commentary()
        self.assertTrue("mean absolute error" in commentary)

    def test_check_metrics_step(self):
        '''
        testring the check metrics method returns True if metric
        performed

        '''
        output = self.s.metrics.mae()
        self.assertTrue(output in
                        self.s.metrics.metrics_methods.values())

    def test_check_metrics_step_false(self):
        '''
        testing the check metrics method returns False if no metrics
        have been performed

        '''
        key = 'mean absolute error'
        self.assertFalse(key in self.s.metrics.metrics_methods.keys())

    def test_prec_rec_f1_score(self):
        '''
        testing the output of the precision, recall and f1 score method
        is correct shape

        '''
        self.s.metrics.prec_rec_f1_score()
        result = (self.s.metrics.
                  metrics_methods['precision, recall, f1 score and support'])
        self.assertIsInstance(result, tuple)
        shape = [len(tup) for tup in result]
        self.assertEqual(shape, [2, 2, 2, 2])


if __name__ == '__main__':
    unittest.main()
