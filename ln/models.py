from django.db import models

# Create your models here.


class Base(models.Model):
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更改时间')

    class Meta:
        abstract = True


class Department(Base):
    """
    部门组织架构
    """
    name = models.CharField(max_length=60, verbose_name="名称")
    price = models.IntegerField(verbose_name='基础工资')
    dividend = models.IntegerField(choices=((1, '3000'), (2, '5000'),
                                            (3, '8000')),
                                   null=True,
                                   blank=True,
                                   verbose_name='奖金')
    wage = models.IntegerField(null=True, blank=True, verbose_name='加班时薪')
    start = models.TimeField(null=True, blank=True, verbose_name='上班打卡时间')
    end = models.TimeField(null=True, blank=True, verbose_name='下班打卡时间')
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name="父类架构")

    class Meta:
        db_table = 'department'
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class User(Base):
    """
    员工表
    """
    name = models.CharField(max_length=50, verbose_name='姓名')
    password = models.CharField(max_length=200,
                                default='123456',
                                verbose_name='密码')
    age = models.IntegerField()
    gender = models.IntegerField(choices=((1, '男'), (2, '女')),
                                 verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    address = models.CharField(max_length=100, verbose_name='地址')
    department = models.ForeignKey(Department,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   verbose_name='所属部门')
    position_type = (
        (1, '普通员工'),
        (2, '经理'),
        (3, '科长'),
        (4, '部长'),
        (5, '总监'),
        (6, '管理层'),
        (7, '高级管理者'),
        (8, '总经理'),
    )
    position = models.IntegerField(choices=position_type,
                                   null=True,
                                   blank=True,
                                   verbose_name='职位')
    number = models.CharField(max_length=200, verbose_name='工号', unique=True)
    image = models.ImageField(upload_to='media/%Y/%m',
                              null=True,
                              blank=True,
                              default='media/default.png',
                              verbose_name='头像')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = '员工'
        verbose_name_plural = verbose_name


class Announcement(Base):
    """
    公告表
    """
    title = models.CharField(max_length=50, unique=True, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='announcementuser',
                             verbose_name='公告发起人')
    department = models.ForeignKey(Department,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='announcementdepartment')

    def __str__(self):
        return self.user.name + ':' + self.title

    class Meta:
        db_table = 'announcement'
        verbose_name = '公告'
        verbose_name_plural = verbose_name


class Salary(Base):
    """
    薪资表
    """
    overtime = models.IntegerField(null=True, blank=True, verbose_name='加班时长')
    delgold = models.IntegerField(null=True, blank=True, verbose_name='扣除金额')
    overmoney = models.IntegerField(null=True,
                                    blank=True,
                                    verbose_name='额外奖金或提成')
    department = models.ForeignKey(Department,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='salarydepartment',
                                   verbose_name='所属部门')
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='salaryuser',
                             verbose_name='所属员工')

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'salary'
        verbose_name = '薪资'
        verbose_name_plural = verbose_name


class Checking(Base):
    """
    考勤表
    早晨记录最早的一次打卡时间
    下午记录最早的一次的打卡时间
    默认全年无休的打卡，请假，出差等一律视为缺勤
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='关联员工')
    start = models.DateTimeField(verbose_name='上班打卡时间')
    end = models.DateTimeField(verbose_name='下班打卡时间')
    statu = models.IntegerField(choices=((1, '迟到'), (2, '早退'), (3, '缺勤'),
                                         (4, '正常')),
                                verbose_name='打卡状态')

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'checking'
        verbose_name = '考勤'
        verbose_name_plural = verbose_name


class Leave(Base):
    """
    请假表
    """
    type = (
        (1, '事假'),
        (2, '病假'),
        (3, '年假'),
    )
    leave_type = models.IntegerField(choices=type, verbose_name='请假类型')
    start = models.DateTimeField(verbose_name='请假日期')
    end = models.DateTimeField(verbose_name='结束日期')
    num = models.IntegerField(verbose_name='请假天数')
    reason = models.TextField(verbose_name='请假事由')
    initiator = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='leaveinitiator',
                                  verbose_name='假条发起人')
    approve = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='leaveapprove',
                                verbose_name='假条审批人')
    leader = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='leaveleader',
                               verbose_name='抄送人')
    result = models.IntegerField(choices=((1, '拒绝'), (2, '通过'), (3, '等待中')),
                                 default=3,
                                 verbose_name='审批状态')
    command = models.TextField(null=True, blank=True, verbose_name='审核结果的批示')

    def __str__(self):
        return self.initiator.name

    class Meta:
        db_table = 'leave'
        unique_together = ('initiator', 'approve', 'leader')
        verbose_name = '请假'
        verbose_name_plural = verbose_name


class Overtime(Base):
    """
    加班表
    """
    start = models.DateTimeField(verbose_name='加班日期时间')
    end = models.DateTimeField(verbose_name='结束日期时间')
    num = models.IntegerField(verbose_name='加班时长')
    reason = models.TextField(verbose_name='加班事由')
    initiator = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='overtimeinitiator',
                                  verbose_name='假条发起人')
    approve = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='overtimeapprove',
                                verbose_name='假条审批人')
    leader = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='overtimeleader',
                               verbose_name='抄送人')
    result = models.IntegerField(choices=((1, '拒绝'), (2, '通过'), (3, '等待中')),
                                 default=3,
                                 verbose_name='审批状态')
    command = models.TextField(null=True, blank=True, verbose_name='审核结果的批示')

    def __str__(self):
        return self.initiator.name

    class Meta:
        db_table = 'overtime'
        unique_together = ('initiator', 'approve', 'leader')
        verbose_name = '加班'
        verbose_name_plural = verbose_name


class Evection(Base):
    """
    出差表
    """
    destination = models.CharField(max_length=200, verbose_name='目的地')
    start = models.DateTimeField(verbose_name='出差日期')
    end = models.DateTimeField(verbose_name='结束出差日期')
    num = models.IntegerField(verbose_name='出差天数')
    reason = models.TextField(verbose_name='出差事由')
    initiator = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='evectioninitiator',
                                  verbose_name='出差发起人')
    approve = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='evectionapprove',
                                verbose_name='出差审批人')
    leader = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='evectionleader',
                               verbose_name='抄送人')
    result = models.IntegerField(choices=((1, '拒绝'), (2, '通过'), (3, '等待中')),
                                 default=3,
                                 verbose_name='审批状态')
    command = models.TextField(null=True, blank=True, verbose_name='审核结果的批示')

    def __str__(self):
        return self.initiator.name

    class Meta:
        db_table = 'evection'
        unique_together = ('initiator', 'approve', 'leader')
        verbose_name = '出差'
        verbose_name_plural = verbose_name


class Log(Base):
    """
    日志
    """
    type = ((1, '日报'), (2, '周报'), (3, '月报'))
    log_type = models.IntegerField(choices=type, verbose_name='日志类型')
    work = models.TextField(verbose_name='今日工作')
    unfinished = models.TextField(verbose_name='未完成工作')
    initiator = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='loginitiator',
                                  verbose_name='日志发出人')
    leader = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='logleader',
                               verbose_name='抄送人')

    def __str__(self):
        return self.initiator.name

    class Meta:
        db_table = 'log'
        verbose_name = '日志'
        verbose_name_plural = verbose_name
