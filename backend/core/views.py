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
from django.db.models import Count

import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_type_distribution(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)

        equipment_list = dataset.equipment.all()
        
        distribution = {}
        for equip in equipment_list:
            equip_type = equip.equipment_type
            if equip_type not in distribution:
                distribution[equip_type] = {
                    'equipment_type': equip_type,
                    'count': 0,
                    'equipment_names': []
                }
            distribution[equip_type]['count'] += 1
            distribution[equip_type]['equipment_names'].append(equip.name)
        
        result = sorted(distribution.values(), key=lambda x: x['count'], reverse=True)
        return Response({
            'dataset_id': dataset.id,
            'distribution': result
        }, status=status.HTTP_200_OK)
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(1*inch, height - 1*inch, "Equipment Usage Report")

        # Dataset Info
        p.setFont("Helvetica", 12)
        y = height - 1.5*inch
        p.drawString(1*inch, y, f"Filename: {dataset.filename}")
        y -= 0.3*inch
        p.drawString(1*inch, y, f"Uploaded: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
        y -= 0.3*inch
        p.drawString(1*inch, y, f"Total Equipment: {dataset.total_count}")
        
        # Statistics
        y -= 0.5*inch
        p.setFont("Helvetica-Bold", 14)
        p.drawString(1*inch, y, "Statistics:")
        p.setFont("Helvetica", 12)
        y -= 0.3*inch
        p.drawString(1*inch, y, f"Average Flowrate: {dataset.avg_flowrate:.2f}")
        y -= 0.3*inch
        p.drawString(1*inch, y, f"Average Pressure: {dataset.avg_pressure:.2f}")
        y -= 0.3*inch
        p.drawString(1*inch, y, f"Average Temperature: {dataset.avg_temperature:.2f}")
        
        # Type distribution
        y -= 0.5*inch
        p.setFont("Helvetica-Bold", 14)
        p.drawString(1*inch, y, "Equipment Type Distribution:")
        
        distribution = dataset.equipment.values('equipment_type').annotate(
            count=Count('equipment_type')
        )
        
        p.setFont("Helvetica", 12)
        for item in distribution:
            y -= 0.3*inch
            p.drawString(1.2*inch, y, f"{item['equipment_type']}: {item['count']}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        return response
    except Dataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)