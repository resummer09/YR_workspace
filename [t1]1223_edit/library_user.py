import datetime
import csv


class User:
    def __init__(self, user_id, user_pw, name, country, phone, question, answer):
        self.user_id = user_id  # 아이디
        self.user_pw = user_pw  # 비밀번호
        self.name = name  # 이름
        self.country = country  # 내/외국인
        self.phone = phone  # 전화번호
        self.question = question  # 회원 확인 질문
        self.answer = answer  # 회원 확인 질문에 대한 답변
        self.status = '정상회원'  # 회원 상태, 대여 가능 시 '정상회원', 연체 시 '연체회원'
        self.ban_date = None  # 날짜형식으로 들어갈 예정
        self.book1 = None
        self.book2 = None
        self.book3 = None
        self.book4 = None
        self.book5 = None

    def change_info(self, user_pw, phone):
        if user_pw != '':
            self.user_pw = user_pw
        if phone != '':
            self.phone = phone

    def rental_ban(self, rental_date, ):
        today = datetime.datetime.now()
        date = f"{today.year}-{today.month}-{today.day}"
        self.ban_date = date  # 날짜형식으로 들어갈 예정 (yyyy-mm-dd)

    def return_info(self):
        s = f"{self.user_id},{self.user_pw},{self.name},{self.country},{self.phone},{self.question},{self.answer}," \
            f"{self.status},{self.ban_date},{self.book1},{self.book2},{self.book3},{self.book4},{self.book5}"
        return s

    def set_now(self, info):
        print("들어옴?")
        self.user_id = info[0]  # 아이디
        self.user_pw = info[1]  # 비밀번호
        self.name = info[2]  # 이름
        self.country = info[3]  # 내/외국인
        self.phone = info[4]  # 전화번호
        self.question = info[5]  # 회원 확인 질문
        self.answer = info[6]  # 회원 확인 질문에 대한 답변
        self.status = info[7]  # 회원 상태
        self.ban_date = info[8]  # 연체일자
        self.book1 = info[9]  # 대여한 책
        self.book2 = info[10]  # 대여한 책
        self.book3 = info[11]  # 대여한 책
        self.book4 = info[12]  # 대여한 책
        self.book5 = info[13]  # 대여한 책

