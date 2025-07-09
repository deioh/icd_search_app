
import React from 'react';
import { SearchIcon } from './icons/SearchIcon';

interface SearchInputProps {
  query: string;
  setQuery: (query: string) => void;
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export const SearchInput: React.FC<SearchInputProps> = ({ query, setQuery, onSearch, isLoading }) => {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., 'unspecified asthma' or 'type 2 diabetes'"
        autoFocus
        className="w-full pl-12 pr-4 py-4 text-lg bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-700 rounded-full focus:ring-4 focus:ring-blue-500/50 dark:focus:ring-blue-500/30 focus:border-blue-500 dark:focus:border-blue-500 outline-none transition-all duration-300 shadow-sm"
        disabled={isLoading}
      />
      <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500">
        <SearchIcon className="h-6 w-6" />
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2.5 bg-blue-600 text-white font-semibold rounded-full hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 disabled:bg-slate-400 dark:disabled:bg-slate-600 disabled:cursor-not-allowed transition-all duration-300 transform active:scale-95"
      >
        {isLoading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
};
