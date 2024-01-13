import unittest
import pandas as pd
import os
from datascribe.scribe import Scribe


class WorkflowTesting(unittest.TestCase):
    def setUp(self):
        initial_df = pd.DataFrame({
            'Variable1': [10, 20, 30, 10, 20],
            'Variable2': ['A', 'B', 'A', 'A', 'A'],
            'Variable3': [1.1, 0.0, 3.3, 4.4, 5.5],
            'Variable4': ['y', 'n', 'y', 'n', 'y'],
            'Variable5': [1, 2, 3, 4, 5]})
        output_dir = r'tests'
        self.s = Scribe(initial_df, output_dir)

        # preprocessing for demo
        self.df = initial_df.copy()
        self.df = self.s.preprocessing.imputed_median_cols.append('Variable5')
        self.df = self.s.preprocessing.imputed_mean_cols.append('Variable3')
        self.df = (self.s.preprocessing.imputed_backfill_cols
                   .append('Variable2'))
        self.df = self.s.preprocessing.dummy_coding_cols.append('Variable2')

        # add model info
        self.s.model.model_type = 'LR_GCV_skf'
        self.s.model.k_num = 5
        self.s.model.split = 0.2

    def test_get_nodes(self):
        '''
        test that nodes are stored in attribute after calling method
        '''
        self.s.workflow.get_nodes()
        result = len(self.s.workflow.nodes)
        expected = 8
        self.assertEqual(result, expected)

    def test_workflow_image_exists(self):
        '''
        checks whether the workflow image file is saved as expected when
        calling create_workflow_image method

        checks whether image name and location saved in visuals_loc
        attribute of Scribe class

        '''
        image_output_file = f'{self.s.dir}/images/model workflow.png'
        self.s.workflow.create_workflow_image()
        self.assertTrue(os.path.exists(image_output_file),
                        f"Image file '{image_output_file}' does not exist.")
        self.assertTrue('workflow' in self.s.visuals_loc.keys())

    def test_model_nodes_added(self):
        '''
        tests whether the model nodes for LR_GCV_skf type load on
        get_model_nodes method

        '''
        list_of_nodes = ['3.1', '4.1', '4.2', '4.3', '5.1']
        self.s.workflow.get_model_nodes()
        for node in list_of_nodes:
            self.assertTrue(node in self.s.workflow.nodes.keys())

    def test_model_nodes_no_model(self):
        '''
        tests whether the get_model_nodes returns False if no model type
        in model_type attribute of Model class

        '''
        self.s.model.model_type = None
        result = self.s.workflow.get_model_nodes()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
