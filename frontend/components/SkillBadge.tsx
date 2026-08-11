import React from 'react';

interface SkillBadgeProps {
  label: string;
  category?: 'programming' | 'framework' | 'database' | 'tool' | 'cloud' | 'default';
}

export default function SkillBadge({ label, category = 'default' }: SkillBadgeProps) {
  const categoryStyles = {
    programming: 'bg-blue-500/10 text-blue-400 border-blue-500/30 hover:bg-blue-500/20',
    framework: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30 hover:bg-indigo-500/20',
    database: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20',
    tool: 'bg-purple-500/10 text-purple-400 border-purple-500/30 hover:bg-purple-500/20',
    cloud: 'bg-amber-500/10 text-amber-400 border-amber-500/30 hover:bg-amber-500/20',
    default: 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750',
  };

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium border transition-colors duration-150 ${categoryStyles[category]}`}
    >
      {label}
    </span>
  );
}
