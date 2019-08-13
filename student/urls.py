from django.urls import path

from . import views
urlpatterns = [
    path('index/',views.index,name='index'),
    path('index2/',views.index2,name='index2'),
    path('add/',views.add,name='add'),
    path('<int:stu_no>/update/',views.update,name='update'),
    path('<int:stu_no>/do_update/',views.do_update,name='do_update'),
    path('do_add',views.do_add,name='do_add'),
    path('<int:no>/delete/',views.delete,name='delete'),
    path('derive/',views.derive,name='derive'),
    path(r'~excel_Excel/xls/$',views.excel_Excel,name='excel_Excel'),
    path('api/index/',views.api_index,name='api_index')
]

#大多数情况俩种方式可互换
#方式一：入过参数就1一个，且与业务关系较大，适合动态url匹配方式。  bili.ocm/av/58888/   path(av/<av_id>).视图函数的参数获取到。
#方式二：参数较多。适合query string，url后？传参。
#bili.com/news/?page_no=2&page_site=2 ,path('news/') ,视图函数中request.GET['page_no']
