import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/Navbar';

export const metadata: Metadata = {
  title: 'AI Job Finder - Personal AI-Powered Job Matcher',
  description: 'Upload your resume, extract candidate profiles, and discover perfectly matched job opportunities across 13 job sources.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 flex flex-col min-h-screen antialiased selection:bg-brand-500 selection:text-white">
        <Navbar />
        <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          {children}
        </main>
        <footer className="border-t border-slate-800/80 bg-slate-900/40 py-6 text-center text-xs text-slate-500">
          <p>© 2026 AI Job Finder. Personal AI Job Discovery Engine — Built with FastAPI, Next.js, PostgreSQL & AI.</p>
        </footer>
      </body>
    </html>
  );
}
