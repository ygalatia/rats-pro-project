from django.shortcuts import render
from django.http import HttpResponse
from .forms import MergeDatasetForm
from datetime import datetime

import pandas as pd
import os


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = MergeDatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset_1 = request.FILES['dataset_1']
            dataset_2 = request.FILES['dataset_2']
            selected_countries = form.cleaned_data['countries']

            if dataset_1.name.endswith('csv') & dataset_2.name.endswith('csv'):
                df_1 = pd.read_csv(dataset_1)
                df_1 = filter_by_countries(df_1, selected_countries)
                df_1 = df_1[['id', 'email']]

                df_2 = pd.read_csv(dataset_2)
                df_2 = df_2[['id', 'btc_a', 'cc_t']]

                merge_df = df_1.merge(df_2, on='id', how='left')
                renamed_df = merge_df.rename(columns={
                    'id' : 'client_identifier',
                    'btc_a' : 'bitcoin_address',
                    'cc_t' : 'credit_card_type'
                })

                save_path = get_save_path()

                renamed_df.to_csv(save_path)

                response = HttpResponse(
                    '<script type="text/javascript">'
                    'alert("Data successfully stored!");'
                    'window.location.href = window.location.href;'
                    '</script>'
                )

                return response
            else:
                return HttpResponse('Files must be csv')
    else:
        form = MergeDatasetForm()
    return render(request, 'read_csv_datasets.html', {'form': form})

def filter_by_countries(df, selected_countries):
    return df[df['country'].isin(selected_countries)]

def get_save_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client_data_folder = os.path.join(root_dir, 'client_data')
    file_path = os.path.join(client_data_folder, generate_file_name())
    return file_path

def generate_file_name():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    file_name = 'client_data_'+formatted_datetime+'.csv'
    return file_name