/**
 * UI translations — Thai (default) / English toggle.
 *
 * Thai copy standard (Founder requirement, 10 Aug 2026): natural, flowing Thai
 * that a native reader absorbs without translation-seams — NOT word-for-word
 * substitution. Terminology choices:
 *   - "Research Intelligence." -> "งานวิจัยอัจฉริยะ." (brand, kept as-is is
 *     also acceptable; we use the Thai brand with the English period style)
 *   - "published" -> "ฉบับตีพิมพ์" / "ตีพิมพ์แล้ว"
 *   - "Portfolio-blind" -> "ไม่เห็นพอร์ตการลงทุน" (explains the meaning, not
 *     the literal "blind")
 *   - "Advisory only" -> "ใช้ประกอบการวิเคราะห์เท่านั้น"
 *   - "point-in-time" -> "ข้อมูล ณ เวลานั้น" (FD #58 doctrine)
 *   - "opposing essay (CRO)" -> "บทวิเคราะห์ค้าน (CRO)"
 *   - "This week's notes" -> "บันทึกประจำสัปดาห์"
 *   - "Latest intelligence" -> "บทวิเคราะห์ล่าสุด"
 *   - "Read the report" -> "อ่านบทวิเคราะห์"
 *   - "No buy/sell instruction" -> "ไม่มีการชี้นำให้ซื้อหรือขาย"
 */

export type Lang = "th" | "en";

export const LANG_STORAGE_KEY = "iip_lang";

export const translations = {
  // ── Login ─────────────────────────────────────────────────────────────────
  "login.title": { th: "เข้าสู่ระบบ", en: "Sign in" },
  "login.subtitle": {
    th: "พื้นที่ทำงานวิจัยส่วนตัว — ข้อมูลประกอบการวิเคราะห์ ไม่ใช่คำแนะนำ",
    en: "Private research workspace — advisory intelligence, not advice.",
  },
  "login.username": { th: "ชื่อผู้ใช้", en: "Username" },
  "login.password": { th: "รหัสผ่าน", en: "Password" },
  "login.button": { th: "เข้าสู่ระบบ", en: "Sign in" },
  "login.error": {
    th: "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
    en: "Invalid username or password",
  },
  "login.momentum": {
    th: "ค้นหาโอกาสก่อนใคร — มุ่งเน้นโมเมนตัม",
    en: "Momentum-first opportunity discovery",
  },
  "login.platform": {
    th: "แพลตฟอร์มข้อมูลการลงทุน",
    en: "The Investment Intelligence Platform",
  },
  "login.decisiondesk": {
    th:
      "เครื่องมือช่วยตัดสินใจที่ลดขอบเขตการค้นหาลงทั่วโลก พร้อมเก็บหลักฐาน ความไม่แน่นอน และความเห็นที่แตกต่างไว้อย่างครบถ้วน",
    en:
      "A decision-desk that reduces the global investment search space while preserving evidence, uncertainty, and dissent.",
  },
  "login.question": {
    th: "ตอบคำถามเดียว: อะไรสมควรแก่การค้นคว้าต่อ?",
    en: "It answers one question: what deserves further investigation?",
  },
  "login.advisory": {
    th: "ใช้ประกอบการวิเคราะห์เท่านั้น — ไม่มีการชี้นำซื้อ/ขาย/จัดสรร และไม่เชื่อมต่อนายหน้า",
    en: "Advisory only — no buy/sell/allocate. No broker connectivity.",
  },
  "login.portfolioBlind": {
    th: "ไม่เห็นพอร์ตการลงทุนของคุณ — ระบบไม่เคยเข้าถึงข้อมูลการถือครอง",
    en: "Portfolio-blind: the system never sees your holdings.",
  },
  "login.dataLabeled": {
    th: "ข้อมูลทุกหน้าถูกกำกับว่าจริง ผสม หรือจำลอง",
    en: "Data is labeled real, hybrid, or synthetic on every page.",
  },
  "login.pillars": {
    th: "Alpha Momentum · Close System · Fundamental & Opportunity — แกนข้อมูลอัจฉริยะเดียวกัน",
    en: "Alpha Momentum · Close System · Fundamental & Opportunity — one shared intelligence core",
  },

  // ── Library / magazine ─────────────────────────────────────────────────────
  "library.brand": { th: "งานวิจัยอัจฉริยะ", en: "Research Intelligence" },
  "library.published": {
    th: "{n} ฉบับตีพิมพ์ · {date}",
    en: "{n} published · {date}",
  },
  "library.featured": { th: "บทเด่น", en: "Featured" },
  "library.weekNotes": { th: "บันทึกประจำสัปดาห์", en: "This week's notes" },
  "library.latest": { th: "บทวิเคราะห์ล่าสุด", en: "Latest intelligence" },
  "library.readReport": { th: "อ่านบทวิเคราะห์ →", en: "Read the report →" },
  "library.opposing": {
    th: "บทวิเคราะห์ค้าน (CRO)",
    en: "The opposing essay (CRO)",
  },
  "library.opposingShort": { th: "+ บทค้าน", en: "+ opposing" },
  "library.search": { th: "ค้นหา", en: "Search" },
  "library.searchPlaceholder": {
    th: "ชื่อเรื่อง, หัวข้อ, ผู้เขียน…",
    en: "title, subject, author…",
  },
  "library.status": { th: "สถานะ", en: "Status" },
  "library.type": { th: "ประเภท", en: "Type" },
  "library.sort": { th: "เรียง", en: "Sort" },
  "library.statusAll": { th: "ทั้งหมด", en: "all" },
  "library.statusPublished": { th: "ตีพิมพ์แล้ว", en: "published" },
  "library.statusReview": { th: "กำลังตรวจ", en: "in review" },
  "library.statusDraft": { th: "ร่าง", en: "draft" },
  "library.sortNewest": { th: "ใหม่ที่สุดก่อน", en: "newest first" },
  "library.sortOldest": { th: "เก่าที่สุดก่อน", en: "oldest first" },
  "library.sortTitle": { th: "ชื่อเรื่อง ก–ฮ", en: "title A–Z" },
  "library.sortSeries": { th: "ชุดบทวิเคราะห์", en: "series" },
  "library.emptyTitle": {
    th: "ไม่มีบทวิเคราะห์ที่ตรงกับตัวกรอง",
    en: "No reports match your filters.",
  },
  "library.emptyBody": {
    th:
      "ลองล้างตัวกรองหรือคำค้นเพื่อดูคลังทั้งหมด — บทวิเคราะห์ของทีมวิจัยจะปรากฏที่นี่เมื่อผ่านการตรวจ",
    en:
      "Clear the search or filters to see the full library. The research team's reports appear here as they pass review.",
  },
  "library.clearFilters": { th: "ล้างตัวกรอง →", en: "Clear filters →" },
  "library.all": { th: "ทั้งหมด", en: "All" },
  "library.notes": { th: "บทความ", en: "notes" },
  "library.tagline": {
    th: "บันทึกงานวิจัยอ้างอิงหลักฐาน — ใช้ประกอบการวิเคราะห์เท่านั้น",
    en: "Evidence-based research notes — advisory only.",
  },
  "library.footerLine": {
    th:
      "ไม่เห็นพอร์ตการลงทุน · ข้อมูล ณ เวลานั้น (FD #58) · ไม่มีการชี้นำซื้อ/ขาย — {n} ฉบับตีพิมพ์",
    en:
      "Portfolio-blind · Point-in-time data (FD #58) · No buy/sell instruction. {n} published reports.",
  },
  "library.typeLabel.company": { th: "บทวิเคราะห์บริษัท", en: "Company" },
  "library.typeLabel.product": { th: "บทวิเคราะห์สินค้าโภคภัณฑ์", en: "Product" },
  "library.typeLabel.weekly": { th: "จดหมายรายสัปดาห์", en: "Weekly" },
  "library.typeLabel.quarterly": { th: "รายงานรายไตรมาส", en: "Quarterly" },
  "library.typeLabel.theme": { th: "บทวิเคราะห์ธีม", en: "Theme" },
  "library.typeKicker.company": { th: "งานวิจัยบริษัท", en: "Company Research" },
  "library.typeKicker.product": { th: "สินค้าโภคภัณฑ์", en: "Commodities" },
  "library.typeKicker.weekly": { th: "ข่าวกรองรายสัปดาห์", en: "Weekly Intelligence" },
  "library.typeKicker.quarterly": { th: "รายไตรมาส", en: "Quarterly" },
  "library.typeKicker.theme": { th: "ธีม", en: "Theme" },

  // ── Article page ───────────────────────────────────────────────────────────
  "article.back": { th: "← คลังบทวิเคราะห์", en: "Library" },
  "article.typeLabel.company": { th: "บันทึกงานวิจัยบริษัท", en: "Company Research Note" },
  "article.typeLabel.product": { th: "บันทึกงานวิจัยสินค้าโภคภัณฑ์", en: "Product Research Note" },
  "article.typeLabel.weekly": { th: "จดหมายข่าวรายสัปดาห์", en: "Weekly Brief" },
  "article.typeLabel.quarterly": { th: "รายงานรายไตรมาส", en: "Quarterly Report" },
  "article.typeLabel.theme": { th: "บันทึกธีม", en: "Theme Note" },
  "article.realData": {
    th: "ข้อมูลจริง · อ้างอิงแหล่งที่มาและวันที่",
    en: "Real data · sourced & dated",
  },
  "article.portfolioBlind": { th: "ไม่เห็นพอร์ตการลงทุน", en: "Portfolio-blind" },
  "article.advisoryOnly": {
    th: "ใช้ประกอบการวิเคราะห์เท่านั้น — ไม่มีการชี้นำซื้อ/ขาย",
    en: "Advisory only — no buy/sell instruction",
  },
  "article.notFound": { th: "ไม่พบบทวิเคราะห์นี้", en: "Report not found." },
  "article.loadError": {
    th: "ไม่สามารถโหลดบทวิเคราะห์นี้ได้",
    en: "Could not load this report.",
  },
  "article.retry": { th: "ลองอีกครั้ง →", en: "Retry →" },
  "article.footerNote": {
    th: "ข้อมูล ณ เวลานั้น · ไม่เห็นพอร์ตการลงทุน · ไม่มีการชี้นำซื้อ/ขาย",
    en: "Advisory only · Portfolio-blind · Point-in-time data (FD #58)",
  },
  "article.later": { th: "บทถัดไปของ {subject} →", en: "Later {subject} note →" },
  "article.earlier": { th: "← บทก่อนหน้าของ {subject}", en: "← Earlier {subject} note" },

  // ── Org Office / Kanban / Audit ────────────────────────────────────────────
  "org.title": { th: "สำนักงานองค์กร", en: "Org Office" },
  "kanban.title": { th: "กระดานคัมบัง", en: "Kanban Board" },
  "audit.title": { th: "ศูนย์ตรวจสอบ", en: "Audit Center" },

  // ── Language toggle ────────────────────────────────────────────────────────
  "lang.switchToEn": { th: "English", en: "ไทย" },
} as const;

export type TranslationKey = keyof typeof translations;

export function translate(key: string, lang: Lang, vars?: Record<string, string | number>): string {
  const entry = (translations as Record<string, { th: string; en: string } | undefined>)[key];
  if (!entry) return key;
  let s = entry[lang];
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      s = s.replaceAll(`{${k}}`, String(v));
    }
  }
  return s;
}
