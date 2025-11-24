const btn = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
function updateButton() {
    if(document.body.classList.contains('light-mode')) {
        btn.innerHTML =
            '<svg width="21" height="21" viewBox="0 0 18 18" fill="none">' +
            '<path d="M14.2 11.35A6 6 0 0 1 6.62 3.52a.5.5 0 0 0-.63-.62A7 7 0 1 0 14.7 12a.5.5 0 0 0-.5-.65z" fill="#a2c3f6"/>' +
            '</svg>';

        btn.title = "Modo Escuro";
    } else {
        btn.innerHTML = '<svg width="21" height="21" viewBox="0 0 18 18" fill="none"><rcle cx="9" cy="9" r="8" fill="#f3f7fbfb"/><path d="M9 4v2M9 12v2M4 9H6M12 9h2" stroke="#b2cefa" stroke-width="2" stroke-linecap="round"/>ircle cx="9" cy="9" r="5" fill="#fffff" /></svg>';
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
