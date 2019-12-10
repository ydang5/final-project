from rest_framework import serializers
from foundation.models import LLIStudentData

class LLIStudentDataSerializer(serializers.Serializer):

    level = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    student_id = serializers.IntegerField()
    start_date = serializers.DateField()
    contract_end_date = serializers.DateField()
    pathway = serializers.CharField()
    photo = serializers.CharField()
    date_of_birth = serializers.DateField()
    nationality = serializers.CharField()
    email_address = serializers.EmailField()
    immigration_status = serializers.CharField()
    immigration_status_valid_date = serializers.DateField()
    insurance_valid_date = serializers.DateField()
    payment_through = serializers.CharField()
    payment_valid_date = serializers.DateField()
    if_have_student_file = serializers.CharField()
