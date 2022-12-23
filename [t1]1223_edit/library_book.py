import csv
import datetime


# 도서 클래스
class Book:
    def __init__(self, book_data):
        self.serial_num = book_data[0]  # 연번
        self.library = book_data[1]  # 소장도서관명
        self.location = book_data[2]  # 자료실
        self.regist_num = book_data[3]  # 등록번호
        self.title = book_data[4]  # 도서명
        self.writer = book_data[5]  # 저자
        self.publisher = book_data[6]  # 출판사
        self.year_of_publication = book_data[7]  # 출판연도
        self.call_sign = book_data[8]  # 청구기호
        self.date = book_data[9]  # 데이터기준일자
        self.rental_date = book_data[10]  # 대출일
        self.return_date = book_data[11]  # 반납 예정일
        self.status = book_data[12]  # 대여 상태


def books_database(file_name):  # csv 파일을 열어 데이터로 변환
    # 도서관 공공데이터 csv를 읽기 전용으로 연다
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        # csv.reader(file)로 라인을 읽어들인다
        lines = csv.reader(file)
        books_db = []
        # for문으로 line을 book_list에 추가
        # 연번 - 소장도서관명 - 자료실 - 등록번호 - 도서명 - 저자 - 출판사 - 출판연도 - 청구기호 - 데이터기준일자
        for row in lines:
            books_db.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                             row[11], row[12]))
    # 설명이 적혀있는 0번 인덱스 삭제
    del books_db[0]
    return books_db


def create_books(books_db: list):  # 변환된 데이터로 Book 클래스의 인스턴스 생성
    books = {}
    for book_data in books_db:
        books[book_data[4]] = Book(book_data)
    return books


def search_book(books, keyword, option):  # 1개 옵션으로 조회(책 딕셔너리, 검색키워드)  -- 딕셔너리 반환
    result = {}  # 결과를 반환할 딕셔너리
    for book in books:  # books 딕셔너리 전체 조회
        if option == '저자':
            if keyword in str(books[book].writer):  # 저자명이 검색 키워드를 포함하고 있다면
                result[books[book].title] = book  # 결과 딕셔너리에 객체 추가
        elif option == '제목':
            if keyword in str(books[book].title):  # 제목이 검색 키워드를 포함하고 있다면
                result[books[book].title] = book  # 결과 딕셔너리에 객체 추가
        elif option == '출판사':
            if keyword in str(books[book].publisher):  # 출판사명이 검색 키워드를 포함하고 있다면
                result[books[book].title] = book  # 결과 딕셔너리에 객체 추가
        elif option == '등록번호':
            if keyword == str(books[book].regist_num):  # 등록번호가 검색 키워드와 일치한다면
                result[books[book].title] = book  # 결과 딕셔너리에 객체 추가
    return result


def save_book_data(file_name, books):  # 프로그램 종료시 csv 파일 저장
    # 파일을 쓰기 전용으로 연다
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        w = csv.writer(file)
        row_first = '연번,소장도서관명,자료실명,등록번호,도서명,저자,출판사,출판연도,청구기호,데이터기준일자,대여일,반납예정일,상태'.split(',')
        w.writerow(row_first)
        for book in books:
            row_data = (books[book].serial_num, books[book].library, books[book].location, books[book].regist_num,
                        books[book].title, books[book].writer, books[book].publisher, books[book].year_of_publication,
                        books[book].call_sign, books[book].date, books[book].rental_date, books[book].return_date,
                        books[book].status)
            w.writerow(row_data)
