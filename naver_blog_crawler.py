#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 블로그 크롤링 스크립트
Playwright를 사용하여 네이버 블로그에서 제목, 작성자, 본문만 정확히 추출
"""

import asyncio
import re
import json
import aiohttp
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import argparse
from urllib.parse import urljoin, urlparse


class NaverBlogCrawler:
    def __init__(self):
        self.selectors = {
            'title': 'h1, h2, h3, .title, [class*="title"], .se-title, .blog-title',  # 제목
            'author': '.blog_author, .author, [class*="author"]',  # 작성자
            'content': '.se-main-container, .post-content, .content, article, main, .se-component, #postViewArea',  # 본문
            'fallback_title': 'title',  # 페이지 제목으로 대체
            'fallback_content': 'p, div[class*="content"], div[class*="post"]'  # 대체 본문 셀렉터
        }
    
    async def extract_content(self, page, url):
        """페이지에서 콘텐츠 추출"""
        try:
            # 페이지 로딩 대기
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # iframe 확인 및 처리
            iframe = await page.query_selector('iframe#mainFrame')
            if iframe:
                print("📱 iframe 감지됨, iframe 내용으로 전환")
                frame = await iframe.content_frame()
                if frame:
                    page = frame  # iframe 내용을 사용
                    await frame.wait_for_load_state('networkidle', timeout=5000)
            
            # 페이지 전체 텍스트 확인 (디버깅)
            all_text = await page.inner_text('body')
            print(f"🔍 전체 텍스트 길이: {len(all_text)}자")
            if len(all_text) > 200:
                print(f"🔍 첫 200자: {all_text[:200]}...")
            else:
                print(f"🔍 전체 텍스트: {all_text}")
            
            # 제목 추출
            title = await self._extract_title(page)
            print(f"📝 추출된 제목: {title}")
            
            # 작성자 추출  
            author = await self._extract_author(page)
            print(f"👤 추출된 작성자: {author}")
            
            # 블로그 ID 생성
            blog_id = author if author != "작성자 없음" else "unknown_blog"
            
            # 텍스트와 이미지가 혼합된 콘텐츠 추출 (원본 순서 유지)
            content = await self._extract_mixed_content(page, blog_id)
            print(f"📄 혼합 콘텐츠 추출 완료")
            
            # 이미지 개수 계산 (이미 다운로드된 이미지들)
            images_dir = Path(f"images/{blog_id}")
            if images_dir.exists():
                image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.JPG")) + list(images_dir.glob("*.png"))
                image_count = len(image_files)
            else:
                image_count = 0
            
            # 작성일 추출 (페이지에서 날짜 패턴 찾기)
            published_date = await self._extract_date(page)
            
            return {
                'url': url,
                'title': title,
                'author': author,
                'content': content,
                'published_date': published_date,
                'scraped_at': datetime.now().isoformat(),
                'content_length': len(content) if content else 0,
                'word_count': len(content.split()) if content else 0,
                'image_count': image_count
            }
            
        except Exception as e:
            print(f"콘텐츠 추출 오류: {e}")
            return None
    
    async def _extract_title(self, page):
        """제목 추출"""
        try:
            # 첫 번째 시도: 모든 제목 셀렉터들 순차 시도
            title_selectors = self.selectors['title'].split(', ')
            for selector in title_selectors:
                title_element = await page.query_selector(selector.strip())
                if title_element:
                    title = await title_element.inner_text()
                    if title.strip() and len(title.strip()) > 2:
                        return title.strip()
            
            # 두 번째 시도: 페이지 제목에서 추출
            page_title = await page.title()
            if page_title:
                # "제목 : 네이버 블로그" 형태에서 제목 부분만 추출
                if ' : ' in page_title:
                    clean_title = page_title.split(' : ')[0].strip()
                elif ' - ' in page_title:
                    clean_title = page_title.split(' - ')[0].strip()
                else:
                    clean_title = page_title.strip()
                
                if clean_title and '네이버 블로그' not in clean_title:
                    return clean_title
            
            # 세 번째 시도: 첫 번째 텍스트 블록에서 제목 찾기
            all_text = await page.inner_text('body')
            lines = all_text.split('\n')
            for line in lines[:20]:  # 첫 20줄에서 제목 찾기
                line = line.strip()
                if line and len(line) > 5 and len(line) < 100:
                    if 'CCTV' in line or '설치' in line or '후기' in line:
                        return line
                        
            return "제목 없음"
            
        except Exception as e:
            print(f"제목 추출 오류: {e}")
            return "제목 추출 실패"
    
    async def _extract_author(self, page):
        """작성자 추출"""
        try:
            author_element = await page.query_selector(self.selectors['author'])
            if author_element:
                author = await author_element.inner_text()
                return author.strip() if author else "작성자 없음"
            
            # 대체 방법: URL에서 블로거 ID 추출
            url = page.url
            if 'blog.naver.com' in url:
                # blog.naver.com/블로거ID/글번호 형태에서 블로거ID 추출
                match = re.search(r'blog\.naver\.com/([^/]+)/', url)
                if match:
                    return match.group(1)
            
            return "작성자 없음"
            
        except Exception as e:
            print(f"작성자 추출 오류: {e}")
            return "작성자 추출 실패"
    
    async def _extract_mixed_content(self, page, blog_id):
        """텍스트와 이미지가 혼합된 원본 순서 그대로 콘텐츠 추출"""
        try:
            # 본문 컨테이너 찾기
            content_selectors = [
                '.se-main-container', 
                '.post-content', 
                '.content', 
                'article', 
                'main', 
                '.se-component', 
                '#postViewArea'
            ]
            
            content_container = None
            for selector in content_selectors:
                content_container = await page.query_selector(selector)
                if content_container:
                    print(f"📍 본문 컨테이너 발견: {selector}")
                    break
            
            if not content_container:
                # fallback: body 전체 사용
                content_container = await page.query_selector('body')
                print("📍 fallback: body 전체 사용")
            
            # DOM 순서대로 모든 요소 탐색
            mixed_content = []
            await self._traverse_elements(content_container, mixed_content, blog_id, page)
            
            if not mixed_content:
                return "본문 추출 실패"
            
            # 혼합 콘텐츠를 마크다운으로 변환
            markdown_content = self._convert_to_markdown(mixed_content)
            return markdown_content
            
        except Exception as e:
            print(f"혼합 콘텐츠 추출 오류: {e}")
            return "본문 추출 실패"

    async def _traverse_elements(self, container, mixed_content, blog_id, page):
        """DOM 트리를 순서대로 탐색하며 텍스트와 이미지 추출"""
        try:
            # 컨테이너 내의 모든 직속 자식 요소들을 순서대로 처리
            children = await container.query_selector_all('> *')
            
            for child in children:
                tag_name = await child.evaluate('element => element.tagName.toLowerCase()')
                
                # 이미지 처리
                if tag_name == 'img':
                    await self._process_image_element(child, mixed_content, blog_id)
                
                # 이미지를 포함한 div나 다른 컨테이너 처리
                elif tag_name in ['div', 'span', 'p', 'section']:
                    # 이 요소 안에 이미지가 있는지 확인
                    img_in_element = await child.query_selector('img')
                    if img_in_element:
                        # 이미지가 있으면 이미지 처리
                        await self._process_image_element(img_in_element, mixed_content, blog_id)
                    else:
                        # 이미지가 없으면 텍스트 처리
                        await self._process_text_element(child, mixed_content)
                
                # 텍스트 요소 처리
                elif tag_name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span']:
                    await self._process_text_element(child, mixed_content)
                
                # 복합 요소는 재귀적으로 탐색
                else:
                    await self._traverse_elements(child, mixed_content, blog_id, page)
            
        except Exception as e:
            print(f"요소 탐색 오류: {e}")

    async def _process_image_element(self, img_element, mixed_content, blog_id):
        """이미지 요소 처리"""
        try:
            src = await img_element.get_attribute('src')
            alt = await img_element.get_attribute('alt') or "이미지"
            
            if src and ('postfiles.pstatic.net' in src or 'blogfiles.naver.net' in src):
                # 이미지 다운로드
                images_dir = Path(f"images/{blog_id}")
                images_dir.mkdir(parents=True, exist_ok=True)
                
                image_count = len([item for item in mixed_content if item['type'] == 'image']) + 1
                filename = await self._download_image(src, images_dir, f"{blog_id}_image_{image_count}")
                
                if filename:
                    mixed_content.append({
                        'type': 'image',
                        'src': src,
                        'alt': alt,
                        'local_path': f"images/{blog_id}/{filename}",
                        'filename': filename
                    })
                    print(f"📷 이미지 순서대로 처리 완료: {filename}")
                    
        except Exception as e:
            print(f"이미지 요소 처리 오류: {e}")

    async def _process_text_element(self, element, mixed_content):
        """텍스트 요소 처리"""
        try:
            text = await element.inner_text()
            if text and text.strip():
                cleaned_text = self._clean_text_segment(text.strip())
                if cleaned_text and len(cleaned_text) > 5:
                    mixed_content.append({
                        'type': 'text',
                        'content': cleaned_text
                    })
                    
        except Exception as e:
            print(f"텍스트 요소 처리 오류: {e}")

    def _clean_text_segment(self, text):
        """개별 텍스트 세그먼트 정리"""
        # 네이버 블로그 UI 요소 필터링
        skip_patterns = [
            r'^공감\s*\d*$',
            r'^댓글\s*\d*$',
            r'^스크랩$',
            r'^이웃추가$',
            r'^구독$',
            r'^좋아요$',
            r'^이전글$',
            r'^다음글$',
            r'^목록$',
            r'^블로그$',
            r'^NAVER$',
            r'^블로그 검색$',
            r'^메뉴 바로가기$',
            r'^본문 바로가기$',
        ]
        
        for pattern in skip_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return None
        
        return text

    def _convert_to_markdown(self, mixed_content):
        """혼합 콘텐츠를 마크다운으로 변환"""
        markdown_parts = []
        
        for item in mixed_content:
            if item['type'] == 'text':
                markdown_parts.append(item['content'])
                markdown_parts.append('')  # 빈 줄 추가
            elif item['type'] == 'image':
                markdown_parts.append(f"![{item['alt']}]({item['local_path']})")
                markdown_parts.append('')  # 빈 줄 추가
        
        return '\n'.join(markdown_parts).strip()
    
    async def _extract_date(self, page):
        """작성일 추출"""
        try:
            # 페이지 전체 텍스트에서 날짜 패턴 찾기
            page_content = await page.content()
            
            # 한국어 날짜 패턴들
            date_patterns = [
                r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일',
                r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})',
                r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, page_content)
                if matches:
                    # 첫 번째 매치를 사용 (보통 작성일)
                    year, month, day = matches[0]
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            return datetime.now().strftime('%Y-%m-%d')
            
        except Exception as e:
            print(f"날짜 추출 오류: {e}")
            return datetime.now().strftime('%Y-%m-%d')
    
    def _clean_content(self, content):
        """본문 텍스트 정리"""
        if not content:
            return ""
        
        # 불필요한 공백 제거
        content = re.sub(r'\n\s*\n', '\n\n', content)  # 연속된 빈 줄을 두 줄로
        content = re.sub(r'[ \t]+', ' ', content)      # 연속된 공백을 하나로
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # 빈 줄은 유지
            if not line:
                cleaned_lines.append('')
                continue
            
            # 네이버 블로그 UI 요소 제거
            skip_patterns = [
                r'^공감\s*\d*$',
                r'^댓글\s*\d*$',
                r'^스크랩$',
                r'^이웃추가$',
                r'^구독$',
                r'^좋아요$',
                r'^이전글$',
                r'^다음글$',
                r'^목록$',
                r'^블로그$',
                r'^카테고리$',
                r'^태그$',
                r'^방문자$',
                r'네이버.*블로그',
                r'^Copyright',
                r'^\[.*\]$',  # 대괄호로 감싸진 텍스트
            ]
            
            should_skip = False
            for pattern in skip_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    should_skip = True
                    break
            
            if not should_skip:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()



    async def _download_image(self, url, images_dir, base_filename):
        """이미지 파일 다운로드"""
        try:
            # URL에서 파일 확장자 추출
            parsed_url = urlparse(url)
            path = parsed_url.path
            ext = os.path.splitext(path)[1] or '.jpg'
            
            filename = f"{base_filename}{ext}"
            filepath = images_dir / filename
            
            # aiohttp로 이미지 다운로드
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        filepath.write_bytes(content)
                        return filename
            
            return None
            
        except Exception as e:
            print(f"이미지 다운로드 실패 {url}: {e}")
            return None
    
    async def crawl_url(self, url, output_format='markdown'):
        """단일 URL 크롤링"""
        async with async_playwright() as p:
            # 브라우저 시작 (헤드리스 모드)
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            try:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = await context.new_page()
                
                print(f"크롤링 시작: {url}")
                
                # 페이지 로드
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # 콘텐츠 추출
                result = await self.extract_content(page, url)
                
                if result:
                    print(f"✅ 크롤링 완료: {result['title']}")
                    
                    # 파일로 저장
                    if output_format == 'markdown':
                        await self._save_as_markdown(result)
                    elif output_format == 'json':
                        await self._save_as_json(result)
                    
                    return result
                else:
                    print("❌ 크롤링 실패")
                    return None
                    
            finally:
                await browser.close()
    
    async def _save_as_markdown(self, data):
        """마크다운 파일로 저장"""
        filename = f"naver_blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        markdown_content = f"""---
title: "{data['title']}"
author: "{data['author']}"
url: "{data['url']}"
published_date: "{data['published_date']}"
scraped_at: "{data['scraped_at']}"
content_length: {data['content_length']}
word_count: {data['word_count']}
image_count: {data.get('image_count', 0)}
---

# {data['title']}

**작성자**: {data['author']}  
**작성일**: {data['published_date']}  
**출처**: {data['url']}
**이미지 수**: {data.get('image_count', 0)}개

---

{data['content']}
"""
        
        Path(filename).write_text(markdown_content, encoding='utf-8')
        print(f"📄 마크다운 파일 저장: {filename}")
    
    async def _save_as_json(self, data):
        """JSON 파일로 저장"""
        filename = f"naver_blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        Path(filename).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), 
            encoding='utf-8'
        )
        print(f"📄 JSON 파일 저장: {filename}")


async def main():
    parser = argparse.ArgumentParser(description='네이버 블로그 크롤러')
    parser.add_argument('url', help='크롤링할 네이버 블로그 URL')
    parser.add_argument('--format', choices=['markdown', 'json'], 
                       default='markdown', help='출력 형식 (기본값: markdown)')
    
    args = parser.parse_args()
    
    # URL 검증
    if 'blog.naver.com' not in args.url:
        print("❌ 네이버 블로그 URL이 아닙니다.")
        return
    
    crawler = NaverBlogCrawler()
    result = await crawler.crawl_url(args.url, args.format)
    
    if result:
        print("\n=== 크롤링 결과 요약 ===")
        print(f"제목: {result['title']}")
        print(f"작성자: {result['author']}")
        print(f"작성일: {result['published_date']}")
        print(f"내용 길이: {result['content_length']}자")
        print(f"단어 수: {result['word_count']}개")
        print(f"이미지 수: {result.get('image_count', 0)}개")
        print("✅ 크롤링 성공!")
    else:
        print("❌ 크롤링 실패")


if __name__ == "__main__":
    asyncio.run(main()) 
