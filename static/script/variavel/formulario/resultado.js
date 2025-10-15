// Animação de entrada
document.addEventListener('DOMContentLoaded', function() {
    const resultCard = document.querySelector('.result-card');
    resultCard.style.transform = 'translateY(20px)';
    resultCard.style.opacity = '0';
    
    setTimeout(() => {
        resultCard.style.transition = 'all 0.5s ease';
        resultCard.style.transform = 'translateY(0)';
        resultCard.style.opacity = '1';
    }, 100);
});