# Navercafe_Auto_comment-EX v3.3

## 개요

네이버카페 댓글을 자동으로 달아주는 매크로 프로그램.  
특정 게시판의 글을 순회하며 댓글을 달고 좋아요를 누른다.

네이버카페에 글을 최신 글부터 하나씩 확인하며,  
내가 설정해둔 게시판이면 들어가서 댓글을 쓰고,  
아닌 경우 다음 글로 넘어간다.

좋아요가 있는 게시판은 좋아요로 읽었는지 확인하고,  
없는 게시판은 댓글 작성자 리스트를 만들어 본인 아이디와 비교한다.  
passlist가 있으며 그 아이디는 글을 읽지 않고 넘어간다.

## 릴리즈 노트

- v3.2  
  댓글 창을 닫아놓는 옵션이 있다.  
  거의 없지만 이런 설정일 때 오류로 프로그램이 멈추는 것을 확인했다.  
  댓글 창이 닫혀있을 때 넘어가게 코딩했다.

- v3.1  
  글이 많이 올라올 때 댓글 쓰고 새로고침할 때,  
  원래 글이 아래로 내려오는 경우가 생긴다.  
  이로인해 방금 쓴 글에 다시 들어가서 중복이라고 종료되는 경우가 생겼다.  
  그래서 페이지 입력창을 일단 임시로 만들었고,  
  중복이면 넘어가고 정해진 페이지까지 반복확인한다.

- v3  
  게시판별로 실행하는 불편을 없앴다.  
  실행하면 전체글보기에서 하나씩 읽어가며 게시판별로 맞게 작동한다.

## 기능

실행하면 로그인창이 실행되고 아이디, 비밀번호을 선택한 뒤,  
정해진 카페로 가서 첫 글부터 확인한다.  
중복을 체크해 댓글을 모두 작성하고 나면 브라우저 종료.

- 네이버카페 특정게시판에 댓글을 작성하는 것으로 제작되었다.
- 크롬으로 작동한다.

## 매커니즘

1. 로그인창 실행
2. 아이디, 비밀번호, 확인할 페이지수 입력 후 로그인 클릭
3. 네이버 로그인 페이지 접속
4. 아이디 로그인
5. 지정된 카페로 이동
6. 최신 글부터 확인
7. passlist에 있는 이름이면 다음 글로 넘어가기
8. passlist에 없는 이름이면 작성게시판 확인
9. 지정된 게시판이 아니면 다음 글로 넘어가기
10. 지정된 게시판이면 글로 들어가기
11. 댓글창 닫혀있으면 다음 글로 넘어가기
12. 댓글창 열려있으면 좋아요 확인
13. 좋아요 있는 게시판이면 클릭 여부 확인하여 중복 확인
14. 중복이 아닐 때 좋아요 클릭
15. 좋아요 없는 게시판일 때 댓글 작성자 리스트 확인
16. 본인 닉네임과 비교하여 중복 확인
17. 댓글 작성
18. 다음 게시글로 이동
19. 정해진 페이지까지 6~18번 반복
20. 정해진 페이지까지 확인하고 브라우저 종료

## 사용된 라이브러리

selenium  
pyperclip  
tkinter  
time
