from django.forms import ModelForm
from ops_manager.models import Operation


class OperationForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Operation
        fields = ('operation_date','operator','title' ,'approval_num','yml_data','ops_purpus','ops_status','rollback_status','approval_status' )