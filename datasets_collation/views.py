from django.shortcuts import render
from django.http import HttpResponse
from .forms import MergeDatasetForm
from datetime import datetime

import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):

    """
    Main view function for collating datasets.

    Handles the collation process when a POST request is received,
    and renders the form for GET requests.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered template or a result popup.
    """

    if request.method == 'POST':
        logger.info('POST request received to Collate Dataset')

        form = MergeDatasetForm(request.POST, request.FILES)
        logger.info('Posted form information stored in form object')

        if form.is_valid():
            logger.info('Required fields is valid. Reading fields value')

            dataset_1 = request.FILES['dataset_1']
            logger.info('Dataset 1 stored in dataset_1')

            dataset_2 = request.FILES['dataset_2']
            logger.info('Dataset 2 stored in dataset_1')

            selected_countries = form.cleaned_data['countries']
            logger.info(f'{len(selected_countries)} country/ies selected: {selected_countries}')

            if dataset_1.name.endswith('csv') & dataset_2.name.endswith('csv'):
                logger.info('Provided datasets are in CSV format. Reading csv dataset as dataframe')

                df_1 = read_csv_as_df(dataset_1)
                df_1 = filter_by_countries(df_1, selected_countries)
                logger.info(f'Clients from {selected_countries} included')
                df_1 = df_1[['id', 'email']]
                logger.info('fields containing personal information are removed')

                df_2 = read_csv_as_df(dataset_2)
                logger.info('Dataset 2 stored as dataframe in df_2')
                df_2 = df_2[['id', 'btc_a', 'cc_t']]
                logger.info('field containing private financial information is removed')

                merge_df = left_merge_dataframe(df_1, df_2)

                renamed_df = rename_fields(merge_df)

                save_path = get_save_path()
                logger.info('save path retrieved')

                renamed_df.to_csv(save_path)
                logger.info(f'output stored in {save_path}')

                return result_popup(f'Data succesfully stored in {save_path}')
            else:
                logger.error('providing files other than csv')
                return result_popup('Datasets file must be in CSV')
    else:
        logger.info('Data Collation App invoked')
        form = MergeDatasetForm()
        logger.info('Returning MergeDatasetForm to main view')
    return render(request, 'read_csv_datasets.html', {'form': form})

def filter_by_countries(df, selected_countries):
    """
        This function filters the provided Pandas DataFrame based on the list of selected countries.
        It keeps only the rows where the 'country' column matches one of the selected countries.

        Args:
            df (pandas.DataFrame): The DataFrame to be filtered.
            selected_countries (list): A list of country names to filter by.

        Returns:
            pandas.DataFrame: A filtered DataFrame containing only the rows with selected countries.
    """
    logger.info(f'removing data outside the specified countries: {selected_countries}')
    return df[df['country'].isin(selected_countries)]

def get_save_path():
    """
    Get the file path for saving the merged dataset.
    The path is based on the root directory of the project
    Later, the file will be stored in a folder named 'client_data'.

    Returns:
        str: The complete file path for saving the merged dataset.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f'Root directory path: {root_dir}')
    client_data_folder = os.path.join(root_dir, 'client_data')
    logger.info(f'fClient Data folder path: {client_data_folder}')
    file_path = os.path.join(client_data_folder, generate_file_name())
    logger.info(f'File name retrieved. File path complete: {file_path}')
    return file_path

def generate_file_name():
    """
    Get the file name for saving the merged dataset.
    The file name composed of: client_data_{date_time}.csv

    Returns:
        str: The complete file name for saving the merged dataset.
    """
    current_datetime = datetime.now()
    logger.info(f'Retrived current date time: {current_datetime}')
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    logger.info('Date time formatted')
    file_name = 'client_data_'+formatted_datetime+'.csv'
    logger.info(f'Generated file name: {file_name}')
    return file_name

def read_csv_as_df(file):
    """
    Read a CSV file as a pandas DataFrame.

    Args:
        file (File): The CSV file to read.

    Returns:
        DataFrame: The pandas DataFrame containing the CSV data.
    """
    logger.info(f'read {file} as dataframe')
    return pd.read_csv(file)

def left_merge_dataframe(df_1, df_2):
    """
    Left-merge two DataFrames on the 'id' column.

    Args:
        df_1 (DataFrame): The first DataFrame. This is the dataframe containing the personal information.
        df_2 (DataFrame): The second DataFrame. This is the dataframe containing the financial information.

    Returns:
        DataFrame: The merged DataFrame.
    """
    logger.info('Merge df_1 and df_2 on ID using left-merge')
    return df_1.merge(df_2, on='id', how='left')

def rename_fields(df):
    """
    Renaming fields into more descriptive and clearer name.
    There will be three field renamed:
    'id' -> 'client_identifier',
    'btc_a' -> 'bitcoin_address',
    'cc_t' -> 'credit_card_type'.

    Args:
        df (Dataframe): The dataframe to be edited.

    Returns:
        df: Renamed dataframe fields.
    """
    logger.info('Renaming id, btc_a and cc_t fields')
    return df.rename(columns={
                        'id' : 'client_identifier',
                        'btc_a' : 'bitcoin_address',
                        'cc_t' : 'credit_card_type'
                    })

def result_popup(msg):
    """
    Generate a popup containing message defined.

    Args:
        msg (str): The message to display in the popup.

    Returns:
        HttpResponse: A response containing the popup.
    """
    return HttpResponse(
                            f'<script type="text/javascript">'
                            f'alert("{msg}");'
                            f'window.location.href = window.location.href;'
                            f'</script>'
                        )