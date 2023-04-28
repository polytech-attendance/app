from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from attendance.models import Subject, Teacher

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_teacher_subjects(request, teacher_id):
    if Teacher.objects.filter(teacher_id=request.data.get('teacher_id')).exists():
        return Response({'error': f'Such teacher with teacher_id {request.data.get("teacher_id")}' + ' doesnt exists'},
                        status=400)
    subjects = Subject.objects.filter(teacher_id=teacher_id)
    data = [{"group_id": subject.group_id, "subject_id": subject.subject_id} for subject in subjects]
    return Response(data, status=200)
