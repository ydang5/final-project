from django.core.management import call_command

from django_cron import CronJobBase, Schedule


# class MyCronJob(CronJobBase):
#     RUN_AT_TIMES = ['11:30']
#
#     schedule = Schedule(run_at_times=RUN_AT_TIMES)
#
#     code = 'foundation.my_cron_job'    # a unique code
#
#     def do(self):
#         print("123test")    # do your thing here

class ImmigrationStatusEmailJob(CronJobBase):
    RUN_AT_TIMES = ['11:30']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'foundation.immigration_status_email_job'    # a unique code

    def do(self):
        call_command('email_when_immi_due')


class PaymentEmailJob(CronJobBase):
    RUN_AT_TIMES = ['12:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'foundation.payment_email_job'    # a unique code

    def do(self):
        call_command('email_when_payment_due')


class InsuranceEmailJob(CronJobBase):
    RUN_AT_TIMES = ['11:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'foundation.insurance_email_job'    # a unique code

    def do(self):
        call_command('email_when_insurance_due')
