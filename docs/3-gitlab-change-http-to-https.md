---
layout: minimal
title: http 통신을 https 통신으로 변경
nav_order: 3
published_date: 2024-07-25
has_children: false
parent: GitLab과 Apache2
grand_parent: Main
---

<a href='https://velog.io/@s2jin/gitlab-change-http-to-https'>[[velog post]]</a>


개요
==


현재 <http://git.nlp.wo.tc> 로만 깃랩에 접근 가능하였다.  
이 경우 보안이 약하며, Safari에서는 https 접근을 강제해 gitlab 사용이 불가능하다는 문제점이 있다. 


https의 사용을 위해 ssl 인증서를 설정한다. 


진행
==


### SSL 인증서 설정


`/etc/gitlab/ssl`에 ssl 인증서를 위치시킨다. 


\+) 이 경로는 나중에 apache의 gitlab config에 명시해야한다. 



```rb
## /etc/apache2/site-available/gitlab.conf
## <VirtualHost *:443> 아래에

SSLCertificateFile "/etc/gitlab/ssl/gitlab.crt"
SSLCertificateKeyFile "/etc/gitlab/ssl/gitlab.key"
```

letsencrypt을 통해 무료 ssl 인증서를 발급받으려 했으나 같은 도메인에 대해서 신청이 일주일 5번으로 제한되어 실패하였다.  
openssl로 자체 서명 인증서를 생성하여 적용시켜 보았으나 크롬에서 '타사의 인증을 받지않은 인증서'라는 경고와 함께 적용이 되지않은 문제가 계속되었다. 


그래서 현재 gitlab의 도메인명이 이전 서버에서 사용하던 도메인명과 동일하기 때문에 우선 이전 modi 서버에서 동작한 인증서를 가져왔고, 적용되는 것을 확인하였다. 


다만, "주의요함"이 표시되기 때문에 다시 인증서를 준비하여 설정해야한다. 


### gitlab.rb 파일 수정



```rb
external_url = 'http://git.nlp.wo.tc'
gitlab_rails['internal_api_url'] ='http://localhost:9999'

letsencrypt['enable'] = false
```

### gitlab.conf 파일 수정


* 파일 위치: `/etc/apache2/site-available/gitlab.conf`



```rb
<VirtualHost *:80>

    ...

    ProxyPass http://localhost:9999/ Keepalive=on
    ProxyPassReverse http://localhost:9999/

    ...

    RewriteRule .* http://localhost:9999%{REQUEST_URI} [P,QSA,NE]

    ...

</VirtualHost>

<VirtualHost *:443>

    SSLengine On
    SSLCertificateFile "/etc/gitlab/ssl/gitlabe.crt"
    SSLCertificateKeyFile "/etc/gitlab/ssl/gitlab.key"

    SSLProxyEngine on
    SSLProxyVerify none
    SSLProxyCheckPeerCN on
    SSLProxyCheckPeerName on
    SSLProxyCheckPeerExpire on

    ...

    ProxyPass http://localhost:9999/ Keepalive=on
    ProxyPassReverse http://localhost:9999/

    ...

    RewriteRule .* http://localhost:9999%{REQUEST_URI} [P,QSA,NE]

    ...

</VirtualHost>
```

### 추가 설정


* 포트 열기



```bash
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

* apache2 mode 추가



```bash
a2enmod ssl
```

결론
==


<http://git.nlp.wo.tc> 와 <https://git.nlp.wo.tc> 로 gitlab에 접근 가능하다.  
Safari에서도 접근할 수 있는 것을 확인하였다. 


하지만 `external_url`이 http이기 때문에 git clone에 사용되는 주소가 http이다.  
또, chrome과 internet explorer에서 확인해 본 결과 접근을 https로 하더라도 http로 바뀌었다. 


git clone의 주소(external\_url)를 https로 바꾸고 https로 주소가 유지되게 해야한다. 


추가) git clone 주소 수정
===================


* external\_url과 listen\_https 수정하여 git clone의 주소도 변경하였다.



```rb
## 변경 전
external_url 'http://git.nlp.wo.tc'
...
# nginx['listen_https'] = false

## 변경 후
external_url 'https://git.nlp.wo.tc'
...
nginx['listen_https'] = false

```
