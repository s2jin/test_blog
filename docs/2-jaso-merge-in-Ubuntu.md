---
layout: minimal
title: Ubuntu에서 자소가 분리된 파일 복구하기
nav_order: 2
published_date: 2024-07-16
has_children: false
parent: Main
---

<a href='https://velog.io/@s2jin/jaso-merge-in-Ubuntu'>[[velog post]]</a>

<ul>
<li><p>MacOS에서 저장된 한글 파일들의 자모가 리눅스에서 따로 떨어져서 나오는 현상이 발생할 수 있습니다.</p>
</li>
<li><p>이는 유니코드 포맷(NFD와 NFC의 차이)이 달라서 생기는 문제입니다.</p>
</li>
<li><p>다음 코드를 통해 파일명을 복구할 수 있습니다.</p>
<pre><code class="language-bash">convmv -r --nfc --nosmart -f UTF-8 -t UTF-8 --notest [DIRECTORY]</code></pre>
</li>
<li><p><code>DIRECTORY</code> 부분을 파일명을 복구하고 싶은 디렉토리 경로로 지정해줍니다.</p>
</li>
</ul>