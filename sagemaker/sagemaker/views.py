from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from joblib import load
from django.core.files import File
import os
import numpy as np
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django.template import Library
import sys
import boto3
from django.conf import settings

# 'fuelType', 'km', 'make', 'model', 'price', 'transmissionType', 'year',
#        'cubicCapacity', 'doors', 'hp'


def inicio(request):

    # ----------------------lectura de json para los select ---------------------------

    marcas_id = open(
        os.path.dirname(os.path.realpath(__file__)) + "/json/marcas_id.json",
        "rb",
    )

    
    marca_model_id = open(
        os.path.dirname(os.path.realpath(__file__)) +
        "/json/marca_model_id.json",
        "rb",
    )

    with marcas_id as file:
        data = json.load(file)
        data_json = json.dumps(data)

    with marca_model_id as file2:
        data2 = json.load(file2)
        data_json2 = json.dumps(data2)

    # ----------------------lectura de json para los select ---------------------------

    aws_access_key_ID = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_KEY = settings.AWS_SECRET_ACCESS_KEY
    aws_session_TOKEN = settings.AWS_SESSION_TOKEN
    endpPoint = settings.ENDPOINT
    bucket = settings.BUCKET
    region_NAME = settings.REGION_NAME

    if request.POST:
        # 'fuelType', 'km', 'make', 'model','transmissionType', 'year','cubicCapacity', 'doors', 'hp'
        fuelType = request.POST['fuelType']
        km = request.POST['km']
        make = request.POST['make']
        model = request.POST['model']
        transmissionType = request.POST['transmissionType']
        year = request.POST['year']
        cubicCapacity = request.POST['cubicCapacity']
        doors = request.POST['doors']
        hp = request.POST['hp']

    
        data_usuario = "{fuelType},{km},{make},{model},{transmissionType},{year},{cubicCapacity},{doors},{hp}"

        client = boto3.Session(
            aws_access_key_id=aws_access_key_ID,
            aws_secret_access_key=aws_secret_access_KEY,
            aws_session_token=aws_session_TOKEN,
            region_name=region_NAME).client('sagemaker-runtime')

        response = client.invoke_endpoint(
            EndpointName=endpPoint, ContentType='text/csv', Accept='text/csv', Body=data_usuario)
        response = response['Body'].read().decode('utf-8')

        return render(request, "resultado.html", {"predict": response})

    return render(request, "inicio.html", {"marcas_id": data_json, "marca_model_id": data_json2})
