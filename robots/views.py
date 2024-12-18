import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Robot

@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            serial = data.get('serial')
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')
            
            if not all([serial, model, version, created]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if not Robot.objects.filter(model=model, version=version).exists():
                return JsonResponse({'error': f'Model {model} with version {version} does not exist'}, status=400)
            
            created_date = parse_datetime(created)
            if not created_date:
                return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD HH:MM:SS'}, status=400)
            
            robot = Robot.objects.create(
                serial=serial,
                model=model,
                version=version,
                created=created_date
            )

            return JsonResponse({'message': 'Robot created successfully', 'robot_id': robot.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)