# import numpy as np
import os
# import cv2
# from pathlib import Path
import pandas as pd


def get_image_names(root_dir, base_path=None, csv_writter=None):
    """
    if csv_writter is not None, write the file paths to csv file
    example: filenames = get_image_names(path, base_path=path, csv_writter={'image_name': 'image name'})
    """
    file_paths = []
    for root, directories, files in os.walk(root_dir):
        for filename in files:
            absolute_path = os.path.join(root, filename)
            if base_path is not None:
                # base_path = root_dir
                name = os.path.relpath(absolute_path, base_path)
            else:
                name = absolute_path
            file_paths.append(name)
    if csv_writter is not None:
        df = pd.DataFrame({csv_writter['image_name']: file_paths})
        return df
    else:
        return file_paths


# if __name__ == '__main__':
#     aa = get_image_names(path, base_path=path)
#     bb = 0
