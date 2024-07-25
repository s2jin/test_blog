---
layout: minimal
title: 업로드한 파일에 접근 시 404 에러 발생 문제
nav_order: 9
published_date: 2024-07-24
has_children: false
parent: GitLab과 Apache2
grand_parent: Main
---

<a href='https://velog.io/@s2jin/gitlab-uploaded-file-404-error-issue'>[[velog post]]</a>


개요
==


프로젝트에 접근 및 이슈 생성 후 파일 또는 이미지를 "업로드"하였을 때, 해당 파일에 접근 및 다운로드가 불가한 문제가 있었습니다.  
오류 상황에서 이미지는 깨져서 보이지않고, 파일 혹은 이미지를 선택하면 다음과 같은 오류 페이지가 나타납니다. 




| gitlab 오류 페이지 |
| --- |
|  |


같은 그룹 내 다른 프로젝트에서는 파일에 정상적으로 접근 가능합니다. 


진행
==


업로드 파일에 접근 시 "The page could not be found or **you don’t have permission to view it**" 라고 나오는 것을 볼 때 권한 문제를 의심합니다.  
다른 프로젝트의 설정과 비교해 본 결과 git storage에 대한 권한이 설정이 없었고 이 때문에 해당 오류가 발생한 것으로 보입니다. 


아래 그림의 노란 박스의 부분을 활성화시켜 주었습니다. 




| Project에서 `Settings > General > Visibility,project features, permissions` |
| --- |
|  |


결론
==


업로드 파일에 정상적으로 접근할 수 있는 것을 확인하였습니다.

