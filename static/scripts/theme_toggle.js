const btn = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
function updateButton() {
    if(document.body.classList.contains('light-mode')) {
        btn.innerHTML = '<svg width="21" height="21" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="8" fill="#0af"/><path d="M6.5 8c0-2.21 1.79-4 4-4 .26 0 .51.02.76.07A6.001 6.001 0 014.07 13.24c.05-.25.07-.5.07-.76 0-2.21 1.79-4 4-4z" fill="#fff"/></svg>';
        btn.title = "Modo Escuro";
    } else {
        btn.innerHTML = '<svg width="21" height="21" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="8" fill="#ffe600"/><path d="M9 4v2M9 12v2M4 9H6M12 9h2" stroke="#f59e00" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="9" r="5" fill="#fffae0" /></svg>';
        btn.title = "Modo Claro";
    }
}
function setInitialTheme() {
    let theme = localStorage.getItem('theme');
    if(theme === 'light' || (!theme && prefersDark.matches === false)) {
        document.body.classList.add('light-mode');
    } else {
        document.body.classList.remove('light-mode');
    }
    updateButton();
}
btn.addEventListener('click', function(){
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    updateButton();
});
setInitialTheme();
prefersDark.addEventListener('change', setInitialTheme);
