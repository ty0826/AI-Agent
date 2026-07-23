import json
from abc import ABC, abstractmethod


class Book:
    def __init__(self, order_id, title, author, num):
        self.order_id = order_id
        self.title = title
        self.author = author
        self.__num = num

    def borrow_book(self):
        if self.__num > 0:
            self.__num -= 1
            return True
        return False

    def return_book(self):
        self.__num += 1

    def get_num(self):
        return self.__num


# 抽象类：是一种只能被继承不能被实例化的类，作用是规定子类必须要实现哪些方法，强制子类必须遵守唯一的代码规范
# python中的抽象类：需要继承abc模版里的ABC类
class Member(ABC):
    def __init__(self, member_id, name, password):
        self.member_id = member_id
        self.name = name
        self.__password = password
        self.__borrowed_book = []

    def borrow_book(self, book: Book):
        if len(self.__borrowed_book) > self.get_max_num():
            print(f"已经达到最大借阅数，请先退还")
            return False
        if book in self.__borrowed_book:
            print(f"{book.title}已经借阅，请选择其他的！")
            return False
        if book.borrow_book():
            self.__borrowed_book.append(book)
            print(f"{book.title} 借阅成功！")
            return True
        else:
            print(f"{book.title} 库存不足！")
            return False

    def return_book(self, book: Book):
        if book in self.__borrowed_book:
            self.__borrowed_book.remove(book)
            print(f"{book.title} 归还成功！")
            book.borrow_book()
            return True
        print(f"{book.title} 不在库里！")
        return False

    def get_password(self):
        return self.__password

    def get_borrowed_book(self):
        return self.__borrowed_book

    @abstractmethod  # 子类里需要重写这个方法
    def get_max_num(self) -> int:
        pass


class VipMember(Member):
    def __init__(self, member_id, name, password, level):
        Member.__init__(self, member_id, name, password)
        self.level = level

    def get_max_num(self) -> int:
        return 6 + self.level


class NormalMember(Member):
    def get_max_num(self) -> int:
        return 3


class LibrarySystem:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.current_member: Member | None = None
        self.get_load_book()
        self.get_load_member()

    def get_load_book(self):
        with open('./data/books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
            for book in books:
                self.books[book['编号']] = Book(book['编号'], book['标题'], book['作者'], book['数量'])
            print(f"图书数据加载成功！")

    def get_load_member(self) -> Member | None:
        with open('./data/members.json', 'r', encoding='utf-8') as f:
            members = json.load(f)
            for member in members:
                if member['卡号'].startswith('N'):
                    self.members[member['卡号']] = NormalMember(member['卡号'], member['姓名'], member['密码'])
                elif member['卡号'].startswith('V'):
                    self.members[member['卡号']] = VipMember(member['卡号'], member['姓名'], member['密码'],
                                                             member['会员等级'])
            print(f"图书人员加载成功！")

    def login(self):
        while True:
            print("【登录】")
            member_id = input("请输入会员卡卡号：")
            password = input("请输入会员卡密码：")
            if member_id not in self.members:
                print("登陆失败！会员卡号不存在！")
                continue
            member = self.members[member_id]
            if member.get_password() == password:
                self.current_member = member
                print(f"登录成功！{member.name}")
                return True
            else:
                print('账号密码错误，请重新输入！')
                continue

    def borrow_book(self):
        for book in self.books.values():
            print(f"编号:{book.order_id},标题:{book.title},作者:{book.author},库存数:{book.get_num()}")

        input_order = input("请输入图书编号：")
        if input_order not in self.books:
            print("借阅失败，请重新输入！")
            return False
        self.current_member.borrow_book(self.books[input_order])

    def return_book(self):
        borrowed_book = self.current_member.get_borrowed_book()
        for books in borrowed_book:
            print(f"编号：{books.order_id},标题：{books.title}")
        input_order = input("请输入图书编号：")
        if input_order not in self.books:
            print("还书失败，请重新输入！")
            return False
        self.current_member.return_book(self.books[input_order])

    def show_borrowed_books(self):
        borrowed_book = self.current_member.get_borrowed_book()
        if len(borrowed_book) > 0:
            for books in borrowed_book:
                print(f"编号：{books.order_id},标题：{books.title}")
        else:
            print("暂未借阅相关图书！")

    def run(self):
        if self.login():
            while True:
                print('\n 1、借阅图书')
                print("2、归还图书")
                print("3、查看借阅")
                print("4、退出系统")
                choice = input("请输入操作（1-4）：")
                match choice:
                    case "1":
                        self.borrow_book()
                    case "2":
                        self.return_book()
                    case "3":
                        self.show_borrowed_books()
                    case "4":
                        print("退出系统！")
                        break
                    case _:
                        print("输入错误，请重新输入！")


if __name__ == '__main__':
    LibrarySystem = LibrarySystem()
    LibrarySystem.run()
