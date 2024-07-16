---
layout: minimal
title: Linux 서버 사용자 추가 + SAMBA 설정
nav_order: 1
published_date: 2024-07-16
has_children: false
parent: Main
---

<a href='https://velog.io/@s2jin/add-user-linux-server-and-setting-samba'>[[velog post]]</a>

<h2 id="01-리눅스-서버-사용자-추가">01. 리눅스 서버 사용자 추가</h2>
<ol>
<li>사용자를 추가한다. (adduser 명령어의 경우 홈 디렉토리도 함께 생성한다.)</li>
</ol>
<pre><code class="language-bash">sudo adduser [USERNAME]</code></pre>
<ol start="2">
<li>사용자의 권한을 할당한다.</li>
</ol>
<pre><code class="language-bash">sudo vi /etc/group

## in /etc/group
sudo:x:user1,user2, ... # &lt;- 사용자 아이디 추가</code></pre>
<h2 id="02-samba-설정">02. SAMBA 설정</h2>
<p>다른 컴퓨터에서 파일 탐색기를 통해 해당 서버의 디렉토리에 접근하고자 할 때 필요한 설정이다.</p>
<ol>
<li>samba 사용자를 추가한다.</li>
</ol>
<pre><code class="language-bash">sudo smbpasswd -a [USERNAME]</code></pre>
<ol start="2">
<li>samba 설정 파일에 유저 정보를 추가한다.<ol>
<li><code>[NAME]</code>: samba 접속 시 사용할 경로, path의 별칭</li>
<li><code>path</code>: 해당 이름으로 접속했을 때 연결할 디렉토리</li>
<li><code>valid users</code>: 해당 경로에 접근할 수 있는 사용자 아이디</li>
</ol>
</li>
</ol>
<pre><code class="language-python">## in /etc/samba/smb.conf

#======================= Share Definitions =======================
...

[sujin_home]
   path = /home/sujin
   valid users = sujin
   read only = no
   writable = yes
   public = no
   browseable = yes
   printable = no
   create mask = 0750

[sujin_data1]
   path = /mnt/data1/sujin
   valid users = sujin
   read only = no
   writable = yes
   public = no
   browseable = yes
   printable = no
   create mask = 0750

[specific_dir_shared]
   path = /mnt/data1/sujin/project_A
   read only = no
   writable = yes
   public = yes
   browseable = yes
   printable = no
   create mask = 0750

...</code></pre>
<h3 id="1-samba-접속">1) samba 접속</h3>
<h4 id="macos">MacOS</h4>
<ol>
<li>Finder에서 <code>이동 &gt; 서버에 연결</code> 또는 <code>command + k</code>로 네트워크 서버 연결 창에 접속한다.</li>
<li><code>smb://[SERVER_IP or DNS]/[NAME]/[DIR_PATH]</code>와 같은 형식을 입력한다.<ol>
<li>(예) <code>smb://10.100.00.000/sujin_home/project_B/documents</code><br />→ <code>10.100.00.000</code> 서버의 <code>sujin_home(=/home/sujin)</code> 디렉토리 아래 <code>project_B/documents</code> 디렉토리를 연결  </li>
</ol>
</li>
</ol>
<h2 id="03-방문자-계정으로-접근하기">03. 방문자 계정으로 접근하기</h2>
<p>접근하고자 하는 서버의 디렉토리에 특정 사용자가 아닌 방문자 권한으로 접근하고자 할 때,  </p>
<ol>
<li>samba 설정 파일 <code>/etc/samba/smb.conf</code>의 <code>hosts allow</code>에 본인 기기의 ip를 추가해야 한다.</li>
</ol>
<h4 id="🅐-연구실-공유-디렉토리-접근을-위한-설정-예시">🅐 연구실 공유 디렉토리 접근을 위한 설정 예시</h4>
<input type="text" placeholder="password" id="inputString" onkeyup="if(window.event.keyCode==13){callApi('share_dir_server_example.md')}" style="margin:0px auto; display:block;text-align:center;"/>
<div id="resultContainer"></div>