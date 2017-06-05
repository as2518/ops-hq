from django.db import models
from datetime import datetime

class Operation(models.Model):

    #登録日時
    regist_date = models.DateTimeField(
        verbose_name = 'Created Date',
        default = datetime.now,
     )

    #作業予定日時
    operation_date = models.DateTimeField(
        verbose_name = 'Scheduled Date',
        default = datetime.now,
     )

    #承認要求番号
    approval_num = models.CharField(
        verbose_name = 'approval number',
        max_length = 20,
        unique = True,
    )

    #作業概要
    title = models.CharField(
        verbose_name = 'operation title',
        max_length = 255,
        null = False,
        blank = True,
    )

    #作業者
    operator = models.CharField(
        verbose_name = 'operator',
        max_length = 255,
        null = True,
        blank = True,
    )

    #ymldata
    yml_data = models.TextField(
        verbose_name = 'ymldata',
        null = False,
        blank = False,
    )

    #作業目的
    ops_purpus = models.TextField(
        verbose_name = 'ops_purpus',
        null = True,
        blank = True,
    )

    #operation_status
    ops_status = models.BooleanField(
        verbose_name = 'operation status',
        default = False,
    )

    #approval_status
    approval_status = models.BooleanField(
        verbose_name = 'Approval status',
        default = False,
    )

    #rollback_status
    rollback_status = models.BooleanField(
        verbose_name = 'rollback status',
        default = False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Operation'
        verbose_name_plural = 'Operations'
