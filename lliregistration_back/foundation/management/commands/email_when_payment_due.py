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
