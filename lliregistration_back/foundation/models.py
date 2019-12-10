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
