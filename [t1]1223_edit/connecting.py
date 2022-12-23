import csv
import sys
import re
import time
import random
from datetime import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
from library_user import *
### 도서 모듈 추가
from library_book import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui_library.ui")[0]


class WindowClass(QMainWindow, form_class):
    temp_id = None
    isCheck = False
    login = False
    now_user = None
    find_id = None
    find_pw = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ### 도서관 이름 타이틀로 설정 / 프로그램 아이콘 설정
        self.setWindowTitle("첨단 도서관")
        self.setWindowIcon(QIcon("0.img_window_icon.png"))
        ### 창 크기 고정
        self.setFixedSize(QSize(1000, 950))

        self.stackedWidget.setCurrentIndex(0)  # 초기화면
        self.btn_loginpage.clicked.connect(self.to_login)  # 메인1의 로그인 버튼 누르면 로그인 페이지로 이동
        self.btn_login.clicked.connect(self.to_main2)  # 로그인 페이지의 로그인 버튼 누르면 메인2 화면으로 이동
        self.btn_join.clicked.connect(self.to_join)  # 로그인 페이지의 회원가입 버튼 누르면 회원가입 화면으로 이동
        self.btn_main2.clicked.connect(self.to_main1)  # 회원가입 페이지의 메인 버튼 누르면 메인1화면으로 이동
        self.btn_main.clicked.connect(self.to_main1)  # 로그인 페이지의 메인 버튼 누르면 메인1화면으로 이동
        self.btn_join2.clicked.connect(self.to_login2)  # 회원가입 페이지의 회원가입 버튼누르면 로그인화면으로 이동
        self.btn_logout.clicked.connect(self.to_main1)  # 메인2페이지의 로그아웃 버튼 누르면 메인1화면으로 이동
        self.btn_check.clicked.connect(self.id_check)  # 회원가입페이지의 중복확인 버튼
        self.join_id.textChanged.connect(self.id_join_check)  # 회원가입페이지의 id입력란에 텍스트가 변할때 작동됨
        self.join_verify_pw1.textChanged.connect(self.pw_check_join)  # 회원가입 페이지의 비밀번호 확인란에서 다른곳으로 커서가 바뀔때 작동됨
        self.btn_booksearch.clicked.connect(self.to_booksearch)  # 메인1의 도서조회 버튼 누르면 도서조회 화면으로 이동
        self.btn_booksearch2.clicked.connect(self.to_booksearch)  # 메인2의 도서조회 버튼 누르면 도서조회 화면으로 이동
        self.btn_mypage.clicked.connect(self.to_mypage)  # 메인2의 마이페이지 버튼 누르면 마이페이지 화면으로 이동
        self.btn_main3.clicked.connect(self.to_main3)  # 도서조회페이지의 메인 버튼 누르면 로그아웃상태(메인1), 로그인상태(메인2)로 이동
        self.btn_cancel.clicked.connect(self.to_main4)  # 마이페이지의 회원정보수정 탭에서 취소 버튼 누르면 메인2화면으로 이동
        self.btn_main4.clicked.connect(self.to_main4)  # 마이페이지의 대여현황창 탭에서 메인 버튼 누르면 메인2화면으로 이동
        self.edit_verify_pw1.textChanged.connect(self.pw_check_change)  # 마이페이지-회원정보수정 탭의 비밀번호 확인란에서 다른곳으로 커서가 바뀔때 작동됨
        self.btn_search.clicked.connect(self.book_lookup)  # 도서조회페이지의 도서 조회 - 검색버튼 누르면 : 조회
        self.btn_idpw_lookup.clicked.connect(self.idpw_lookup)
        self.btn_id_lookup.clicked.connect(self.id_lookup)  # 아이디찾기페이지에서 찾기버튼 누르면
        self.btn_pw_lookup.clicked.connect(self.pw_lookup)  # 비밀번호찾기페이지에서 찾기버튼 누르면
        self.name_id_lookup.textChanged.connect(self.all_insert1)
        self.tel_id_lookup.textChanged.connect(self.all_insert1)
        self.answer_id_lookup.textChanged.connect(self.all_insert1)
        self.id_pw_lookup.textChanged.connect(self.all_insert2)
        self.tel_pw_lookup.textChanged.connect(self.all_insert2)
        self.answer_pw_lookup.textChanged.connect(self.all_insert2)
        self.btn_id_cancel.clicked.connect(self.to_login)  # 아이디찾기 페이지에서 취소버튼 누르면 로그인페이지로 이동
        self.btn_pw_cancel.clicked.connect(self.to_login)  # 비밀번호찾기 페이지에서 취소버튼 누르면 로그인페이지로 이동

        ### 메인1화면 공지사항 링크 12-22 20:19
        self.notice_01.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3364?query=">첨단도서관 [크리스마스랑, 책이랑] 프로그램 안내</a>')
        self.notice_01.setOpenExternalLinks(True)
        self.notice_02.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3350">1인가구를 위한 홈스타일링 강의 안내</a>')
        self.notice_02.setOpenExternalLinks(True)
        self.notice_03.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3332">첨단도서관 시인과 함께하는 힐링인문학</a>')
        self.notice_03.setOpenExternalLinks(True)
        self.notice_04.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3330">첨단도서관 임시 휴관 안내</a>')
        self.notice_04.setOpenExternalLinks(True)
        ### 메인2화면 공지사항 링크 12-23 03:08
        self.notice_05.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3364?query=">첨단도서관 [크리스마스랑, 책이랑] 프로그램 안내</a>')
        self.notice_05.setOpenExternalLinks(True)
        self.notice_06.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3350">1인가구를 위한 홈스타일링 강의 안내</a>')
        self.notice_06.setOpenExternalLinks(True)
        self.notice_07.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3332">첨단도서관 시인과 함께하는 힐링인문학</a>')
        self.notice_07.setOpenExternalLinks(True)
        self.notice_08.setText(
            '<a href="https://lib.gwangsan.go.kr/CD/board/3/1/read/3330">첨단도서관 임시 휴관 안내</a>')
        self.notice_08.setOpenExternalLinks(True)
        # self.btn_pw_lookup.clicked.connect(self.id_lookup) #질문

    def keyPressEvent(self, e):  # esc 입력시 종료 함수
        if e.key() == Qt.Key_Escape:
            # 다 끝내고 마무리할 때 정말 종료할 건지 확인하는 알림창 띄우기
            self.close()

    def to_main1(self):  # 메인1화면으로 이동
        self.now_user = None
        print(self.now_user)
        self.out_join()
        self.login_pw.setText('')  # 로그아웃시 pw입력란 초기화
        self.login = False
        self.stackedWidget.setCurrentIndex(0)

    def out_join(self):  # 텍스트 입력란 초기화 함수
        self.join_id.setText('')
        self.join_pw.setText('')
        self.join_verify_pw1.setText('')
        self.join_name.setText('')
        self.join_tel.setText('')
        self.answer.setText('')

    def to_login(self):  # 로그인 페이지로 이동
        self.stackedWidget.setCurrentIndex(1)

    def to_login2(self):  # 회원가입 페이지의 회원가입 버튼누르면 미입력란 확인 후 로그인화면으로 이동
        # self.out_join()
        print(self.radio_local.isChecked())
        print(self.radio_foreigner.isChecked())
        print(not self.radio_local.isChecked() and not self.radio_foreigner.isChecked())
        print(self.answer.text(), end='1')
        if (self.join_id.text() == "" or self.join_pw.text() == "" or self.join_verify_pw1.text() == "" or
            self.join_name.text() == "" or self.join_tel.text() == "" or self.answer.text() == '') or \
                not self.radio_local.isChecked() and not self.radio_foreigner.isChecked():
            QMessageBox.information(self, "알림", "모든 항목을 입력해주세요")
        else:
            if self.temp_id != self.join_id.text() or not self.isCheck:
                QMessageBox.information(self, "알림", "아이디 중복 확인")
            elif self.join_pw.text() != self.join_verify_pw1.text():
                QMessageBox.information(self, "알림", "비밀번호 확인")
            else:
                user_id = self.join_id.text()
                user_pw = self.join_pw.text()
                name = self.join_name.text()
                country = self.radio_local.text() if self.radio_local.isChecked() else self.radio_foreigner.text()
                phone = self.join_tel.text()
                question = self.comboBox.currentText()
                answer = self.answer.text()
                new_user = User(user_id, user_pw, name, country, phone, question, answer)
                file = open('db_users.csv', 'a', newline='', encoding='utf-8-sig')
                w = csv.writer(file)
                data = new_user.return_info().split(',')
                w.writerow(data)
                file.close()
                QMessageBox.information(self, "알림", "가입에 성공하셨습니다.")
                self.out_join()
                self.stackedWidget.setCurrentIndex(1)

    def id_check(self):
        check_ok = True
        file = open('db_users.csv', 'r', newline='', encoding='utf-8-sig')
        line = csv.reader(file)
        for i in line:  # [아이디, 비밀번호, ...]
            if i[0] == self.join_id.text():
                QMessageBox.information(self, "알림", "이미 사용 중인 아이디")
                check_ok = False
                break
        if check_ok:
            self.temp_id = self.join_id.text()
            self.isCheck = True
            QMessageBox.information(self, "알림", "사용 가능 아이디")
        file.close()

    def id_join_check(self):  # 회원가입 시 아이디 유효성검사
        id_word = self.join_id.text()
        for i in id_word:
            if (47 < ord(i) < 58) or (64 < ord(i) < 91) or (96 < ord(i) < 123):
                self.join_id_chk_msg.setText("사용 가능 아이디")
                self.btn_check.setEnabled(True)
                if len(self.join_id.text()) < 4:
                    self.join_id_chk_msg.setText("4자 이상 입력")
                    self.btn_check.setEnabled(False)
            else:
                self.join_id2.setText("영문 또는 숫자 입력")
                self.btn_check.setEnabled(False)

    def to_join(self):  # 회원가입 화면으로 이동
        self.stackedWidget.setCurrentIndex(2)

    def to_main2(self):  # 로그인 화면 미입력시 메시지박스 호출
        done = True
        if self.login_id.text() == "":
            QMessageBox.information(self, "알림", "id를 입력해주세요")
        elif self.login_pw.text() == "":
            QMessageBox.information(self, "알림", "비밀번호를 입력해주세요")
        else:  # 여기에서 데이터베이스랑 값 비교
            file = open('db_users.csv', 'r', newline='', encoding='utf-8-sig')
            line = csv.reader(file)
            for i in line:  # [아이디, 비밀번호, ...]
                if i[0] == self.login_id.text():
                    done = True
                    print(i[0], end='\t')
                    if i[1] == self.login_pw.text():
                        print(i[1])
                        QMessageBox.information(self, "알림", "로그인 성공")
                        books_db = books_database('lib_cd.csv')
                        books = create_books(books_db)

                        self.now_user = User(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                        self.now_user.set_now(i)
                        print(self.now_user.return_info())

                        self.stackedWidget.setCurrentIndex(3)
                        self.welcome_msg.setText(f"{i[2]} 님 환영합니다.")
                        book_list = [self.now_user.book1, self.now_user.book2, self.now_user.book3, self.now_user.book4,
                                     self.now_user.book5]
                        book_list = sort_book(book_list)

                        # self.table_rental.setRowCount(5)
                        # for title in book_list:
                        #     late = datetime.date.today() - books[title].return_date
                        #     self.table_rental.setCellWidget(i, 0, QCheckBox())
                        #     self.table_rental.setItem(i, 1, QTableWidgetItem(books[title].library))
                        #     self.table_rental.setItem(i, 2, QTableWidgetItem(books[title].title))
                        #     self.table_rental.setItem(i, 3, QTableWidgetItem(books[title].writer))
                        #     self.table_rental.setItem(i, 4, QTableWidgetItem(books[title].publisher))
                        #     self.table_rental.setItem(i, 5, QTableWidgetItem(books[title].year_of_publication))
                        #     self.table_rental.setItem(i, 6, QTableWidgetItem(str(books[title].rental_date)))
                        #     self.table_rental.setItem(i, 7, QTableWidgetItem(str(books[title].return_date)))
                        #     self.table_rental.setItem(i, 8, QTableWidgetItem(str(late.days)))
                        #     self.table_rental.setItem()

                        self.login = True
                        break
                    else:
                        QMessageBox.information(self, "알림", "비밀번호가 일치하지 않습니다")
                        break
                else:
                    done = False
            if not done:
                QMessageBox.information(self, "알림", "존재하지 않는 아이디입니다")
                self.login = False
            file.close()

    def pw_check_join(self):  # 비밀번호 유효성검사
        if self.join_pw.text() == self.join_verify_pw1.text():  # pw 와 pw 확인 값이 같아야함
            self.join_verify_pw2.setText("확인완료")
        print(len(self.join_verify_pw1.text()))
        print(self.join_verify_pw1.text().isdigit())
        print(self.join_verify_pw1.text().isalpha())
        if len(self.join_verify_pw1.text()) < 8 or \
                self.join_verify_pw1.text().isdigit() or self.join_verify_pw1.text().isalpha():  # 8자 이상 숫자,문자혼용
            self.join_verify_pw2.setText("영문, 숫자를 혼용하여 8자 이상 입력하세요")
        if self.join_pw.text() != self.join_verify_pw1.text():
            self.join_verify_pw2.setText("비밀번호가 틀립니다.")

    def pw_check_change(self):  # 회원수정에서 비밀번호 유효성검사
        if self.edit_pw.text() == self.edit_verify_pw1.text():  # pw 와 pw 확인 값이 같아야함
            self.edit_verify_pw2.setText("확인완료")
        print(len(self.edit_verify_pw1.text()))
        print(self.edit_verify_pw1.text().isdigit())
        print(self.edit_verify_pw1.text().isalpha())
        if len(self.edit_verify_pw1.text()) < 8 or \
                self.edit_verify_pw1.text().isdigit() or self.edit_verify_pw1.text().isalpha():  # 8자 이상 숫자,문자혼용
            self.edit_verify_pw2.setText("영문, 숫자를 혼용하여 8자 이상 입력하세요")
        if self.edit_pw.text() != self.edit_verify_pw1.text():
            self.edit_verify_pw2.setText("비밀번호가 틀립니다.")

    def to_booksearch(self):
        self.stackedWidget.setCurrentIndex(4)

    def to_mypage(self):
        self.stackedWidget.setCurrentIndex(6)

    def to_main3(self):
        if self.login:
            print(True)
            self.table_search.setRowCount(0)
            self.search_title.clear()
            self.search_writer.clear()
            self.search_publisher.clear()
            self.search_renum.clear()
            self.stackedWidget.setCurrentIndex(3)
        else:
            print(False)
            self.table_search.setRowCount(0)
            self.search_title.clear()
            self.search_writer.clear()
            self.search_publisher.clear()
            self.search_renum.clear()
            self.stackedWidget.setCurrentIndex(0)

    def to_main4(self):
        self.stackedWidget.setCurrentIndex(3)

    ### 대여 버튼 - 업데이트 12-22 20:17
    def book_lookup(self):
        books_db = books_database('lib_cd.csv')  # 첨단 도서관 데이터
        books = create_books(books_db)  # { '책 제목' : 객체 } 딕셔너리
        # 공백이 아닐 때 검색을 실행하는 lambda 함수
        check = lambda x, y: search_book(books, x, y) if x != '' else False
        # 공백이 아닌 칸의 검색 결과를 담는 리스트
        result = []
        # check로 검사할 검색 조건
        optional = [
            [self.search_title.text(), '제목'],
            [self.search_writer.text(), '저자'],
            [self.search_publisher.text(), '출판사'],
            [self.search_renum.text(), '등록번호']]
        # 공백이 아닌 칸의 검사 결과를 result에 추가
        for option in optional:
            if check(option[0], option[1]):
                result.append(check(option[0], option[1]))
        # result의 값이 1이라면 최종 결과는 해당 값,2 이상이라면 최종 결과는 교집합
        search_result = []
        if len(result) > 1:
            search_result = result[0]
            for btn in range(len(result)):
                if btn == 0:
                    continue
                search_result = set(search_result) & set(result[btn])
        elif len(result) == 1:
            search_result = result[0]
        self.table_search.setRowCount(len(search_result))

        btnList = []
        col = 0
        status_view = lambda x: '' if x is None else x
        button_set = lambda x: False if x == '대여중' else True
        for res in search_result:
            self.table_search.setItem(col, 0, QTableWidgetItem(books[res].library))  # 소장도서관명
            self.table_search.setItem(col, 1, QTableWidgetItem(books[res].title))  # 도서명
            self.table_search.setItem(col, 2, QTableWidgetItem(books[res].location))  # 자료실
            self.table_search.setItem(col, 3, QTableWidgetItem(books[res].regist_num))  # 등록번호
            self.table_search.setItem(col, 4, QTableWidgetItem(books[res].writer))  # 저자
            self.table_search.setItem(col, 5, QTableWidgetItem(books[res].publisher))  # 출판사
            self.table_search.setItem(col, 6, QTableWidgetItem(books[res].year_of_publication))  # 출판연도

            btn = QPushButton(books[res].status)
            btnList.append(btn)  # btn 위치 : btnList[col]
            self.table_search.setCellWidget(col, 7, btn)
            btn.clicked.connect(self.rental_click)  # 버튼 시그널 추가
            btn.setEnabled(button_set(books[res].status))

            self.table_search.setItem(col, 8, QTableWidgetItem(status_view(books[res].return_date)))
            col += 1

        # 행 크기를 내용에 맞춰 조절하는 코드
        self.table_search.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    ###
    def rental_click(self):
        books_db = books_database('lib_cd.csv')  # 첨단 도서관 데이터
        books = create_books(books_db)  # { '책 제목' : 객체 } 딕셔너리
        btn = self.sender()
        item = self.table_search.indexAt(btn.pos())
        # item을 기준으로 도서명을 가져옴
        title = self.table_search.item(item.row(), 1).text()
        print('대여 책 제목', title)

        print('빌리려는 책 :')
        print(books[title].title)

        print("로그인 확인 전")
        if self.now_user is None:
            QMessageBox.information(self, '알림', '로그인 먼저 해주세요')
        else:
            book_cnt = 5
            now_booklist = [self.now_user.book1, self.now_user.book2, self.now_user.book3, self.now_user.book4,
                            self.now_user.book5]
            now_booklist = sort_book(now_booklist)

            for now_book in now_booklist:
                if now_book != 'None':
                    book_cnt -= 1

            # 5권 이미 다 빌리면 back
            date = datetime.date.today()
            alert_str = '대여 가능 권수: ' + str(book_cnt) + ' / 5' + '\n대여일자: ' + str(date) + '\n반납예정일: ' + str(
                date + timedelta(days=14)) + '\n선택하신 책을 대여하시겠습니까?'
            buttonReply = QMessageBox.information(self, '알림', alert_str, QMessageBox.No | QMessageBox.Yes,
                                                  QMessageBox.Yes)
            # 기본 선택 = Yes
            if buttonReply == QMessageBox.Yes:
                print('대여 완료')
                QMessageBox.information(self, '알림', '대여가 완료되었습니다')
                books[title].rental_date = date
                books[title].return_date = date + timedelta(days=14)
                # books[book].return_date = datetime.date(2022, 12, 20)
                for i in range(5):
                    if now_booklist[i] == 'None':
                        now_booklist[i] = books[title].title
                        break
                self.now_user.book1 = now_booklist[0]
                self.now_user.book2 = now_booklist[1]
                self.now_user.book3 = now_booklist[2]
                self.now_user.book4 = now_booklist[3]
                self.now_user.book5 = now_booklist[4]
                print(now_booklist)
                print(self.now_user.book1, self.now_user.book2, self.now_user.book3, self.now_user.book4,
                      self.now_user.book5)
                self.table_rental.setRowCount(5)
                late = date - books[title].return_date
                late = late.days
                for i in range(5):
                    if now_booklist[i] == 'None':
                        break
                    else:
                        if books[title].return_date >= date:
                            late = ''
                        self.table_rental.setCellWidget(i, 0, QCheckBox())
                        self.table_rental.setItem(i, 1, QTableWidgetItem(books[title].library))
                        self.table_rental.setItem(i, 2, QTableWidgetItem(books[title].title))
                        self.table_rental.setItem(i, 3, QTableWidgetItem(books[title].writer))
                        self.table_rental.setItem(i, 4, QTableWidgetItem(books[title].publisher))
                        self.table_rental.setItem(i, 5, QTableWidgetItem(books[title].year_of_publication))
                        self.table_rental.setItem(i, 6, QTableWidgetItem(str(books[title].rental_date)))
                        self.table_rental.setItem(i, 7, QTableWidgetItem(str(books[title].return_date)))
                        self.table_rental.setItem(i, 8, QTableWidgetItem(late))

                self.table_rental.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

                btn.setText("대여중")
                btn.setDisabled(True)
                self.book_status_change(title, '대여중')

            else:
                print('대여 취소')
                # 취소 했을 때

    ### 도서의 상태를 변경하는 함수
    def book_status_change(self, title, status):
        books_db = books_database('lib_cd.csv')  # 첨단 도서관 데이터
        books = create_books(books_db)  # { '책 제목' : 객체 } 딕셔너리
        books[title].status = status  # 도서의 상태를 매개변수 status에 전달된 인자로 변경
        date = datetime.date.today()
        books[title].return_date = date + timedelta(days=14)
        save_book_data('lib_cd.csv', books)


    def idpw_lookup(self):
        self.stackedWidget.setCurrentIndex(7)

    def id_lookup(self):  # 아이디 찾기
        file = open('db_users.csv', 'r', newline='', encoding='utf-8-sig')
        line = csv.reader(file)
        done = False
        for i in line:
            if i[2] == self.name_id_lookup.text():
                if i[4] == self.tel_id_lookup.text():
                    if i[5] == self.combo_id.currentText():
                        if i[6] == self.answer_id_lookup.text():
                            done = True
            else:
                done = False
        if done == True:
            QMessageBox.information(self, "Information Title", f"아이디 : {i[0]}")
            self.stackedWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Information Title", "일치하는 회원정보가 없습니다.")
            self.stackedWidget.setCurrentIndex(1)

    def pw_lookup(self):  # 비밀번호 찾기
        file = open('db_users.csv', 'r', newline='', encoding='utf-8-sig')
        line = csv.reader(file)
        done = False
        for i in line:
            if i[0] == self.id_pw_lookup.text():
                if i[4] == self.tel_pw_lookup.text():
                    if i[5] == self.combo_pw.currentText():
                        if i[6] == self.answer_pw_lookup.text():
                            done = True
            else:
                done = False
        if done == True:
            QMessageBox.information(self, "Information Title", f"비밀번호 : {i[1]}")
            self.stackedWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Information Title", "일치하는 회원정보가 없습니다.")
            self.stackedWidget.setCurrentIndex(1)

    def all_insert1(self):
        if self.name_id_lookup.text() != "":
            if self.tel_id_lookup.text() != "":
                if self.answer_id_lookup.text() != "":
                    self.btn_id_lookup.setEnabled(True)

    def all_insert2(self):
        if self.id_pw_lookup.text() != "":
            if self.tel_pw_lookup.text() != "":
                if self.answer_pw_lookup.text() != "":
                    self.btn_pw_lookup.setEnabled(True)


def sort_book(book_list):
    for i in range(1, 5):
        if book_list[i - 1] == 'None':
            temp = book_list[i - 1]
            book_list[i - 1] = book_list[i]
            book_list[i] = temp
    return book_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
