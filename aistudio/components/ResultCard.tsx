
import React from 'react';
import { ICDResult } from '../types';

interface ResultCardProps {
  result: ICDResult;
}

export const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-md hover:shadow-xl dark:hover:shadow-blue-500/20 border border-slate-200 dark:border-slate-700 p-6 transition-all duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-[1.02]">
      <div className="flex flex-col h-full">
        <div className="flex-grow">
          <div className="flex justify-between items-start mb-3">
              <p className="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider">{result.category}</p>
          </div>
          <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100">{result.description}</h3>
        </div>
        <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
            <p className="text-2xl font-mono font-medium text-slate-600 dark:text-slate-300">{result.code}</p>
        </div>
      </div>
    </div>
  );
};

export const ResultCardSkeleton: React.FC = () => {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-md border border-slate-200 dark:border-slate-700 p-6">
          <div className="animate-pulse-fast flex flex-col h-full">
            <div className="flex-grow">
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3 mb-4"></div>
                <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-full mb-2"></div>
                <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-5/6"></div>
            </div>
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/2"></div>
            </div>
          </div>
      </div>
    );
};
