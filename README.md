# 실습 개요
* 제공된 [**쿠팡** 웹페이지](https://www.coupang.com/)의 테스트 케이스를 활용하여 스크립트를 작성하는 실습을 합니다.
* 각 페이지를 객체화하는 POM(Page Object Model) 디자인 패턴을 연습합니다.

## 테스트 케이스 요약
|ID|Testcase|Description|
|:-|:-|:-|
|CP-TC001|상품 검색 기능 테스트|웹 크롬으로 접속 후 검색 기능 정상 작동 여부 확인
|CP-TC002|장바구니 담기 기능 테스트|상품을 장바구니에 추가하여 수량 변경, 삭제, 최대 수량 제한, 로그아웃 후 유지 여부 등 전반적인 장바구니 기능이 정상 동작하는지 확인
|CP-TC003|상품 옵션 변경 및 반영 테스트|상품 클릭 수 페이지에서 옵션 변경, 장바구니 추가, 뒤로 가기 등 옵션 선택 사항이 정상적으로 반영, 유지되는지 확인
|CP-TC004|검색 필터 기능 테스트|쿠팡 검색필터(가격, 브랜드, 평점) 적용 및 초기화 기능 정상 동작 확인  
|CP-TC005|판매자 특가 페이지 테스트|판매자 특가 페이지에서 특가 상품 가격 비교, 할인율 정확성, 필터 기능이 정상적으로 동작하는지 확인
|CP-TC006|최근 본 상품 목록 테스트|최근 본 상품 목록에서 삭제 버튼 및 새로고침(F5) 이후 목록 유지되는지 확인

\* 테스트 케이스 제공자 : 엘리스 SW QA트랙 1기 **윤찬유**님

## 기술스택
- Python

## 테스트 도구
- Pytest
- Selenium

\* 파랑색 글자를 클릭하시면 관련 페이지로 이동하실 수 있습니다.