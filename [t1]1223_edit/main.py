from library_book import *

books_db = books_database('cd_lib.csv')  # 첨단 도서관 데이터
books = create_books(books_db)  # {제목:Book 객체} 딕셔너리 생성

# 제목으로 객체 출력 테스트
test1 = books['왕의 남자[비디오녹화자료]. :']
print(test1.publisher)

# 1개의 옵션으로 조회 테스트
searchTest = search_book(books, '창비', '출판사')
print(searchTest)
for res in searchTest :
    print(res.title + " / 작가 - " + res.writer + " / 출판사 - " + res.publisher)

# 다중 옵션으로 조회 테스트 -- 미구현

# 파일 저장 테스트
save_book_data('save_testing.csv', books)