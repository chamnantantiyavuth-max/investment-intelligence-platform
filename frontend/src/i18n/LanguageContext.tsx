/**
 * Language context — Thai default, English toggle (FD: 10 Aug 2026).
 * Persists choice in localStorage; Thai is the initial default.
 */
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { LANG_STORAGE_KEY, type Lang } from "./translations";

interface LangContextValue {
  lang: Lang;
  setLang: (l: Lang) => void;
  toggleLang: () => void;
}

const LangContext = createContext<LangContextValue | null>(null);

function initialLang(): Lang {
  try {
    const stored = localStorage.getItem(LANG_STORAGE_KEY);
    if (stored === "en" || stored === "th") return stored;
  } catch {
    /* SSR / privacy mode — default */
  }
  return "th"; // Thai is the default language (Founder, 10 Aug 2026)
}

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang);

  useEffect(() => {
    document.documentElement.lang = lang === "th" ? "th" : "en";
    try {
      localStorage.setItem(LANG_STORAGE_KEY, lang);
    } catch {
      /* ignore */
    }
  }, [lang]);

  const setLang = (l: Lang) => setLangState(l);
  const toggleLang = () => setLangState((prev) => (prev === "th" ? "en" : "th"));

  return <LangContext.Provider value={{ lang, setLang, toggleLang }}>{children}</LangContext.Provider>;
}

export function useLang(): LangContextValue {
  const ctx = useContext(LangContext);
  if (!ctx) throw new Error("useLang must be used within LangProvider");
  return ctx;
}
