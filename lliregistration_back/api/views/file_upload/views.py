from api.serializers import LLIStudentMasterSheetUploadSerializer
from rest_framework import status, response, views
from django.core.management import call_command

class LLIStudentMasterSheetUploadAPIView(views.APIView):
    def post(self, request):
        serializer = LLIStudentMasterSheetUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        object = serializer.save()

        call_command('process_student_data',object.id)

        return response.Response( # Renders to content type as requested by the client.
            status=status.HTTP_200_OK,
            data={
                'detail': serializer.data,
            }
        )
