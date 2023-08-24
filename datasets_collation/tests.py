from django.test import TestCase
from .views import read_csv_as_df, filter_by_countries, left_merge_dataframe, rename_fields, generate_file_name, get_save_path
from pandas import DataFrame
import os

# Create your tests here.
class DatasetCollationTests(TestCase):
    def init_test():
        return "Data Collation App Test"
    
    def test_filter_by_countries(self):
        data = {'id': [1, 2, 3], 'first_name':['Anntoine', 'Brook', 'Casey'], 'country':['France', 'United Kingdom', 'Netherlands']}
        df = DataFrame(data)

        selected_countries = ['Netherlands', 'United Kingdom']
        filtered_df = filter_by_countries(df, selected_countries)

        self.assertNotIn('Anntoine', filtered_df['first_name'])
        self.assertEqual(len(filtered_df), 2)
    
    def test_read_csv_as_df(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'sample_data.csv')
        df = read_csv_as_df(csv_file_path)
        self.assertEqual(len(df), 3)

    def test_left_merge_df(self):
        data_1 = {'id': [1, 2, 3], 'first_name':['Anntoine', 'Brook', 'Casey'], 'country':['France', 'United Kingdom', 'Netherlands']}
        data_2 = {'id': [1, 2, 3], 'last_name':['Louis', 'Holten', 'van der Poel']}
        df_1 = DataFrame(data_1)
        df_2 = DataFrame(data_2)

        merged_df = left_merge_dataframe(df_1, df_2)

        self.assertEqual(list(merged_df.columns), ['id', 'first_name', 'country', 'last_name'])

    def test_rename_fields(self):
        data = {'id': [1, 2, 3], 'cc_t':['Visa', 'American Express', 'Mastercard'], 'btc_a':['123', '456', '789'], 'country':['France', 'United Kingdom', 'Netherlands']}
        df = DataFrame(data)

        renamed_df = rename_fields(df)

        self.assertEqual(list(renamed_df.columns), ['client_identifier', 'credit_card_type', 'bitcoin_address', 'country'])
 



