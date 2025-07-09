document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const docElement = document.documentElement;
      // Toggle the 'dark' class on the <html> element
      docElement.classList.toggle('dark');
      
      // Determine the new theme and save it to localStorage
      const newTheme = docElement.classList.contains('dark') ? 'dark' : 'light';
      localStorage.setItem('theme', newTheme);
    });
  }

  // The 'autofocus' attribute on the input field in index.html handles
  // the initial focus, so no additional JavaScript is needed for that.
});
