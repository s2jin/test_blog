import feedparser
import git
import os
import re
from datetime import datetime


def main():
    # 벨로그 RSS 피드 URL
    # example : rss_url = 'https://api.velog.io/rss/@rimgosu'
    rss_url = 'https://api.velog.io/rss/@s2jin'

    # 레포지토리 로드
    repo_path = '.'
    repo = git.Repo(repo_path)


    # 'velog-posts' 폴더 경로
    posts_dir = os.path.join(repo_path, 'docs')
    if os.path.exists(posts_dir):
#         [os.remove(os.path.join(x[0],y)) for x in os.walk(posts_dir) for y in x[-1]]
#         os.rmdir(posts_dir)
        git.rmtree(posts_dir)
    os.makedirs(posts_dir)


    # RSS 피드 파싱
    feed = feedparser.parse(rss_url)
    entries = sorted(feed.entries, key=lambda x:x.published)


    # 각 글을 파일로 저장하고 커밋
    for ientry, entry in enumerate(entries):

        filename, content = refine(entry, order=ientry+1)
        filename = os.path.join(posts_dir, filename)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)  # 글 내용을 파일에 작성

            # 깃허브 커밋
            repo.git.add(filename)
            repo.git.commit('-m', f'Add post: {entry.title}')

    # 변경 사항을 깃허브에 푸시
    repo.git.push()


def refine(data, order=1):

    content = data.description

    replace_map = { 
            'toc':'<br/>\n<details markdown="block">\n  <summary>\n    Table of contents\n  </summary>\n  {: .text-gamma }\n- TOC\n{:toc}\n</details>\n<br/>',
            'lab_post_api':'<input type="text" placeholder="password" id="inputString" onkeyup="if(window.event.keyCode==13){{callApi(\'{}.md\')}}" style="margin:0px auto; display:block;text-align:center;"/>\n<div id="resultContainer"></div>',
            }

    ## TOC replace
    targets = re.findall('<!--\[\[TOC\]\]-->',content)
    for target in targets:
        content = content.replace(target, replace_map['toc'])

    ## lab_post_api replace
    targets = re.findall('<!--\[\[lab_post_api:[^\]]*\]\]-->', content)
    values = [re.findall(':(.*)\]\]',d)[0] for d in targets]
    for t,v in zip(targets, values):
        content = content.replace(t, replace_map['lab_post_api'].format(v))

    date = datetime.strptime(data.published, '%a, %d %b %Y %H:%M:%S GMT')
    date = date.strftime('%Y-%m-%d')

    header_map = {
            'layout': 'minimal',
            'title': data.title,
            'nav_order': order,
            'published_date': date,
            #'last_modified_date': '',
            'has_children': 'false',
            'parent': 'Main',
            #'grand_parent': 'Main',
            }

    header = ['---']
    for k,v in header_map.items():
        header.append( f"{k}: {v}" )
    header.append('---')
    header = '\n'.join(header)

    link = data.link
    
    content = f"{header}\n\n<a href='{link}'>[[velog post]]</a>\n\n{content}"

    filename = link.strip().split('/')[-1]
    filename = f"{order}-{filename}.md"

    return filename, content
    


main()
