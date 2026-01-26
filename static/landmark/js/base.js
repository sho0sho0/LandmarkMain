document.addEventListener('DOMContentLoaded', function() {
    const corporates = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');

    corporates.addEventListener('mouseenter', () => {
        dropdownContent.style.display = 'block';
    });

    corporates.addEventListener('mouseleave', () => {
        dropdownContent.style.display = 'none';
    });
});
function showsidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'flex'
 }
 function hidesidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'none'
 }