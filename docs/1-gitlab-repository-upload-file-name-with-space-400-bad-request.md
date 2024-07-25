---
layout: minimal
title: repository 업로드 파일 이름에 공백 포함 시 400 Bad Request 발생
nav_order: 1
published_date: 2024-07-25
has_children: false
parent: GitLab과 Apache2
grand_parent: Main
---

<a href='https://velog.io/@s2jin/gitlab-repository-upload-file-name-with-space-400-bad-request'>[[velog post]]</a>


문제 발생
=====


(21\.06\.14\) 


* repository에 업로드된 파일에 접근을 시도했을 때 400 Bad Request 오류가 발생하는 경우가 있음
* 같은 폴더 내에 파일 중에서도 오류가 발생하는 파일과 발생하지 않는 파일이 존재
* git clone으로 해당 repository를 다운로드받고 오류가 발생하는 파일을 확인했을 때 파일이 올바르게 열림 (서버와의 링크가 달라졌거나 파일이 깨진 문제는 아님)
* 400 에러는 url에 문제가 있거나 캐시에 문제가 있을 때 발생한다고 함


문제 원인
=====


* 파일 이름에 공백이 포함되어있을 때 웹 주소가 정상적으로 생성이 안되는 것을 확인함
* 이는 repository에 직접 업로드하는 경우에만 문제가 됨
* issue 작성 시 파일을 업로드하면 공백이 자동으로 '\_' 문자로 치환되어 문제가 발생하지 않음
* 다음은 정상적 파일에 접근할 수 있는 경우 log로, 접근 파일 주소와 동일한 주소가 log에 작성되는 것을 확인



```bash
## 정상 예시
## 접근 파일 주소: https://git.nlp.wo.tc/s2jin/project/blob/master/README.md
10.100.54.146 - - [14/Jun/2021:17:55:34 +0900] "GET /s2jin/project/blob/master/README.md?format=json&viewer=simple HTTP/1.1" 200 1517 "https://git.nlp.wo.tc/s2jin/project/blob/master/README.md" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
```

* 오류가 발생하는, 즉 공백이 포함되어있을 경우 연결 주소가 프로젝트까지만 생성되고 400이 리턴됨



```bash
## 오류 예시
## 접근 파일 주소: https://git.nlp.wo.tc/s2jin/project/blob/master/test%20file.txt
10.100.54.146 - - [14/Jun/2021:17:57:57 +0900] "GET /s2jin/project/blob/master/test%20file.txt HTTP/1.1" 400 254 "https://git.nlp.wo.tc/s2jin/project" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
```

해결
==


참고: [https://gitlab.com/gitlab\-org/gitlab/\-/issues/18213](https://gitlab.com/gitlab-org/gitlab/-/issues/18213)


* `/etc/apache2/sites-available/003-gitlab.conf`의 103행(현재 주석처리, 210615\) 을 102행으로 수정, Flag에서 NE를 제외함
* 참고 사이트에서 NE를 제거한 상황에서 branch 이름에 / 문자가 포함되어있을 때 문제가 발생한다는 언급이 있으나 확인 결과 다른 문제가 발생하지는 않음
