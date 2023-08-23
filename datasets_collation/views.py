from django.shortcuts import render
from django.http import HttpResponse
from .forms import MergeDatasetForm
import pandas as pd

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

                return HttpResponse(renamed_df.to_string, content_type='text/plain')
            else:
                return HttpResponse('Files must be csv')
    else:
        form = MergeDatasetForm()
    return render(request, 'read_csv_datasets.html', {'form': form})

def filter_by_countries(df, selected_countries):
    return df[df['country'].isin(selected_countries)]