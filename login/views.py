import hashlib
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import User

# Create your views here.
def index(request):
    #假设 服务器判断 request.cookie['session_id'],session_id没有或不正确禁止登录，重新定向到登录页面
    # print(request.session['is_login'])
    return render(request, 'login/index.html', context={})

def register(request):
    """GET  返回注册表单"""
    if request.method == 'GET':
        return render(request,'login/register.html',context={})
    elif request.method == 'POST':
        context = {}
        name = request.POST['name']
        password = request.POST['password']
        #密码加密 # 也可以 from django.contrib.auth.hashers
        md5 = hashlib.md5()
        md5.update(password.encode())
        hash_password = md5.hexdigest()
        #验证 用户名、密码是否在长度范围内  len()  #判断字符串是否纯中文
        if len(name) <=1:
            #讲ajax时的反倒
            context['crror_message'] = '用户名太短'
            return render(request,'login/register.html',context)
        user = User(name=name,password=password,hash_password=hash_password)
        user.save()
        # print(name,password)
        return redirect(to='/login/login')#成功返回首页
        # return render(request,'login/register.html',context) #失败
def register_check(request):
    """检查注册参数，返回json结果"""
    # :param   客户端的表单请求  name字段
    # :method   请求方式  POST
    # :return  json格式的字符串
    #
    # {
    #     "code":100,          #200成功
    #     "status":"faild",         #ok成功
    #     "error_message":"",      #用户名太短等。。。
    # }

    import json
    resp_obj = {}
    name = request.POST['name']
    context = {}
    if len(name) <= 1:
        # 讲ajax时的反倒
        context['crror_message'] = '用户名太短'
        resp_obj = {
            'code':100,
            'status':'验证失败',
            'error_message':'用户名太短'
        }
        resp_json = json.dumps(resp_obj)
        print(type(resp_obj))
        print(type(resp_json))
        return HttpResponse(resp_json)

def do_register(request):
    pass

def login(request):
    if request.method == 'GET':
        return render(request,'login/login.html',context={})
    elif request.method == 'POST':
        context = {}
        name = request.POST['name']
        password = request.POST['password']

        user_list = User.objects.filter(name=name,password=password) #多个where条件逗号分隔，代表and连接条件。
        #多条件可以用Q对象from django.db.models import Q
        # User.objects.filter(Q(name=xxxx)&Q(password=xxxx))
        if user_list:
            # 登录成功

            #user_list[0].name + time.now() 通过hash生成session_id
            #return HTTPResponse set_cookie响应头把数据存到自己的cookie中
            #之后客户端每一次请求，都会带上cookie，服务器就会比对是否存在，存在即用户已登录
            #django已经封装了方法，我们可以简单在响应头里设置cookie
            request.session['is_login'] = True
            request.session['username'] = user_list[0].name
            request.COOKIES['is_login'] = True
            request.session['username'] = user_list[0].name
            context = {'message':'登录成功'}
            # return render(request,'login/index.html',context)
            return redirect(to='/student/index/')
        else:
            #登录失败
            if User.objects.filter(name=name).exists():  #检测用户名是否存在
                context['message'] = '密码错误'
                # return render(request, 'login/login.html', context)
            else:
                context['message'] = '用户名不存在，请先注册'
            return render(request, 'login/login.html', context)

# def login(request):
#     if request.method == 'GET':
#         return render(request,'login/login.html',context={})
#     elif request.method == 'POST':
#         context = {}
#         name = request.POST['name']
#         password = request.POST['password']
#
#         user_list = User.objects.filter(name=name,password=password)   # 多个where条件逗号分隔， 代表and连接条件。
#         # 多条件可以用Q对象
#         # from django.db.models import Q
#         # User.objects.filter(Q(name=1111)&Q(password=2222))
#
#         if user_list:
#             # 登录成功
#
#             # 原理:
#             # user_list[0].name + time.now()    通过hash生成session_id
#             # HttpResponse set_cookie ['session_id':'dfghidsuyg3476#%']
#             # 客户端接收到响应 根据set_cookie响应头把数据库存到自己的cookie中
#             # 之后客户端每一次请求,都会带上cookie. 服务器就会对比是否存在,存在即用户已登录.
#             # django已经封装了方法.我们可以简单在响应头里面设置cookie
#             request.session['is_login'] = True
#             request.session['username'] = user_list[0].name
#             request.COOKIES['is_login'] = True
#             request.COOKIES['username'] = user_list[0].name
#             context = {'message': '登录成功'}
#             return render(request,'login/index.html',context)
#             return redirect(to='/login/index/')
#         else:
#             # 登录失败
#             if User.objects.filter(name=name).exists():
#                 context['message'] = '密码错误'
#                 # return render(request,'login/login.html',context)
#             else:
#                 context['message'] = '用户不存在，请先注册'
#             return render(request, 'login/login.html', context)

def register_email_active(request):
    """用户提交注册信息后，需要邮件激活"""
    #发一封邮件
    #active = user.name 经过base64或sha加密   #lskjefFE
    #active_url = '127.0.0.1:port' + '/login/email_active/' + 'user_id_encrvp'
    #发一封邮件
def email_active(request):
    user_id = request.GET['user_id_']

def do_login(request):
    pass

def logout(request):
    request.session.flush()  #清除session
    #统计在线人数，读django_session表行数，自己测试注意用不同的浏览器登录
def auth(request):
    return render(request,'')