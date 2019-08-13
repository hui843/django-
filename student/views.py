import os
from django.http import HttpResponse
import xlwt
from django.shortcuts import render,reverse,redirect
from .models import Student,Class
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.conf import settings
from student import models
from math import ceil
from django.db.models import Q

# Create your views here.
def index(request):
    """获取学生列表"""
    #计算分页索引
    page_no = int(request.GET.get('page_no',1)) #从第几页显示
    page_size = int(request.GET.get('page_size',3))#一页显示几条数据
    start_index = (page_no - 1) * page_size #(1-1)*3
    end_index = page_no * page_size
    #todo 多条件过滤
    # if request.POST:
    #     name_like = request.POST.get('name',None)
    #     gender = request.POST.get('gender',None)
    #查询
    rows_amount = Student.objects.all().count()
    # page_amount = rows_amount // page_size + 1
    page_amount = ceil(rows_amount/page_size)
    #  #9条，每页3条 整除时导致总页数多算了1.解决方法一 行数-0.1再除；方法二ceil返回大于等于的整数
    page_amount_list = [i for i in range(page_amount)]
    if page_size > page_amount or page_size < 0:
        error_message = '请求页码超过最大页码'
    lsj = Student.objects.all().order_by('no')[start_index:end_index]
    context = {
        'lsj':lsj,
        'page_amount_list':page_amount_list,
        'page_previous':page_no - 1,
        'page_no':page_no,
        'page_next':page_no +1,
        }
    return (render(request,'student/index.html',context))

def api_index(request):
    """
    :return
    ,
    {
        "code":200,
        "message":"ok",
        "count":"80",
        "student_list":[
            {"id":1,"no":001,"name":"张三","add_time":"2019-10-09"},
            {"id":1,"no":001,"name":"张三","add_time":"2019-10-09"},
        ]
    }
    """

def index2(request):
    student_list = Student.objects.all().order_by('no')
    paginator = Paginator(student_list,3)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request, 'student/index2.html',{'students':students})

def add(request):
    """添加学生信息"""
    max_no = Student.objects.aggregate(Max('no'))
    next_no = max_no['no__max']+1
    context = {
        'next_no':next_no,
    }
    return render(request,'student/add.html',context)
def do_add(request):
    message = ''
    error_message = ''
    """POST 存储用户提交的新学生信息"""
    stuClass = Student
    assert  request.method == 'POST','error:表单http请求方式应为post'
    #取参数
    #django框架自带了表单类，先跟model映射，自动生成表单，自动方法form.isvalid合法性炎症 form.save()保存
    #但这个方法隐藏了原理，前端不容易改css，需要记忆额外来自自定义表单，在具备前端基础的情况下不推荐使用django自带的
    #为了理解原理，前端手写html表单，后端存
    args = request.POST
    file = request.FILES        #文件存到这个字段里， 内存中，open方法打开

    no = args['no']
    files = request.FILES
    user_file = files['avatar']
    chunks = user_file.chunks()
    no = int(args['no'])
    name = args['name']
    age = args['age']
    gender = args['gender']
    phone = args['phone']
    age = int(args['age'])
    gender = int(args['gender'])
    phone = args['phone'] or None
    _file_name = user_file.name
    #todo如果数据库存同名附件"头像.jpg"，并不意味这内容相同。django会在文件名后自动编号以区分，用hash判断两文件是否相同
    _upload_to = Student.avatar.field.upload_to     #取model中的avatar字段的长传路径，查看ImageField源代码和debug查看Student可以发现stuClass=Student
    avatar = _avatar_db_path = os.path.join(_upload_to,_file_name)
    #验证
    #存储
    context = {}
    #判断个参数值是否合法，学号是否存在，等。（在实际工作中，挑重要的写，不重要的交给前端表单验证，单后端验证最安全）
    if no < 0 or no >10000:
        error_message ='输入非法，学号范围为0-9999'
        #return render() 出现错误返回添加页面，但下面也需要写这行的代码重复，明智的做法是判断flag标识，比如error_message是否 为空
    if Student.objects.filter(no=no).exists():
        max_no = Student.objects.aggregate(Max('no'))['max_no']
        error_message = f'学号已存在，目前最大学号为{max_no}，建议学号设置为{max_no+1}'
    if gender not in [i[0] for i in Student.GENDER_CHOICES]:
        error_message = '性别可选值不正确'
    if error_message:
        return render(request,'student/add.html',context={'error_message':error_message})


    #存储信息
    try:
        stu = Student(
            no=no,
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            avatar=avatar,
        )
        stu.save()
        message = '数据库存储完毕。'
    except Exception as e:
        error_message += '数据库执行错误'


# 存储文件
    try:
        _avatar_db_path = os.path.join(settings.MEDIA_ROOT, _avatar_db_path)
        with open(file=_avatar_db_path, mode='wb') as file:
            for chunk in user_file.chunks():
                file.write(chunk)
            message += '附件存储完毕'
    except Exception as e:
        error_message += '本地存储文件错误 路径错误或没有权限。'

    context = {
        'message': message,
        'error_message': error_message,
    }
    if error_message:
        return render(request, 'student/add.html', context)
    else:
        # 运行正确
        return render(request, 'student/success.html', context)

# def export_excel(request):
#     """导出所有学生列表到excel文件"""
    #数据库查询数据查询
    #数据拼成二维数组 （第一行为字段名，后面的数据行，（选做）合并前俩行、填充背景色和修改字体字号）
    #save(date,afile='media/download/student_info.xlsx')
    #redirect(to='域名/media/download/student_info.xlsx')
    # pass




def delete(request,no):
    stu_d = Student.objects.filter(no=no).delete()
    return render(request, "student/delete.html")

def update(request,stu_no):
    student = Student.objects.get(no=stu_no)
    # text = Student.objects.filter(no=student.no)
    # max_no = Student.objects.aggregate(Max('no'))
    # next_no = max_no['no__max']
    context = {
        # "text":text,
        'stu': student,
        # 'next_no': next_no
    }
    return render(request, 'student/update.html', context)


def do_update(request,stu_no):
    assert request.method == 'POST', 'error:表单http请求方式应为post'
    args = request.POST
    file = request.FILES
    no = args['no']
    file = file['avatar']
    name = args['name']
    age = args['age']
    gender = args['gender']
    phone = args['phone'] or None
    student = Student.objects.get(no=stu_no)
    student.no = no
    student.avatar = file
    student.name = name
    student.age = age
    student.gender = gender
    student.phone = phone
    student.save()
    return render(request,'student/nice.html',context={})
    # stu=Student.objects.values('name')
    # print(stu)
    # return render(request,'student/update.html')

def excel_Excel(request):
    """导出所有学生信息到HTML文件"""
    #设置HTTPResponse的类型
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="king.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('student')
    # Sheet  header,  first   row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    column = ['no','name','age','gender','phone','avatar']
    for an in range(len(column)):
        ws.write(row_num,an,column[an], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Student.objects.all().values_list('no','name','age','gender','phone','avatar')
    for row in rows:
        row_num += 1
        for an in range(len(row)):
            ws.write(row_num,an,row[an],font_style)
    wb.save(response)
    return response

def derive(request):
    # message = ''
    args = request.POST     #post请求
    # name = request.POST['name']
    # age = request.POST['age']
    # gender = request.POST['gender']
    name = args['name']
    age = args['age']
    gender = args['gender']
    if name != '' and age!='' and gender =='0':
        lsj = Student.objects.filter(name__icontains=name,age=age)
    elif name == '' and age != '' and gender == '0':
        lsj = Student.objects.filter(name__icontains=name,age=age)
    elif name != '' and age == '' and gender =='0':
        lsj = Student.objects.filter(name__icontains=name)
    elif name == '' and age == '' and gender != '0':
        lsj = Student.objects.filter(gender=gender)




    context = {
        'lsj':lsj
    }
    return render(request,'student/index.html',context)



def cloth_sale_line(request):
    #后端渲染，缺点不适合做动态图
    #获取数据，请求其他接口读数据库等
    #拼前端表格所需的变量
    legend = '销量'
    xAxis = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
    context = {}
    return render('student/8echarts.html',context)

def cloth_sale_line_api(request):
    #前后端分离，前端渲染图表，后端负责返回数据
    legend = '销量'
    xAxis = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    context = {}
    return json.dumps(context)

    # name = request.POST.get("name")
    # age = request.POST.get("age")
    # sex = request.POST.get("gender")
    # if name == 'all':
    #     text_name = Student.objects.filter(Q(question__startswith='name'))| (Q(question__startswith='age'))








# 分页功能原理
# SELECT * FROM student_student LIMIT 0,3; --学生1到3（包含3）
# SELECT * FROM student_student LIMIT 1,3; --学生2到4
# --limit跟python中的列表切片很像但参数含义不一样，limit 1， 3下标（从0开始计第一行）1,3表示向后取的行数。
# SELECT * FROM student_student LIMIT 6,3;
# SELECT count(id) AS page_amount FROM student_student;--计算总行数
#
#page_no 第几页 page_size 一页显示几条  page_amount总数据个数
#           1             10
#select * from student limit 0,(page_size);
#第1页  每页10条              0        10
#第2页                        10       10
#                             20       10
#                             start_index = (page_no-1)*page_size
#总页数                       总行除以每页数向上取整 page_amount//page_size+1
#
#student_list = Student.object.all().order_by('no')[1:3]
#    start_index = (page_no - 1) * page_size
#    end_index = page_no * page_size