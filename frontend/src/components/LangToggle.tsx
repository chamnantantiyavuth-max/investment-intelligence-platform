/**
 * Language toggle — small masthead control (Thai default / English).
 */
import { useLang } from "../i18n/LanguageContext";
import { translate } from "../i18n/translations";

export function LangToggle() {
  const { lang, toggleLang } = useLang();
  return (
    <button
      type="button"
      onClick={toggleLang}
      aria-label={lang === "th" ? "Switch to English" : "เปลี่ยนเป็นภาษาไทย"}
      className="whitespace-nowrap rounded-sm border border-rule px-2 py-1 font-mono text-[10px] font-semibold uppercase tracking-[0.12em] text-ink-2 transition-colors hover:border-primary hover:text-primary"
    >
      {translate("lang.switchToEn", lang)}
    </button>
  );
}
