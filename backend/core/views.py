from .serializers import DatasetSerializer, EquipmentSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer
from .models import Dataset, Equipment

import pandas as pd

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok'
    })

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    # return 201 if success
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    # return 401 if error
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    datasets = Dataset.objects.filter(user=user)

    return Response({
        'user': UserSerializer(user).data,
        'total_datasets': datasets.count(),
        'datasets': [
            {
                'id': dataset.id,
                'filename': dataset.filename,
                'uploaded_at': dataset.uploaded_at,
                'total_count': dataset.total_count,
            }
            for dataset in datasets
        ]
        # This has a lot more data than needed
        # 'datasets': DatasetSerializer(datasets, many=True).data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_dataset(request):
    if 'file' not in request.FILES:
        return Response({
            'error': 'No file provided'
        }, status=status.HTTP_400_BAD_REQUEST)    

    csv_file = request.FILES['file']
    
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        return Response({
            'error': f'Invalid CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST
        )

    # Calculate statistics for visualization

    total_count = len(df)
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()

    dataset = Dataset.objects.create(
        user=request.user,
        filename=csv_file.name,
        total_count=total_count,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature
    )

    for _, row in df.iterrows():
        Equipment.objects.create(
            dataset=dataset,
            name=row.get('Equipment Name', 'Unknown/NA'),
            equipment_type=row.get('Type', 'Unknown/NA'),
            flowrate=row.get('Flowrate', 0.0),
            pressure=row.get('Pressure', 0.0),
            temperature=row.get('Temperature', 0.0)
        )
    
    # filter dataset by different users
    user_datasets = Dataset.objects.filter(user=request.user)
    if user_datasets.count() > 5:
        old_datasets = user_datasets[5:]
        for old in old_datasets:
            old.delete()
    
    return Response({
        'message': "Dataset Uploaded Successfully",
        'dataset': DatasetSerializer(dataset).data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    datasets = Dataset.objects.filter(user=request.user)[:5]
    if datasets:
        return Response(
            DatasetSerializer(datasets, many=True).data
        , status=status.HTTP_200_OK)
    return Response({
        'message': 'No datasets found'
    }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_details(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        return Response(
            DatasetSerializer(dataset).data)
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset.delete()
        return Response({
            'message': 'Dataset deleted successfully'
        }, status=status.HTTP_200_OK)
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)
    

    