from django.test import TestCase
from .views import read_csv_as_df, filter_by_countries, left_merge_dataframe, rename_fields, generate_file_name, get_save_path

class DatasetCollationTests(TestCase):
    def init_test():
        return "Data Collation App Test"

# Create your tests here.
