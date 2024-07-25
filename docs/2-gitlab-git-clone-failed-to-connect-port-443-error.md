---
layout: minimal
title: git clone 시 Failed to connect to port 443 에러 발생
nav_order: 2
published_date: 2024-07-25
has_children: false
parent: GitHub와 Apache2
grand_parent: Main
---

<a href='https://velog.io/@s2jin/gitlab-git-clone-failed-to-connect-port-443-error'>[[velog post]]</a>


문제 발생
=====


(21\.04\.) 


* 내부망 서버 A에서 git clone 수행 시 connection refused 오류가 발생함



```
fatal: unable to access 'https://git.nlp.wo.tc/group/subgroup/project.git/': Failed to connect to git.nlp.wo.tc port 443: 연결이 거부됨
```
문제 원인
=====


* github 주소로 clone을 할 경우 오류 없이 다운로드 가능함
* 내부망 서버 A에서 깃랩 서버로 ssh 연결 가능
* gitlab의 git clone이 가능한 서버(동일 내부망 내 서버 B, C)에서 git.nlp.wo.tc로 ping이 동작함
* 서버 A에서 git.nlp.wo.tc로의 ping은 동작하나 외부 DNS로는 동작하지 않음
	+ 외부 DNS의 경우 학교에서 제공받은 DNS
	+ ➔ dns 검색에 문제가 생겨 검색이 안 되는 것으로 추측됨


해결
==


* 서버 A의 `/etc/netplan/50-cloud-init.yaml`에서 13행 addresses에 `168.126.63.1` 대신 `8.8.8.8`, `203.246.1.3`으로 수정 (수정 후 `sudo netplan apply`로 수정 내용 반영 필요)
	+ 학교 내부망 ip 수정으로, nameserver 주소가 168\.126\.63\.1에서 203\.246\.1\.3으로 수정됨
* gitlab 주소의 git clone이 가능한 것을 확인
