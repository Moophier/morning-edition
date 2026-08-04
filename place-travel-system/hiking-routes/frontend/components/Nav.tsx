"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

export default function Nav() {
  const { user, logout } = useAuth();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-12 flex items-center justify-between px-7 border-b border-[#1c2e22] bg-[rgba(5,9,7,.94)] backdrop-blur-xl">
      <Link href="/" className="font-mono text-[11px] text-[#c9a24e] tracking-[3px] uppercase">
        野径图鉴
      </Link>
      <div className="flex items-center gap-2">
        <Link href="/create" className="font-sans text-xs px-3 py-1.5 rounded-full text-[rgba(255,255,255,.45)] hover:text-white hover:bg-[rgba(255,255,255,.08)] transition-all">
          创建路线
        </Link>
        {user ? (
          <div className="flex items-center gap-3">
            <span className="font-sans text-xs text-text-dim">{user.name}</span>
            <button onClick={logout} className="font-sans text-xs px-3 py-1.5 rounded-full text-text-muted hover:text-text hover:bg-[rgba(200,162,78,.08)] transition-all">
              退出
            </button>
          </div>
        ) : (
          <Link href="/auth/login" className="font-sans text-xs px-3 py-1.5 rounded-full text-[rgba(255,255,255,.45)] hover:text-white hover:bg-[rgba(255,255,255,.08)] transition-all">
            登录
          </Link>
        )}
      </div>
    </nav>
  );
}
