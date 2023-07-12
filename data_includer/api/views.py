import random
import string

import pandas as pd
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from table.models import *
from .serializers import TableSerializer


class GenerateTokenView(UserPassesTestMixin, APIView):
    """
    Generates api_token for an authorized user
    """

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        user = User.objects.get(id=request.user.pk)

        characters = string.ascii_letters + string.digits

        unique_token = False
        while not unique_token:
            api_token = ''.join(random.choice(characters) for _ in range(32))
            existing_user = User.objects.filter(api_token=api_token).exists()
            if not existing_user:
                unique_token = True

        user.api_token = api_token
        user.save()

        return Response({'api_token': api_token})


class RevokeTokenView(UserPassesTestMixin, APIView):
    """
    Revokes api_token for an authorized user
    """

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        user = User.objects.get(id=request.user.pk)

        user.api_token = None
        user.save()

        return Response({'message': 'API token revoked'})


class FileUploadView(APIView):
    """
    Upload csv file on server related to user's api_token
    """

    parser_classes = (FileUploadParser,)

    def post(self, request, format=None):
        content_type = request.content_type.split(';')[0].strip()
        api_token = request.query_params.get('api_token')

        user = User.objects.filter(api_token=api_token).first()

        if user:
            if content_type == 'text/csv':
                file_serializer = TableSerializer(data={'file': request.data.get('file'), 'user': user.pk})
                if file_serializer.is_valid():
                    file_serializer.save()
                    return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(None, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        else:
            return Response({'status_code': '403'}, status=status.HTTP_403_FORBIDDEN)


class FileListView(APIView):
    """
    List of csv files on server related to user's api_token
    """

    def get(self, request, format=None):
        api_token = request.query_params.get('api_token')
        user = User.objects.filter(api_token=api_token).first()

        if user:
            uploaded_files = Dataset.objects.all() if user.is_superuser else Dataset.objects.filter(user=user)
            serializer = TableSerializer(uploaded_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'status_code': '403'}, status=status.HTTP_403_FORBIDDEN)


class FileReadView(APIView):
    """
    Read csv file using get request and pandas dataframe as a response
    """

    parser_classes = (FileUploadParser, )

    def get(self, request, format=None):
        api_token = request.query_params.get('api_token')
        user = User.objects.filter(api_token=api_token).first()

        file = request.data.get('file')

        if not file:
            return Response({'error': 'No file provided'}, status=400)

        if user:
            try:
                table_data = pd.read_table(file).to_dict()
                return Response(table_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

        else:
            return Response({'status_code': '403'}, status=status.HTTP_403_FORBIDDEN)


class FileDeleteView(APIView):
    """
    Delete csv file on server related to user's api_token
    """

    def delete(self, request, file_id, format=None):
        try:
            api_token = request.query_params.get('api_token')
            user = User.objects.filter(api_token=api_token).first()

            if user:
                uploaded_file = Dataset.objects.get(id=file_id) if user.is_superuser \
                    else Dataset.objects.get(id=file_id, user=user)
                uploaded_file.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'status_code': '403'}, status=status.HTTP_403_FORBIDDEN)

        except Dataset.DoesNotExist:
            return Response({'status_code': '404'}, status=status.HTTP_404_NOT_FOUND)
