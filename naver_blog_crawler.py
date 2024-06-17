#https://gist.github.com/jihobak/59a3493cb027114685caa4cbfc25781f
from typing import List, Dict

import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict


class NaverBlogCrawler:
    BASE_URL = 'https://section.blog.naver.com/Search/Post.naver?pageNo={page}&rangeType=ALL&orderBy=sim&keyword={keyword}'

    def __init__(self, keyword):
        self.keyword = keyword

    def search(self, keyword) -> List[str]:
        urls = []
        for page in range(1, 3):  # 예시로 페이지 1, 2만 검색
            try:
                url = self.BASE_URL.format(page=page, keyword=keyword)
                response = requests.get(url)
                response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
                soup = BeautifulSoup(response.text, 'html.parser')

                # 블로그 포스트 URL 추출 (예시, 실제로는 CSS 셀렉터 확인 필요)
                posts = soup.select('a.url')  # 여기를 실제 블로그 포스트 URL에 맞게 수정
                for post in posts:
                    urls.append(post['href'])
            except requests.RequestException as e:
                print(f"Error fetching URL {url}: {e}")
        return urls

    def get_blog_url(self, post):
        # 블로그 URL을 직접 받아와서 처리
        return post['href']

    def get_blog_title(self, post_soup):
        try:
            # 블로그 제목 추출 (예시, 실제로는 CSS 셀렉터 확인 필요)
            title = post_soup.select_one('h3.title').get_text(strip=True)
            return title
        except AttributeError:
            return "No Title Found"

    def get_blog_content(self, post_soup):
        try:
            # 블로그 내용 추출 (예시, 실제로는 CSS 셀렉터 확인 필요)
            content = post_soup.select_one('div.content').get_text(strip=True)
            return content
        except AttributeError:
            return "No Content Found"

    def get_all_information(self, url) -> Dict[str, str]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            post_soup = BeautifulSoup(response.text, 'html.parser')

            url = self.get_blog_url(post_soup)
            title = self.get_blog_title(post_soup)
            content = self.get_blog_content(post_soup)

            return {"title": title, "content": content, "url": url}
        except requests.RequestException as e:
            print(f"Error fetching blog post {url}: {e}")
            return {"title": "Error", "content": "Error", "url": url}

    def get_result(self, save_path: str):
        urls = self.search(self.keyword)

        data = []
        for url in urls:
            info = self.get_all_information(url)
            data.append(info)

        df = pd.DataFrame(data)
        df.to_excel(save_path, index=False)


# 사용 예제
crawler = NaverBlogCrawler(keyword='example_keyword')
crawler.get_result('result.xlsx')


