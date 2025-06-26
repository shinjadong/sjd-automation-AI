import { zodToJsonSchema } from "zod-to-json-schema";
import {
  DatalabSearchSchema,
  DatalabShoppingSchema,
  DatalabShoppingDeviceSchema,
  DatalabShoppingGenderSchema,
  DatalabShoppingAgeSchema,
  DatalabShoppingKeywordsSchema,
  DatalabShoppingKeywordDeviceSchema,
  DatalabShoppingKeywordGenderSchema,
  DatalabShoppingKeywordAgeSchema
} from "../schemas/datalab.schemas.js";

/**
 * 네이버 데이터랩 도구 정의 (한국어 우선)
 */
export const datalabTools = [
  {
    name: "datalab_search",
    description: "네이버 검색어 트렌드 분석 - 특정 키워드의 검색량 변화와 인기도를 시간별로 분석합니다. 마케팅 전략 수립에 유용합니다.",
    inputSchema: zodToJsonSchema(DatalabSearchSchema),
  },
  {
    name: "datalab_shopping_category",
    description: "네이버 쇼핑 카테고리별 트렌드 분석 - 특정 상품 카테고리의 쇼핑 트렌드를 분석합니다. 시장 동향 파악과 상품 기획에 활용하세요.",
    inputSchema: zodToJsonSchema(DatalabShoppingSchema),
  },
  {
    name: "datalab_shopping_by_device",
    description: "네이버 쇼핑 기기별 트렌드 분석 - PC와 모바일 등 기기별 쇼핑 패턴을 분석합니다. 디지털 마케팅 전략 수립에 도움이 됩니다.",
    inputSchema: zodToJsonSchema(
      DatalabShoppingDeviceSchema.pick({
        startDate: true,
        endDate: true,
        timeUnit: true,
        category: true,
        device: true,
      })
    ),
  },
  {
    name: "datalab_shopping_by_gender",
    description: "네이버 쇼핑 성별 트렌드 분석 - 남성과 여성의 쇼핑 선호도와 패턴을 분석합니다. 타겟 마케팅과 상품 개발에 활용하세요.",
    inputSchema: zodToJsonSchema(
      DatalabShoppingGenderSchema.pick({
        startDate: true,
        endDate: true,
        timeUnit: true,
        category: true,
        gender: true,
      })
    ),
  },
  {
    name: "datalab_shopping_by_age",
    description: "네이버 쇼핑 연령별 트렌드 분석 - 연령대별 쇼핑 선호도와 구매 패턴을 분석합니다. 세대별 마케팅 전략 수립에 유용합니다.",
    inputSchema: zodToJsonSchema(
      DatalabShoppingAgeSchema.pick({
        startDate: true,
        endDate: true,
        timeUnit: true,
        category: true,
        ages: true,
      })
    ),
  },
  {
    name: "datalab_shopping_keywords",
    description: "네이버 쇼핑 키워드별 트렌드 분석 - 특정 쇼핑 키워드의 검색량과 관심도 변화를 분석합니다. 상품 키워드 최적화에 활용하세요.",
    inputSchema: zodToJsonSchema(DatalabShoppingKeywordsSchema),
  },
  {
    name: "datalab_shopping_keyword_by_device",
    description: "네이버 쇼핑 키워드 기기별 트렌드 분석 - 특정 키워드에 대한 PC/모바일별 검색 패턴을 분석합니다. 채널별 최적화 전략에 도움이 됩니다.",
    inputSchema: zodToJsonSchema(DatalabShoppingKeywordDeviceSchema),
  },
  {
    name: "datalab_shopping_keyword_by_gender",
    description: "네이버 쇼핑 키워드 성별 트렌드 분석 - 특정 키워드에 대한 남녀별 관심도와 검색 패턴을 분석합니다. 성별 타겟팅에 활용하세요.",
    inputSchema: zodToJsonSchema(DatalabShoppingKeywordGenderSchema),
  },
  {
    name: "datalab_shopping_keyword_by_age",
    description: "네이버 쇼핑 키워드 연령별 트렌드 분석 - 특정 키워드에 대한 연령대별 관심도와 검색 패턴을 분석합니다. 세대별 마케팅에 유용합니다.",
    inputSchema: zodToJsonSchema(DatalabShoppingKeywordAgeSchema),
  },
]; 