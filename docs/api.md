## Final Project Documentary

### API Endpoints/views.py code/Serializer Code/Command Code





1.
Description: This will return the version of the web application \
``urls:api/version``\
Method: GET


2.Description: This will login user by using token method.\
``urls:api/login`` \
Method: POST

3.Description: This will logout users. \
``urls:api/logout`` \
Method: POST


4.Description: This will upload csv file for student data. \
``urls:api/student-file-uploads`` \
Method: POST \

Base code sample for uploading sample csv
```bash
openssl base64 -in sample.csv > sample.csv.base64
http POST :8000/api/student-file-uploads attached_file_name=sample.csv attached_file=@sample.csv.base64 title="2018 Master sheet test" description="This is a test of uploading file."
```
The views.py file has the following code:
```python
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
```
Command code in `process_student_data.py` file

```python
from django.core.management.base import BaseCommand, CommandError
from foundation.models import LLIStudentMasterSheetUpload, LLIStudentData
import csv
from io import StringIO


class Command(BaseCommand):
    help = 'The command will process the student master sheet data.'

    def add_arguments(self, parser):
        parser.add_argument('student_file_ids', nargs='+', type=int)

    def parse_csv_file(self, csv_upload):
        file = csv_upload.read().decode('ISO-8859-1')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        for row_arry in csv_data:
            level = row_arry[0]
            first_name = row_arry[1]
            last_name = row_arry[2]
            student_id = row_arry[3]
            start_date = row_arry[4]
            contract_end_date = row_arry[5]
            pathway = row_arry[6]
            photo = row_arry[7]
            date_of_birth = row_arry[8]
            nationality = row_arry[9]
            email_address = row_arry[10]
            immigration_status = row_arry[11]
            immigration_status_valid_date = row_arry[12]
            insurance_valid_date = row_arry[13]
            payment_through = row_arry[14]
            payment_valid_date = row_arry[15]
            if_have_student_file = row_arry[16]

            if level != "Level":
                LLIStudentData.objects.update_or_create(
                    student_id = student_id,
                    defaults={
                    'level' : level,
                    'first_name' : first_name,
                    'last_name' : last_name,
                    'start_date' : start_date,
                    'student_id' : student_id,
                    'contract_end_date' : contract_end_date,
                    'pathway' : pathway,
                    'photo' : photo,
                    'date_of_birth' : date_of_birth,
                    'nationality' : nationality,
                    'email_address' : email_address,
                    'immigration_status' : immigration_status,
                    'immigration_status_valid_date' : immigration_status_valid_date,
                    'insurance_valid_date' : insurance_valid_date,
                    'payment_through' : payment_through,
                    'payment_valid_date' : payment_valid_date,
                    'if_have_student_file' : if_have_student_file,
                    }                    
                )

    def handle(self, *args, **options):
        for id in options['student_file_ids']:
            student_file = LLIStudentMasterSheetUpload.objects.get(id=id)
            self.parse_csv_file(student_file.data_file)
            self.stdout.write(self.style.SUCCESS('Successfully processed student file at ID "%s"' % id))
```

Code in Serializer file:

```python
from django.db import transaction
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from foundation.models import LLIStudentMasterSheetUpload

from django.core.files.base import ContentFile
import base64
import six
import uuid
def get_content_file_from_base64_string(data, filename):
    """
    Function will convert the string and filename parameter and return a
    `ContentFile` object.

    Special thanks:
    (1) https://github.com/tomchristie/django-rest-framework/pull/1268
    (2) https://stackoverflow.com/a/39587386
    """
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            print("Failed conversion.")
            return None

        # Convert it to the content file.
        data = ContentFile(decoded_file, name=filename)
    return data

class LLIStudentMasterSheetUploadSerializer(serializers.Serializer):
    attached_file_name = serializers.CharField(write_only=True, allow_null=False,)
    attached_file = serializers.CharField(write_only=True, allow_null=False,)
    title = serializers.CharField(required=False, allow_null=True,)
    description = serializers.CharField(required=False, allow_null=True,)

    @transaction.atomic
    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """

        # Extract our upload file data
        content = validated_data.get('attached_file')
        filename = validated_data.get('attached_file_name')

        # Convert the base64 data into a `ContentFile` object.
        content_file = get_content_file_from_base64_string(content, filename)

        # Create our file.
        private_file = LLIStudentMasterSheetUpload.objects.create(
            title = validated_data.get('title'),
            description = validated_data.get('description'),
            data_file = content_file, # When you attack a `ContentFile`, Django handles all file uploading.
        )

        # Return our validated data.
        return private_file
```

5.Description: This will send a daily notice email start at 30 days before the student immigration status expire \
``urls:api/immi-check`` \
Method: GET \

The views.py file has the following code:
```python
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
```

Command code in `email_when_immi_due.py` file

```python
from django.core.management.base import BaseCommand, CommandError
from foundation.models import LLIStudentData
from django.utils import timezone
from django.core.mail import send_mail


class Command(BaseCommand):
    help = '-'

    def process_students(self, students):
        now = timezone.now().date()
        student_expired_immi_status_arr = []
        for student in students:
            print(student.immigration_status_valid_date)
            print(now)
            target_date = student.immigration_status_valid_date
            delta = target_date - now
            print(delta.days+1)
            print()
            if delta.days +1 <= 30:
                if student.was_immigration_status_valid_date_dealt == False:
                    print('send email to student with id:', student.student_id)

                    student_expired_immi_status_arr.append(student)
        self.email_staff(student_expired_immi_status_arr)

    def email_staff(self, students):
        # print(students)
        email_message = ""
        for student in students:
            student_first_name = student.first_name
            student_last_name = student.last_name
            student_id = str(student.student_id)
            student_immi_status_expire_date = str(student.immigration_status_valid_date)

            email_message +="Student :"+ student_first_name+" "+student_last_name+" with student id: "+student_id+" immigration status is going to be expired on "+student_immi_status_expire_date +"\n"

        send_mail(
            'Subject here',
            email_message,
            'from@example.com',
            ['yi@llinstitute.com'],
            fail_silently=False,
        )


    def handle(self, *args, **options):
        # sutudents = LLIStudentData.objects.all()
        # self.process_students(sutudents)
        self.stdout.write(self.style.SUCCESS('Successfully process immigration due dates.'))
```

Code in Serializer file:
```python
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
```
6.Description: This will send a daily notice email start at 7 days before the student payment expires \
``urls:api/immi-check`` \
Method: GET \

The views.py file has the following code:
```python
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
```
Command code in `email_when_payment_due.py` file:

```python
from django.core.management.base import BaseCommand, CommandError
from foundation.models import LLIStudentData
from django.utils import timezone
from django.core.mail import send_mail


class Command(BaseCommand):
    help = '-'

    def process_students(self, students):
        now = timezone.now().date()
        student_expired_payment_arr = []
        for student in students:
            print(student.payment_valid_date)
            print(now)
            target_date = student.payment_valid_date
            delta = target_date - now
            print(delta.days+1)
            print()
            if delta.days +1 <= 7:
                if student.was_payment_valid_date_dealt == False:
                    print('send email to student with id:', student.student_id)

                    student_expired_payment_arr.append(student)
        self.email_staff(student_expired_payment_arr)

    def email_staff(self, students):
        email_message = ""
        for student in students:
            student_first_name = student.first_name
            student_last_name = student.last_name
            student_id = str(student.student_id)
            student_payment_expire_date = str(student.payment_valid_date)

            email_message +="Student :"+ student_first_name+" "+student_last_name+" with student id: "+student_id+" payment is going to be expired on "+student_payment_expire_date +"\n"
        send_mail(
            'Subject here',
            email_message,
            'from@example.com',
            ['yi@llinstitute.com'],
            fail_silently=False,
        )


    def handle(self, *args, **options):
        sutudents = LLIStudentData.objects.all()
        self.process_students(sutudents)
        self.stdout.write(self.style.SUCCESS('Successfully process payment due dates.'))
```
Code in Serializer file: `Same Serializer as 5`

7.Description: This will send a daily notice email start at 7 days before the student insurance expires \
``urls:api/immi-check`` \
Method: GET \

The views.py file has the following code:
```python
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
```

Command code in `email_when_insurance_due.py` file:

```python
from django.core.management.base import BaseCommand, CommandError
from foundation.models import LLIStudentData
from django.utils import timezone
from django.core.mail import send_mail


class Command(BaseCommand):
    help = '-'

    def process_students(self, students):
        now = timezone.now().date()
        student_expired_insurance_arr = []
        for student in students:
            print(student.insurance_valid_date)
            print(now)
            target_date = student.insurance_valid_date
            delta = target_date - now
            print(delta.days+1)
            print()
            if delta.days +1 <= 7:
                if student.was_insurance_valid_date_dealt == False:
                    print('send email to student with id:', student.student_id)

                    student_expired_insurance_arr.append(student)
        self.email_staff(student_expired_insurance_arr)

    def email_staff(self, students):
        email_message = ""
        for student in students:
            student_first_name = student.first_name
            student_last_name = student.last_name
            student_id = str(student.student_id)
            student_insurance_expire_date = str(student.insurance_valid_date)

            email_message +="Student :"+ student_first_name+" "+student_last_name+" with student id: "+student_id+" insurance is going to be expired on "+student_insurance_expire_date +"\n"

        send_mail(
            'Subject here',
            email_message,
            'from@example.com',
            ['yi@llinstitute.com'],
            fail_silently=False,
        )


    def handle(self, *args, **options):
        sutudents = LLIStudentData.objects.all()
        self.process_students(sutudents)
        self.stdout.write(self.style.SUCCESS('Successfully process payment due dates.'))
```
Code in Serializer file: `Same Serializer as 5`

### Models:

```python
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command


class LLIStudentMasterSheetUploadManager(models.Manager):
    def delete_all(self):
        items = LLIStudentMasterSheetUpload.objects.all()
        for item in items.all():
            item.delete()

class LLIStudentMasterSheetUpload(models.Model):
    """
    Upload image class which is publically accessible to anonymous users
    and authenticated users.
    """
    class Meta:
        app_label = 'foundation'
        db_table = 'lli_student_master_sheet_file_uploads'
        verbose_name = _('LLI Student Master Sheet File Upload')
        verbose_name_plural = _('LLI Student Master Sheet Uploads')
        default_permissions = ()
        permissions = ()

    objects = LLIStudentMasterSheetUploadManager()

    #
    #  FIELDS
    #

    data_file = models.FileField(
        upload_to = 'uploads/%Y/%m/',
        help_text=_('The upload binary file.'),
    )
    title = models.CharField(
        _("Title"),
        max_length=63,
        help_text=_('The tile of this upload.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_('The description content of this upload.'),
        blank=True,
        null=True
    )

    #
    #  FUNCTIONS
    #

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super(LLIStudentMasterSheetUpload, self).save(*args, **kwargs)
        call_command('process_student_data', self.id)


class LLIStudentData(models.Model):

    class Meta:
        app_label = 'foundation'
        db_table = 'lli_student_data'
        verbose_name = _('LLI Student Master Sheet datum')
        verbose_name_plural = _('LLI Student Master Sheet data')
        default_permissions = ()
        permissions = ()

    level = models.CharField(
        max_length = 50,
        help_text=_('student current level.'),
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length = 255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length = 255,
        blank=True,
        null=True
    )
    student_id = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    start_date = models.DateField(
        blank=True,
        null=True
    )
    contract_end_date = models.DateField(
        blank=True,
        null=True
    )
    pathway = models.CharField(
        max_length = 50,
        blank=True,
        help_text=_('Is this a pathway student, please answer yes or no.'),
        null=True
    )
    photo = models.CharField(
        max_length = 50,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    nationality = models.CharField(
        max_length = 255,
        blank=True,
        null=True
    )
    email_address = models.EmailField(
        blank=True,
        null=True
    )
    immigration_status = models.CharField(
        max_length = 50,
        help_text=_('Study permit, work permit, visitor, PR, or Canadian citizen'),
        blank=True,
        null=True
    )
    immigration_status_valid_date = models.DateField(
        blank=True,
        null=True
    )
    was_immigration_status_valid_date_dealt = models.BooleanField(
        default = False,
        blank = True
    )
    insurance_valid_date = models.DateField(
        blank=True,
        null=True
    )
    was_insurance_valid_date_dealt = models.BooleanField(
        default = False,
        blank = True
    )
    payment_through = models.CharField(
        max_length = 255,
        help_text=_('Self or agent'),
        blank=True,
        null=True
    )
    payment_valid_date = models.DateField(
        blank=True,
        null=True
    )
    was_payment_valid_date_dealt = models.BooleanField(
        default = False,
        blank = True
    )
    if_have_student_file =  models.CharField(
        max_length = 50,
        blank=True,
        null=True
    )
    def __str__(self):
        return str(self.first_name)+ " " + str(self.last_name) +'is studying in '+str(self.level)+'is under '+ str(self.immigration_status)+'is going to expired on '+str(self.immigration_status_valid_date)+'payment is valid to '+str(self.payment_valid_date)+'insurance is valid to '+str(self.insurance_valid_date)
```
