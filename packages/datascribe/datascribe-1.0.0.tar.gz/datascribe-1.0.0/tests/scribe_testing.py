'''
Unit testing for scribe.py file

'''
import unittest
import pandas as pd
import os
from PIL import Image
from datascribe.scribe import Scribe


class ScribeTest(unittest.TestCase):

    def setUp(self):
        initial_df = pd.DataFrame({
            'Variable1': [10, 20, 30, 10, 20],
            'Variable2': ['A', 'B', 'A', 'A', 'A'],
            'Variable3': [1.1, 2.2, 3.3, 4.4, 5.5]})
        output_dir = r'tests'
        self.s = Scribe(initial_df, output_dir)

    def test_dir_not_exist(self):
        '''
        tests whether a directory which does not exist is created with
        make_dir method

        '''
        self.s.dir = 'tests/unittest/ahh'
        self.s.make_dir()

        self.assertTrue(os.path.exists(self.s.dir),
                        f"Directory '{self.s.dir}' does not exist.")
        self.assertEqual({}, self.s.visuals_loc)

    def test_clean_up_images_removes(self):
        '''
        check folder and images removed when clean_up_images method
        called

        check visuals_loc dict becomes empty when actioned

        '''
        img_dir = f"{self.s.dir}/images"
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img = Image.new("RGB", (800, 1280), (255, 255, 255))
        img_file = f"{img_dir}/image.png"
        img.save(img_file, "PNG")
        self.s.visuals_loc = {'unittest_image': img_file}
        self.assertTrue(os.path.exists(img_dir),
                        f"Directory '{img_dir}' does not exist.")
        self.s.clean_up_images()
        self.assertFalse(os.path.exists(img_dir),
                         f"Directory '{img_dir}' does not exist.")

    def test_mappings_created(self):
        '''
        checks whether the column mappings are processed using
        create_mappings method

        '''
        cols = self.s.summaries.initial_df.columns.to_list()
        col_names = ['New Name 1', 'New name 2', 'New name 3']
        vals_to_rep = {'Variable1': {20: 2, 10: 1, 30: 3}}
        self.s.create_mappings(cols, friendly_names=col_names,
                               friendly_values=vals_to_rep)
        self.assertNotEqual({}, self.s.column_mapping)

    def test_output_process_docx(self):
        '''
        checks whether a word .docx file is output to relevant file path

        '''
        file_name = 'unittesting'
        file_path = f'{self.s.dir}/{file_name}.docx'
        self.s.output_process(file_name, file_type='docx')
        self.assertTrue(os.path.exists(file_path),
                        f"File path '{file_path}' does not exist.")

    def check_output_process_md(self):
        '''
        checks whether a markdown .md file is output to relevant file
        path

        '''
        file_name = 'unittesting'
        file_path = f'{self.s.dir}/{file_name}.md'
        self.s.output_process(file_name, file_type='md')
        self.assertTrue(os.path.exists(file_path),
                        f"File path '{file_path}' does not exist.")


if __name__ == '__main__':
    unittest.main()
