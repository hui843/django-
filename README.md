djaogo学生管理
===
任务：
1.创建项目
2.创建"admin","student","teater",等APP
3.student下创建表结构："student(id,no,name,age,gender,avatar,phone,class_id,teater_id,join_time,备注)""classes(id,no,name,grade,capacity,address)""teacher(id,no,name,age,gender,avatar,salary,subject,address,phone)"

###表结构
表名 student
字段名     字段类型    注释      值示例     备注
 id        integer   表id主键
 no        integer   学号     0001    (1111000011111110 biginteger) 如果整数存储学号 vip会员号,考虑长度. 或用字符串类型.
 name       char
 age       smallint                 默认-125到125 ,正数0-255            (选做)数据库约束,0-150岁,搞不清楚,一般情况int,长数字用bigint
gender(性别) integer          smallinteger(0未填写 1男 2女 3xx) 或 char(4) 'male' 'female' 或bool(false 女 True 男) 三种设计方案均可
phone     int或char     +861237456123   0371-13789423556    400-300-222111 
avatar      char    头像      'E:/project/static/xxxavatar.jpg' request.POST.['file'].read() open('.jpg') write()
join_time    datetime  添加/入学时间
last_modified_time   datetime    上次修改时间
[fk]class_id   学生所在班级



class表
id
no  001
name  三年二班
grade 年级
capacity 容纳
address  xx校区xx号教学楼

teacher表
一些字段同student。可以用继承，但表较少，看表结构时还需要看俩个类，这里没必要用。
salary  工资
subject 主讲科目

student-teacher多对多
id
fk]student_id  1
fk]teacher_id  2

结论：一对多关系，多的一方建立外键
多对多关系，新建第三张表（id,t1_id,t2_id），包含俩表的外键。