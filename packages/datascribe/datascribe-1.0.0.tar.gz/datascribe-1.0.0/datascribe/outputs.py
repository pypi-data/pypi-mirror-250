'''
Stores the functions for preparing the various logged text, images and
tables for the final output.

'''


import pypandoc
import os
import shutil


def convert_md_to_docx(md_file_path, docx_file_path):
    '''
    Converts markdown file (.md) to word document (.docx)

    Parameters:
    ----------
    md_file_path: string
        Directory file path for markdown file

    docx_file_path: string
        Directory file path for docx file

    '''
    # Specify the output format as docx
    output_format = 'docx'

    # Convert Markdown to Word document
    pypandoc.convert_file(md_file_path, output_format,
                          outputfile=docx_file_path)
    os.remove(md_file_path)


def tidy_up_images(scribe, img_file_path, output_img_files=True):
    '''
    Removes image files/folder no longer required from output
    (specifified by the user) location.

    Parameters:
    ----------
    img_file_path: string
        File directory path where all images for output have been
        saved.

    output_img_files: boolean (default=True)
        indicates whether to keep files or not (default is to keep/True)

    '''
    # if user has advised they do not want separate image files in the
    # output, remove folder and its contents
    if output_img_files is False:
        try:
            shutil.rmtree(img_file_path)
            # remove from log
            scribe.visuals_loc = {}
        except Exception as e:
            print(f"Unable to remove images.  Check folder exists: {e}")

    else:
        try:
            # get a list of items in the directory
            dir_contents = os.listdir(img_file_path)

            # check if the directory contains any files
            files_exist = any(os.path
                              .isfile(os.path.join(img_file_path,
                                                   item)) for item
                              in dir_contents)

            # if there are image files, advise where they are stored
            if files_exist:
                print(f"Separate image files can be found "
                      f"here: {img_file_path}")

            # if no image files, remove the empty folder
            else:
                shutil.rmtree(img_file_path)
        except Exception as e:
            print(f"Unable to find images.  Check folder exists: {e}")
