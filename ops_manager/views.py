from django.shortcuts import render
from django.http import HttpResponse
from ops_manager.models import Operation
from pprint import pprint
from jinja2 import Environment,FileSystemLoader
from ops_manager.forms import OperationForm
from ops_manager.scripts.post_to_chatwork import cw_notice
from datetime import datetime

YML_TEMPLATE_FILEPATH = './ops_manager/scripts/yml_templates/'
def bundle_context(postdata):
    context = {
        'title' : postdata['title'],
        'approval_num' : postdata['approval_num'],
        'operation_date' : postdata['operation_date'],
        'operator' : postdata['operator'],
        'peer_type' : postdata['peer_type'],
        'router_name' : postdata['router_name'],
        'neighbor_asnum' : postdata['neighbor_asnum'],
        'neighbor_description' : postdata['neighbor_description'],
        'neighbor_address' : postdata['neighbor_address'],
        'policy_name_in' : postdata['policy_name_in'],
        'policy_name_out' : postdata['policy_name_out'], 
        'ops_purpus' : postdata['ops_purpus'],
    }
    if 'interface_name' in postdata:
        context.update({
            'interface_name' : postdata['interface_name'],
            'interface_description' : postdata['interface_description'],
            'interface_subnet' : postdata['interface_subnet'],
        })
    return context

def ops_list(request):
    if request.method == 'POST':
        env = Environment(loader = FileSystemLoader(YML_TEMPLATE_FILEPATH, encoding = 'utf-8'))
        template = env.get_template('ops_template.j2')
        yml_data = template.render(bundle_context(request.POST))
        ops_data = {
            'title':request.POST['title'],
            'operation_date': datetime.strptime(request.POST['operation_date'], '%Y-%m-%dT%H:%M'),
            'approval_num':request.POST['approval_num'],
            'ops_purpus':request.POST['ops_purpus'],
            'ops_status':False,
            'approval_status':False,
            'rollback_status':False,
            'yml_data':yml_data,
            'operator':request.POST['operator'],
        }
        ops = Operation()
        form = OperationForm(ops_data, instance=ops)
        ops = form.save(commit=False)
        ops.save()
        ops_id = Operation.objects.get(approval_num = request.POST['approval_num']).pk
        ch_notice(request.POST['title'],ops_id,1)

    context = {'ops_list':Operation.objects.all().order_by('-id')}
    return render(request, 'ops_manager/ops_list.html', context)


def ops_add(request):
    if request.method == 'GET':
        return render(request, 'ops_manager/ops_add.html')
    else:
        context = {
            'title' : request.POST['title'],
            'approval_num' : request.POST['approval_num'],
            'operation_date' : request.POST['operation_date'],
            'operator' : request.POST['operator'],
            'peer_type' : request.POST['peer_type'],
            'router_name' : request.POST['router_name'],
            'ops_purpus' : request.POST['ops_purpus'],
        }
        return render(request,'ops_manager/ops_add_param.html',context)

def ops_add_confirm(request):
    context = bundle_context(request.POST)
    return render(request, 'ops_manager/ops_add_confirm.html',context)

def ops_detail(request,ops_id=None):
    ops_obj = Operation.objects.get(pk = ops_id)
    # tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%dT%H:%M')
    # tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
    
    context = {
            'ops_id':ops_id,
            'title' : ops_obj.title,
            'approval_num' : ops_obj.approval_num,
            'operation_date' : ops_obj.operation_date,
            'ops_status' : ops_obj.ops_status,
            'rollback_status' : ops_obj.rollback_status,
            'approval_status' : ops_obj.approval_status,
            'operator' : ops_obj.operator,
            'ops_purpus' : ops_obj.ops_purpus,
            'yml_data' : ops_obj.yml_data,
    }
    return render(request, 'ops_manager/ops_detail.html',context)

def change_status(request,ops_id=None,cond=None,status=None):
    
    ops = Operation.objects.get( pk = ops_id )
    if cond in 'approval':
        if int(status):
            ops.approval_status = True
            
            cw_notice(ops.title,ops_id,2)
        else:
            ops.approval_status = False
    elif cond in 'ops':
        if int(status):
            ops.ops_status = True
        else:
            ops.ops_status = False      
    elif cond in 'rollback':
        if int(status):
            ops.rollback_status = True
        else:
            ops.rollback_status = False

    ops.save()
    context = {'ops_list':Operation.objects.all().order_by('-id')}
    return render(request, 'ops_manager/ops_list.html', context)

def ops_edit(request):
    return

def ops_del(request):
    return