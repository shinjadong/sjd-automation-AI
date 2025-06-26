import { zodToJsonSchema } from "zod-to-json-schema";
import {
  SearchArgsSchema,
  NaverLocalSearchParamsSchema,
} from "../schemas/search.schemas.js";

/**
 * 네이버 검색 도구 정의 (한국어 우선)
 */
export const searchTools = [
  {
    name: "search_webkr",
    description:
      "네이버 웹문서 검색 - 한국어 웹페이지에서 정보를 검색합니다. 일반적인 정보 검색에 가장 적합합니다.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_news",
    description: "네이버 뉴스 검색 - 최신 뉴스와 시사 정보를 검색합니다. 실시간 이슈나 최신 동향 파악에 유용합니다.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_blog",
    description: "네이버 블로그 검색 - 개인 블로그 포스팅을 검색합니다. 리뷰, 체험담, 개인 의견 등을 찾을 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_shop",
    description: "네이버 쇼핑 검색 - 상품 정보와 가격을 검색합니다. 온라인 쇼핑몰의 제품 정보와 가격 비교에 활용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_image",
    description: "네이버 이미지 검색 - 관련 이미지를 검색합니다. 시각적 자료가 필요하거나 이미지로 정보를 찾을 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_kin",
    description: "네이버 지식iN 검색 - 질문과 답변을 검색합니다. 일상적인 궁금증이나 전문 지식을 찾을 때 유용합니다.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_book",
    description: "네이버 책 검색 - 도서 정보를 검색합니다. 책 제목, 저자, 출판사 등의 정보를 찾을 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_encyc",
    description:
      "네이버 지식백과 검색 - 전문적이고 신뢰할 수 있는 백과사전 정보를 검색합니다. 정확한 정의나 학술 정보가 필요할 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_academic",
    description: "네이버 전문자료 검색 - 논문, 학술자료, 연구보고서를 검색합니다. 학술적 근거나 전문 연구 자료가 필요할 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
  {
    name: "search_local",
    description: "네이버 지역 검색 - 맛집, 병원, 상점 등 지역 정보를 검색합니다. 특정 지역의 업체나 장소를 찾을 때 사용하세요.",
    inputSchema: zodToJsonSchema(NaverLocalSearchParamsSchema),
  },
  {
    name: "search_cafearticle",
    description:
      "네이버 카페글 검색 - 카페 커뮤니티의 게시글을 검색합니다. 특정 주제의 커뮤니티 의견이나 정보를 찾을 때 사용하세요.",
    inputSchema: zodToJsonSchema(SearchArgsSchema),
  },
];
