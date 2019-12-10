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
