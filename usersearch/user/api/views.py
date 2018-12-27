from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.views.generic.base import TemplateView


import pandas as pd
import numpy as np


class UserPageTemplateView(TemplateView):
    template_name = "load_user.html"


class InstaSearchUserAPIView(APIView):
    """

    search the users in the dataset based on the query params
    """

    def get(self, request):

        query_param_value = request.query_params.get('q', None)

        if query_param_value is not None and (len(query_param_value) > 3):

            columns = ['givenName', 'middleName', 'surname']

            file_loc = settings.BASE_DIR+'/data.csv'

            # get the dataframe using pandas
            try:
                df = pd.read_csv(file_loc, names=columns)
            except Exception as err:
                print(err)
                df = None
            
            if df is not None:
                # get the dataframe which starts with query_param_value
                matched_df = df[df['givenName'].str.startswith(query_param_value, na=False)]

                # make length of givenName as a index
                matched_df.index = matched_df['givenName'].str.len()

                #sort in ascending of index and drop index
                matched_df = matched_df.sort_index(ascending=True).reset_index(drop=True)

                #replace NaN values to null
                matched_df = matched_df.replace(np.nan, 'null', regex=True)

                # conver to json
                matched_df = matched_df.to_dict(orient='records')

                return Response(matched_df, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            


