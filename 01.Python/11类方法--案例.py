class Student:
    def __init__(self, name, chinese, math, english):
        self.name = name
        self.chinese = chinese
        self.english = english
        self.math = math

    def __str__(self):
        return f"姓名：{self.name},语文：{self.chinese},数学：{self.math},英语：{self.english}"

    def update_data(self, chinese=None, math=None, english=None):
        if chinese is not None:
            self.chinese = chinese
        if english is not None:
            self.english = english
        if math is not None:
            self.math = math


class EduManagement:
    def __init__(self):
        self.students = []

    def add_student(self):
        name = input('请输入添加的考生姓名：')
        for s in self.students:
            if s.name == name:
                print('该考生已存在！')
                return

        chinese = float(input('请输入语文成绩:'))
        math = float(input('请输入数学成绩：'))
        english = float(input('请输入英语成绩：'))
        stu = Student(name, chinese, math, english)
        self.students.append(stu)
        print('考生新增成功！')

    def del_student(self):
        name = input('请输入需要删除的考生姓名：')
        for s in self.students:
            if s.name == name:
                self.students.remove(s)
                print("考生信息删除成功！")
                return
            else:
                print('没有匹配到考生数据，请重新输入！')
                return

    def update_student(self):
        name = input('请输入更新的考生姓名：')
        for s in self.students:
            if s.name == name:
                chinese = float(input('输入语文成绩：'))
                math = float(input('输入数学成绩：'))
                english = float(input('请输入英语成绩：'))
                s.update_data(chinese, math, english)
                print("成绩修改成功！")
                print(f"修改之后的成绩是：{s}")
                return
            else:
                print('未匹配到考生，请重新输入！')
                return

    def query_student_all(self):
        for s in self.students:
            print(s)

    def query_student(self):
        name = input('请输入需要删除的考生姓名：')
        for s in self.students:
            if s.name == name:
                print(s)

    def run(self):
        print('欢迎使用教务管理系统！')
        while True:
            print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
            print('# 1、添加学生 2、修改学生 3、删除学生 4、查询所有学生 5、查询特定学生 6、退出#')
            print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
            chioce = int(input("请选择要执行的操作，1-6"))
            match chioce:
                case 1:
                    self.add_student()
                case 2:
                    self.update_student()
                case 3:
                    self.del_student()
                case 4:
                    self.query_student_all()
                case 5:
                    self.query_student()
                case 6:
                    break
                case _:
                    print('请重新输入！')


if __name__ == '__main__':
    EduManagement = EduManagement()
    EduManagement.run()
