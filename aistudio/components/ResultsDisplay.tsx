
import React from 'react';
import { ICDResult } from '../types';
import { ResultCard, ResultCardSkeleton } from './ResultCard';
import { NoResultsIcon } from './icons/NoResultsIcon';
import { ErrorIcon } from './icons/ErrorIcon';

interface ResultsDisplayProps {
  results: ICDResult[] | null;
  isLoading: boolean;
  error: string | null;
}

const EmptyState: React.FC<{ icon: React.ReactNode; title: string; message: string }> = ({ icon, title, message }) => (
    <div className="text-center py-16 px-6 bg-slate-100 dark:bg-slate-800/50 rounded-lg">
        <div className="mx-auto h-16 w-16 text-slate-400 dark:text-slate-500">{icon}</div>
        <h3 className="mt-4 text-xl font-semibold text-slate-800 dark:text-slate-100">{title}</h3>
        <p className="mt-2 text-slate-500 dark:text-slate-400">{message}</p>
    </div>
);


export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, index) => (
          <ResultCardSkeleton key={index} />
        ))}
      </div>
    );
  }

  if (error) {
    return <EmptyState icon={<ErrorIcon />} title="An Error Occurred" message={error} />;
  }

  if (results && results.length === 0) {
    return <EmptyState icon={<NoResultsIcon />} title="No Results Found" message="Try adjusting your search terms for better results." />;
  }
  
  if (results === null) {
      return (
          <div className="text-center py-16 text-slate-500 dark:text-slate-400">
              <p>Enter a medical term or condition above to begin your search.</p>
          </div>
      );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {results.map((result, index) => (
        <ResultCard key={`${result.code}-${index}`} result={result} />
      ))}
    </div>
  );
};
