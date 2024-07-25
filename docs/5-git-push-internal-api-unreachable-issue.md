---
layout: minimal
title: push할 때, internal API unreachable 문제
nav_order: 5
published_date: 2024-07-24
has_children: false
parent: Main
---

<a href='https://velog.io/@s2jin/git-push-internal-api-unreachable-issue'>[[velog post]]</a>

오류
==


프로젝트를 push할 때 오류가 발생하였습니다.  
clone, pull은 정상 동작합니다. 


오류는 다음과 같은 상황에서 발생합니다.


### 1\. push 시도



```bash
$ git push

Username for 'http://git.nlp.wo.tc': s2jin
Password for 'http://s2jin@git.nlp.wo.tc':
Counting objects: 80, done.
Delta compression using up to 40 threads.
Compressing objects: 100% (78/78), done.
Writing objects: 100% (80/80), 332.53 MiB | 15.34 MiB/s, done.
Total 80 (delta 11), reused 0 (delta 0)
remote: GitLab: Failed to authorize your Git request: internal API unreachable
To http://git.nlp.wo.tc/group/subgroup/project.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'http://git.nlp.wo.tc/group/subgroup/project.git'
```

### 2\. gitlab configure 확인



```bash
$ gitlab-rake gitlab:check

Checking GitLab subtasks ...

Checking GitLab Shell ...

GitLab Shell: ... GitLab Shell version >= 9.3.0 ? ... OK (9.3.0)
Running /opt/gitlab/embedded/service/gitlab-shell/bin/check
Check GitLab API access: FAILED: Failed to connect to internal API
gitlab-shell self-check failed
  Try fixing it:
  Make sure GitLab is running;
  Check the gitlab-shell configuration file:
  sudo -u git -H editor /opt/gitlab/embedded/service/gitlab-shell/config.yml
  Please fix the error above and rerun the checks.

Checking GitLab Shell ... Finished

Checking Gitaly ...

...
```

→ /opt/gitlab/embedded/service/gitlab\-shell/bin/check를 실행했을 때 오류가 발생합니다. 


진행
==


### curl를 사용하여 차이점 확인



```bash
curl --header "Private-Token: oYezMsKoRkHqv7Q5HHCC" -v -k "http://10.100.54.160:9999/api/v4/application/settings"
➔ 오류
curl --header "Private-Token: oYezMsKoRkHqv7Q5HHCC" -v -k "http://localhost:9999/api/v4/application/settings"
➔ 정상동작
```

* Private\-Token
	+ 계정의 profile → setting → access tokens → scopes 설정을 모드 체크해서 personal access token 생성합니다.
	+ Feed token을 Private\-Token으로 사용합니다.


### gitlab.rb 수정



```rb
# 변경 전
gitlab_rails['internal_api_url'] = 'http://10.100.54.160:9999'
# 변경 후
gitlab_rails['internal_api_url'] = 'http://localhost:9999/'
```

결론
==



```bash
$ gitlab-rake gitlab:gitlab_shell:check --trace

...

GitLab Shell: ... GitLab Shell version >= 9.3.0 ? ... OK (9.3.0)
Running /opt/gitlab/embedded/service/gitlab-shell/bin/check
Check GitLab API access: OK
Redis available via internal API: OK

Access to /var/opt/gitlab/.ssh/authorized_keys: OK
gitlab-shell self-check successful

Checking GitLab Shell ... Finished
```


```bash
$ curl --header "Private-Token: oYezMsKoRkHqv7Q5HHCC" -v -k "http://git.nlp.wo.tc:9999/api/v4/application/settings"

...
HTTP/1.1 200 OK
...
```

파일 수정 후 정상 동작합니다. 


\+) 주소창에 <http://git.nlp.wo.tc/api/v4/application/settings> 입력해서 결과를 확인할 수 있습니다.

