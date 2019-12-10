from rest_framework import status, response, views
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.management import call_command

from foundation.models import LLIStudentData
from api.serializers import LLIStudentDataSerializer

# api/students?immigration_status_valid_date=2019-12-01


class ImmiStatusValidCheckAPI(views.APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]


    def get(self, request):
        students = LLIStudentData.objects.all()
        immigration_status_valid_date = request.query_params.get('immigration_status_valid_date', None)
        if immigration_status_valid_date is not None:
            students = students.filter(immigration_status_valid_date__gte = immigration_status_valid_date)
        serializer = LLIStudentDataSerializer(students, many=True)



        return response.Response( # Renders to content type as requested by the client.
                status=status.HTTP_200_OK,
                data = serializer.data,
            )



class PaymentValidCheckAPI(views.APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]


    def get(self, request):
        students = LLIStudentData.objects.all()
        payment_valid_date = request.query_params.get('payment_valid_date', None)
        if payment_valid_date is not None:
            students = students.filter(payment_valid_date__gte = payment_valid_date)
        serializer = LLIStudentDataSerializer(students, many=True)

        call_command('email_when_payment_due')

        return response.Response( # Renders to content type as requested by the client.
                status=status.HTTP_200_OK,
                data = serializer.data,
            )


class InsuranceValidCheckAPI(views.APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]


    def get(self, request):
        students = LLIStudentData.objects.all()
        insurance_valid_date = request.query_params.get('insurance_valid_date', None)
        if insurance_valid_date is not None:
            students = students.filter(insurance_valid_date__gte = insurance_valid_date)
        serializer = LLIStudentDataSerializer(students, many=True)

        call_command('email_when_insurance_due')

        return response.Response( # Renders to content type as requested by the client.
                status=status.HTTP_200_OK,
                data = serializer.data,
            )
