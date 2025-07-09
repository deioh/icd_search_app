
import React, { useState, useEffect, useCallback } from 'react';
import { ICDResult } from './types';
import { fetchICDCodes } from './services/geminiService';
import { SearchInput } from './components/SearchInput';
import { ResultsDisplay } from './components/ResultsDisplay';
import { ThemeToggle } from './components/ThemeToggle';
import { LogoIcon } from './components/icons/LogoIcon';

type Theme = 'light' | 'dark';

export default function App() {
  const [theme, setTheme] = useState<Theme>('light');
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<ICDResult[] | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check for saved theme in localStorage or system preference
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    const userPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (userPrefersDark ? 'dark' : 'light');
    setTheme(initialTheme);
  }, []);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [theme]);

  const handleSearch = useCallback(async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults(null);
      setError(null);
      return;
    }
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const apiResults = await fetchICDCodes(searchQuery);
      setResults(apiResults);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 font-sans transition-colors duration-300">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="flex justify-between items-center mb-8">
            <div className="flex items-center gap-3">
                <LogoIcon className="h-10 w-10 text-blue-600 dark:text-blue-500" />
                <h1 className="text-2xl md:text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-teal-500 dark:from-blue-500 dark:to-teal-400">
                    ICD Search
                </h1>
            </div>
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        </header>

        <main>
          <div className="mb-12">
            <SearchInput
              query={query}
              setQuery={setQuery}
              onSearch={handleSearch}
              isLoading={isLoading}
            />
          </div>
          
          <ResultsDisplay
            results={results}
            isLoading={isLoading}
            error={error}
          />
        </main>
        
        <footer className="text-center mt-16 text-slate-500 dark:text-slate-400 text-sm space-y-2">
            <p>Developed by SirDei</p>
            <p>Powered by Google Gemini. For informational purposes only.</p>
        </footer>
      </div>
    </div>
  );
}