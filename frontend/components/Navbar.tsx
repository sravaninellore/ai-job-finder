'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Briefcase, Upload, Sliders, LayoutDashboard, BookmarkCheck, Mail } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: '/jobs', label: 'Jobs Dashboard', icon: LayoutDashboard },
    { href: '/tracker', label: 'CRM Tracker', icon: BookmarkCheck },
    { href: '/upload', label: 'Resume & Profile', icon: Upload },
    { href: '/preferences', label: 'Job Preferences', icon: Sliders },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-slate-900/85 border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="p-2 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 text-white shadow-lg shadow-brand-500/20 group-hover:scale-105 transition-transform duration-200">
                <Briefcase className="w-5 h-5" />
              </div>
              <div>
                <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-indigo-200 bg-clip-text text-transparent">
                  AI Job Finder
                </span>
              </div>
            </Link>
          </div>

          <nav className="flex items-center gap-1 sm:gap-2">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline">{link.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}
