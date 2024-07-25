---
layout: minimal
title: GitLab과 Apache2 연동 및 Virtual host 설정
nav_order: 7
published_date: 2024-07-24
has_children: false
parent: GitLab과 Apache2
grand_parent: Main
---

<a href='https://velog.io/@s2jin/gitlab-apache2-integration-and-virtual-host-setup'>[[velog post]]</a>


개요
==


gitlab은 웹 서버로 내장된 nginx을 사용합니다. 이를 apache2로 바꾸고자 합니다.  
apache2로 바꾼 뒤 가상호스트를 설정하여 지정된 도메인(git.nlp.wo.tc)으로 접근 가능하게 하는 것을 목표로 합니다.  
하나의 서버에서 도메인에 따라 다른 웹 서비스를 제공하기 위해 이 작업을 진행하였습니다. 


진행
==


apache 설정
---------


#### 1\. gitlab.conf 설정


apache가 gitlab에 대한 설정을 갖도록 gitlab.conf를 작성합니다.


* 파일 위치: `/etc/apache2/sites-available/gitlab.conf`
* 수정해야하는 부분
	+ `ServerName [DOMAIN_NAME]`: 서비스할 도메인, 주 도메인, DNS 연결되어있어야함
	+ `ProxyPassReverse [TARGET_ADDR]`: Target address로 요청 넘김, 실제 gitlab이 동작하는 주소, TARGET\_ADDER \= `http://IP:PORT`
	+ `RewriteRule .* [TARGET_ADDR]%{REQUEST_URI} [P,QSA,NE]`: 입력받은 주소를 주어진 형식으로 변경
	+ `DocumentRoot [SOURCE_FILE_PATH]`: 실제 소스파일이 있는 경로
		- gitlab의 실행 파일 경로: `/opt/gitlab/embedded/service/gitlab-rails/public`



```
<VirtualHost *:80>
    ServerName git.nlp.wo.tc
    ServerSignature Off

    ProxyPreserveHost On
    AllowEncodedSlashes NoDecode

    <Location />
        Order deny,allow
        Allow from all
        # New authorization commands for apache 2.4 and up
        # http://httpd.apache.org/docs/2.4/upgrading.html#access
        Require all granted

        #Allow forwarding to gitlab-workhorse
        #ProxyPassReverse http://127.0.0.1:9999
        ProxyPassReverse http://10.100.54.160:9999
    </Location>

    # Apache equivalent of nginx try files
    RewriteEngine on
    RewriteCond %{DOCUMENT_ROOT}/%{REQUEST_FILENAME} !-f [OR]
    RewriteCond %{REQUEST_URI} ^/uploads/.*
    RewriteRule .* http://127.0.0.1:9999%{REQUEST_URI} [P,QSA,NE]

    DocumentRoot /opt/gitlab/embedded/service/gitlab-rails/public
    # Error Page
    ErrorDocument 404 /404.html

    # Log
    LogFormat "%{X-Forwarded-For}i %l %u %t \"%r\" %>s %b" common_forwarded
    ErrorLog /var/log/apache2/GITLAB_URL_error.log
    CustomLog /var/log/apache2/GITLAB_URL_forwarded.log common_forwarded
    CustomLog /var/log/apache2/GITLAB_URL_access.log combined env=!dontlog
    CustomLog /var/log/apache2/GITLAB_URL.log combined
</VirtualHost>

```
#### 2\. a2ensit



```bash
$ sudo a2ensite gitlab.conf                ## ensite 목록에 gitlab.conf 추가
## 결과
Enabling site gitlab.
To activate the new configuration, you need to run:
    systemctl reload apache2

$ sudo service apache2 restart             ## apache 재시작
$ sudo systemctl status apache2.service    ## apache 실행 상태 확인
```

\+) a2ensite로 추가한 걸 다시 제외시키고 싶을 때



```bash
$ sudo a2dissite [NAME]
```

#### 3\. a2enmod



```bash
$ sudo a2enmode proxy_http # 안하면 500 에러 발생
$ sudo a2enmode proxy_ajp
```

\+) issue: apache2 restart 시 오류 발생



```
Job for apache2.service failed because the control process exited with error code.
See "systemctl status apache2.service" and "journalctl -xe" for details.
```
➔ gitlab.conf에 올바르지않은 문구가 있는 상태, gitlab.conf의 오타를 수정해주니 동작하였습니다.


gitlab 설정
---------


* gitlab 설정 파일 위치: `/etc/gitlab/gitlab.rb`
* 설정 파일 수정 후 반영



```bash
$ sudo gitlab-ctl reconfigure
$ sudo gitlab-ctl restart
```

#### 1\. nginx 비활성화



```rb
# 변경 전
nginx['enable'] = true
# 변경 후
nignx['enable'] = false
```

#### 2\. external\_users 수정



```rb
# 변경 전
web_server['external_users'] = []
# 변경 후
web_server['external_users'] = ['www-data']
```

#### 3\. gitlab\_workhorse 수정



```rb
# 변경 전
gitlab_workhorse['listen_network'] = "unix"
gitlab_workhorse['listen_addr'] = "/var/opt/gitlab/gitlab-workhorse/socket"
# 변경 후
gitlab_workhorse['listen_network'] = "tcp"
gitlab_workhorse['listen_addr'] = "127.0.0.1:9999"
```

결론
==


기존에는 10\.100\.54\.160으로 접속 시 홈페이지가 제공되었고,  
gitlab에 접근하기 위해서는 10\.100\.54\.169:9999로 접근해야했습니다. 


위의 수정을 끝내고 나면 지정된 도메인을 입력했을 때 gitlab에 접근할 수 있으며,  
10\.100\.54\.160:9999로는 접근할 수 없습니다.

