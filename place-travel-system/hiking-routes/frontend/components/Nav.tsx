"use client";

import Link from "next/link";

export default function Nav() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-12 flex items-center justify-between px-7 border-b border-[#1c2e22] bg-[rgba(5,9,7,.94)] backdrop-blur-xl">
      <Link href="/" className="font-mono text-[11px] text-[#c9a24e] tracking-[3px] uppercase">
        野径图鉴
      </Link>
      <div className="flex items-center gap-2">
        <Link href="/create" className="font-sans text-xs px-3 py-1.5 rounded-full text-[rgba(255,255,255,.45)] hover:text-white hover:bg-[rgba(255,255,255,.08)] transition-all">
          创建路线
        </Link>
        <Link href="/auth/login" className="font-sans text-xs px-3 py-1.5 rounded-full text-[rgba(255,255,255,.45)] hover:text-white hover:bg-[rgba(255,255,255,.08)] transition-all">
          登录
        </Link>
      </div>
    </nav>
  );
}
