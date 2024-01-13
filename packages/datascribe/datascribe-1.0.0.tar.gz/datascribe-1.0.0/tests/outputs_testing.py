'''
Unit testing for outputs.py file

'''

import unittest
import pandas as pd
import os
import numpy as np
from PIL import Image

from datascribe.scribe import Scribe
from datascribe.outputs import (convert_md_to_docx,
                                tidy_up_images)


class SummaryStatsTest(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame({
            'Variable1': [10, 20, 30],
            'Variable2': ['A', 'B', 'A'],
            'Variable3': [1.1, 2.2, 3.3]})
        dir = 'tests'
        self.s = Scribe(df, dir)
        self.s.model.y_pred = np.array([0, 0, 0, 1])
        self.s.model.splitted_data['y_test'] = pd.Series([0, 0, 1, 1])

    def test_word_exists(self):
        '''
        Tests whether:
        - md file produced
        - docx file created
        - md file removed after docx creation

        '''
        md_file_path = 'tests/UnitTesting.md'
        doc_file_path = 'tests/UnitTesting.docx'
        with open(md_file_path, "w", encoding="utf-8") as f:
            # write the various input into the file
            f.write("This is a test document")
        f.close()
        self.assertTrue(os.path.exists(md_file_path),
                        f"Doc file '{md_file_path}' does not exist.")
        convert_md_to_docx(md_file_path, doc_file_path)
        self.assertTrue(os.path.exists(doc_file_path),
                        f"Doc file '{doc_file_path}' does exist.")
        self.assertFalse(os.path.exists(md_file_path),
                         f"Doc file '{md_file_path}' does not exist.")

    def test_tidy_up_image_folder_empty(self):
        '''
        tests whether the image folder is removed as empty

        '''
        img_file_pth = 'tests/images'
        if not os.path.exists(img_file_pth):
            os.makedirs(img_file_pth)
            print(f"Directory '{img_file_pth}' created.")
        else:
            print(f"Directory '{img_file_pth}' already exists.")
        self.assertTrue(os.path.exists(img_file_pth),
                        f"Doc file '{img_file_pth}' does not exist.")
        tidy_up_images(self.s, img_file_pth, True)
        self.assertFalse(os.path.exists(img_file_pth),
                         f"Doc file '{img_file_pth}' does not exist.")

    def test_tidy_up_image_folder_not_empty_keep(self):
        '''
        tests whether the image folder is not removed when user wishes
        to keep images

        '''
        img_file_pth = 'tests/images'
        if not os.path.exists(img_file_pth):
            os.makedirs(img_file_pth)
            print(f"Directory '{img_file_pth}' created.")
        else:
            print(f"Directory '{img_file_pth}' already exists.")

        img = Image.new("RGB", (800, 1280), (255, 255, 255))
        img_file = f"{img_file_pth}/image.png"
        img.save(img_file, "PNG")
        self.assertTrue(os.path.exists(img_file_pth),
                        f"Image file '{img_file_pth}' does not exist.")
        tidy_up_images(self.s, img_file_pth, True)
        self.assertTrue(os.path.exists(img_file_pth),
                        f"Doc file '{img_file_pth}' does not exist.")

    def test_tidy_up_image_folder_not_empty_remove(self):
        '''
        tests whether the image folder is removed when user wishes to
        remove images

        '''
        img_file_pth = 'tests/images'
        if not os.path.exists(img_file_pth):
            os.makedirs(img_file_pth)
            print(f"Directory '{img_file_pth}' created.")
        else:
            print(f"Directory '{img_file_pth}' already exists.")

        img = Image.new("RGB", (800, 1280), (255, 255, 255))
        img_file = f"{img_file_pth}/image.png"
        img.save(img_file, "PNG")
        self.assertTrue(os.path.exists(img_file_pth),
                        f"Doc file '{img_file_pth}' does not exist.")
        tidy_up_images(self.s, img_file_pth, False)
        self.assertFalse(os.path.exists(img_file_pth),
                         f"Doc file '{img_file_pth}' does not exist.")


if __name__ == '__main__':
    unittest.main()
