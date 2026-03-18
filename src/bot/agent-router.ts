import fs from "fs";
import path from "path";
import { getAgentsDir } from "../util/paths.js";

const AGENT_ROUTES: Record<string, [string, string]> = {
  // Strategy
  pmf: ["strategy", "pmf-planner"],
  "시장 적합": ["strategy", "pmf-planner"],
  가설: ["strategy", "pmf-planner"],
  "기능 기획": ["strategy", "feature-planner"],
  "기능 추가": ["strategy", "feature-planner"],
  스펙: ["strategy", "feature-planner"],
  정책: ["strategy", "policy-architect"],
  약관: ["strategy", "policy-architect"],
  "데이터 분석": ["strategy", "data-analyst"],
  지표: ["strategy", "data-analyst"],
  매출: ["strategy", "data-analyst"],
  "사업 전략": ["strategy", "business-strategist"],
  "수익 모델": ["strategy", "business-strategist"],
  비즈니스: ["strategy", "business-strategist"],
  아이디어: ["strategy", "idea-refiner"],
  브레인스토밍: ["strategy", "idea-refiner"],
  일정: ["strategy", "scope-estimator"],
  견적: ["strategy", "scope-estimator"],
  스코프: ["strategy", "scope-estimator"],
  // Growth
  마케팅: ["growth", "gtm-strategist"],
  gtm: ["growth", "gtm-strategist"],
  런칭: ["growth", "gtm-strategist"],
  카피: ["growth", "content-writer"],
  블로그: ["growth", "content-writer"],
  글쓰기: ["growth", "content-writer"],
  콘텐츠: ["growth", "content-writer"],
  브랜드: ["growth", "brand-marketer"],
  브랜딩: ["growth", "brand-marketer"],
  네이밍: ["growth", "brand-marketer"],
  광고: ["growth", "paid-marketer"],
  퍼포먼스: ["growth", "paid-marketer"],
  cpa: ["growth", "paid-marketer"],
  // Experience
  "유저 리서치": ["experience", "user-researcher"],
  인터뷰: ["experience", "user-researcher"],
  설문: ["experience", "user-researcher"],
  페르소나: ["experience", "user-researcher"],
  "시장 조사": ["experience", "desk-researcher"],
  경쟁사: ["experience", "desk-researcher"],
  벤치마크: ["experience", "desk-researcher"],
  ux: ["experience", "ux-designer"],
  와이어프레임: ["experience", "ux-designer"],
  사용성: ["experience", "ux-designer"],
  플로우: ["experience", "ux-designer"],
  ui: ["experience", "ui-designer"],
  "디자인 시스템": ["experience", "ui-designer"],
  목업: ["experience", "ui-designer"],
  // Engineering
  프론트: ["engineering", "creative-frontend"],
  프론트엔드: ["engineering", "creative-frontend"],
  랜딩: ["engineering", "creative-frontend"],
  프로토타입: ["engineering", "fde"],
  mvp: ["engineering", "fde"],
  "빠르게 만들": ["engineering", "fde"],
  아키텍처: ["engineering", "architect"],
  설계: ["engineering", "architect"],
  "시스템 구조": ["engineering", "architect"],
  백엔드: ["engineering", "backend-developer"],
  서버: ["engineering", "backend-developer"],
  db: ["engineering", "backend-developer"],
  api: ["engineering", "api-developer"],
  엔드포인트: ["engineering", "api-developer"],
  크롤링: ["engineering", "data-collector"],
  수집: ["engineering", "data-collector"],
  스크래핑: ["engineering", "data-collector"],
  파이프라인: ["engineering", "data-engineer"],
  etl: ["engineering", "data-engineer"],
  배포: ["engineering", "cloud-admin"],
  인프라: ["engineering", "cloud-admin"],
  도커: ["engineering", "cloud-admin"],
  "ci/cd": ["engineering", "cloud-admin"],
};

/** Find the best matching agent for user input. */
export function findAgent(userInput: string): [string, string] | null {
  const lower = userInput.toLowerCase();
  for (const [keyword, route] of Object.entries(AGENT_ROUTES)) {
    if (lower.includes(keyword)) return route;
  }
  return null;
}

/** Load agent SKILL.md content. */
export function loadAgentSkill(team: string, agent: string): string {
  const skillFile = path.join(getAgentsDir(), team, agent, "SKILL.md");
  if (fs.existsSync(skillFile)) {
    return fs.readFileSync(skillFile, "utf-8");
  }
  return "";
}
