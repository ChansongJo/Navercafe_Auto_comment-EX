from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import ttk
from listAll import *
import time
import pyperclip

# 로그인 창
win = Tk()
win.geometry('200x160')
win.title('Login')

# ID 입력창
idLabel = Label(win, text="ID")
idLabel.pack()
idEntry = Entry(win)
idEntry.pack()

# password 입력
pwLabel = Label(win, text="Password")
pwLabel.pack()
pwEntry = Entry(win, show='*')
pwEntry.pack()

# page 입력
pageLabel = Label(win, text="Pages")
pageLabel.pack()
pageEntry = Entry(win)
pageEntry.pack()


def login():
    # 네이버 로그인 열기
    driver = webdriver.Chrome()
    driver.get('https://nid.naver.com/nidlogin.login')

    # id, pw 입력할 곳을 찾습니다.
    tag_id = driver.find_element_by_name('id')
    tag_pw = driver.find_element_by_name('pw')
    tag_id.clear()
    time.sleep(1)

    # id 입력
    tag_id.click()
    pyperclip.copy(idEntry.get())
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # pw 입력
    tag_pw.click()
    pyperclip.copy(pwEntry.get())
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 로그인 버튼을 클릭합니다
    login_btn = driver.find_element_by_id('log.login')
    login_btn.click()

    # 슬립을 꼭 넣어줘야 한다.
    # 그렇지 않으면 로그인 끝나기도 전에 다음 명령어가 실행되어 제대로 작동하지 않는다.
    time.sleep(3)

    # 이중 for문 break를 위한 변수 할당
    # getExit = True
    # 전체게시판 게시글 페이지 1번부터 확인(1페이지에 15개씩 default는 총 195개까지)
    for j in range(1, int(pageEntry.get())+1):
        driver.get(
            f'https://cafe.naver.com/stockschart?iframe_url=/ArticleList.nhn%3Fsearch.clubid=11974608%26search.boardtype=L%26search.totalCount=151%26search.page={j}')
        time.sleep(2)
        # 본인 닉네임 확인
        getYournickname = driver.execute_script(
            'return document.querySelector("#gnb_name1").innerText')

        driver.switch_to_frame("cafe_main")
        # 페이지 게시글 수 확인. 16개 이상이면 답글이 포함되어 있는 것.
        getNumberofposts = driver.execute_script(
            'return document.querySelectorAll("#main-area > div:nth-child(6) > table > tbody > tr")')
        driver.switch_to_default_content()
# 첫글부터 클릭. 좋아요 눌러져있으면 넘어감
        for i in range(1, len(getNumberofposts)+1):
            # 본문은 iframe으로 이뤄져있다. 들어가기.
            driver.switch_to_frame("cafe_main")
            # 작성자 확인
            try:
                nickname = driver.execute_script(
                    f'return document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_name > div > table > tbody > tr > td > a").innerText')
            except:
                driver.refresh()
                time.sleep(1)
                continue
            # passlist와 비교
            if nickname not in passlist:
                # 게시판 확인
                board = driver.execute_script(
                    f'return document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_article > div.board-name > div > a").innerText')
                # 가입인사
                if board in MembershipBoard:
                    # 작성자 등급확인
                    getRating = driver.execute_script(
                        f'return document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_name > div > table > tbody > tr > td > span > img").src')
                    # 등급 1 확인
                    if getRating == "https://cafe.pstatic.net/levelicon/1/1_110.gif":
                        # 글 들어가기
                        driver.execute_script(
                            f'document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_article > div.board-list > div > a").click()')
                        time.sleep(2)
                        # 댓글창 닫기 옵션 확인
                        commentOption = driver.execute_script(
                            'return document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a")')
                        if commentOption == None:
                            driver.refresh()
                            time.sleep(1)
                            continue
                        # 댓글 작성자 node 리스트
                        setAuthorList = driver.find_elements_by_css_selector(
                            ".comment_nickname")
                        # 댓글을 일일이 확인하며 작성자 닉네임만 리스트로
                        alterAuthorList = []
                        for x in range(len(setAuthorList)):
                            alterAuthorList.append(
                                setAuthorList[x].get_attribute('innerText'))
                        # 본인 닉네임과 비교해서 중복 없을 시 댓글 달기
                        if getYournickname not in alterAuthorList:
                            driver.execute_script(
                                'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a").click()')
                            time.sleep(1)
                            driver.execute_script(
                                'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > div > div > div > div > ul > li.active > div > ul > li:nth-child(12) > button").click()')
                            time.sleep(1)
                            driver.execute_script(
                                'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.register_box > a").click()')
                            time.sleep(1)
                            driver.refresh()
                            time.sleep(1)
                            continue
                        # 중복 있으면 종료
                        else:
                            # driver.quit()
                            # break
                            driver.refresh()
                            time.sleep(1)
                            continue
                    else:
                        driver.refresh()
                        time.sleep(1)
                        continue
                # 매매일지 or 모바일 수익
                elif board in logBoard:
                    # 페이지 상단글부터 클릭
                    driver.execute_script(
                        f'document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_article > div.board-list > div > a").click()')
                    time.sleep(2)
                    commentOption = driver.execute_script(
                        'return document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a")')
                    if commentOption == None:
                        driver.refresh()
                        time.sleep(1)
                        continue
                    # 좋아요 값 확인
                    like = driver.execute_script(
                        "return document.querySelector('#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a').getAttribute('aria-pressed')")
                    # 좋아요가 눌러져있으면 종료.
                    if like == 'true':
                        # driver.quit()
                        # getExit = False
                        # break
                        driver.refresh()
                        time.sleep(1)
                        continue
                    else:
                        # 좋아요 클릭
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a > span").click()')
                        time.sleep(1)
                        # 스티커 박스 클릭
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a").click()')
                        time.sleep(1)
                        # 스티커 선택
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > div > div > div > div > ul > li.active > div > ul > li:nth-child(6) > button").click()')
                        time.sleep(1)
                        # 등록 클릭
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.register_box > a").click()')
                        time.sleep(1)
                        # 새로고침해서 밖으로 빠져나가기
                        driver.refresh()
                        time.sleep(1)
                        continue
                # 뉴스
                elif board in NewsBoard:
                    driver.execute_script(
                        f'document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_article > div.board-list > div > a").click()')
                    time.sleep(2)
                    commentOption = driver.execute_script(
                        'return document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a")')
                    if commentOption == None:
                        driver.refresh()
                        time.sleep(1)
                        continue
                    like = driver.execute_script(
                        "return document.querySelector('#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a').getAttribute('aria-pressed')")
                    if like == 'true':
                        driver.refresh()
                        time.sleep(1)
                        continue
                    else:
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a > span").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > div > div > div > div > ul > li.active > div > ul > li:nth-child(5) > button").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.register_box > a").click()')
                        time.sleep(1)
                        driver.refresh()
                        time.sleep(1)
                        continue
                    # 후기
                elif board in reviewBoard:
                    driver.execute_script(
                        f'document.querySelector("#main-area > div:nth-child(6) > table > tbody > tr:nth-child({i}) > td.td_article > div.board-list > div > a").click()')
                    time.sleep(2)
                    commentOption = driver.execute_script(
                        'return document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a")')
                    if commentOption == None:
                        driver.refresh()
                        time.sleep(1)
                        continue
                    like = driver.execute_script(
                        "return document.querySelector('#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a').getAttribute('aria-pressed')")
                    if like == 'true':
                        driver.refresh()
                        time.sleep(1)
                        continue
                    else:
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a > span").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > a").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.attach_box > div > div > div > div > ul > li.active > div > ul > li:nth-child(15) > button").click()')
                        time.sleep(1)
                        driver.execute_script(
                            'document.querySelector("#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.CommentWriter > div.comment_attach > div.register_box > a").click()')
                        time.sleep(1)
                        driver.refresh()
                        time.sleep(1)
                        continue
                # 지정된 게시판이 아닐 때
                else:
                    driver.refresh()
                    time.sleep(1)
                    continue
            else:
                driver.refresh()
                time.sleep(1)
                continue
        # if getExit == False:
        #     break
    driver.quit()


# login 버튼
loginButton = Button(win, text="Login", command=login)
loginButton.pack()

win.mainloop()
