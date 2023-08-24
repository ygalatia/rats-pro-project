from django.test import TestCase
from .views import read_csv_as_df, filter_by_countries, left_merge_dataframe, rename_fields, generate_file_name, get_save_path
import pandas as pd

# Create your tests here.
class DatasetCollationTests(TestCase):
    def init_test():
        return "Data Collation App Test"
    
    def test_filter_by_countries(self):
        data = {'id': [1, 2, 3], 'first_name':['Anntoine', 'Brook', 'Casey'], 'country':['France', 'United Kingdom', 'Netherlands']}
        df = pd.DataFrame(data)

        selected_countries = ['Netherlands', 'United Kingdom']
        filtered_df = filter_by_countries(df, selected_countries)

        self.assertNotIn('Anntoine', filtered_df['first_name'])
        self.assertEqual(len(filtered_df), 2)

