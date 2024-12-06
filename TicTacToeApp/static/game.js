const cells = document.querySelectorAll('[data-cell]');
const winnerMessage = document.getElementById('winner-message');
let currentPlayer = 'X';

cells.forEach(cell => {
    cell.addEventListener('click', handleClick, { once: true });
});

function handleClick(e) {
    const cell = e.target;
    cell.textContent = currentPlayer;
    if (checkWin(currentPlayer)) {
        winnerMessage.textContent = `¡El jugador ${currentPlayer} gana!`;
    } else if ([...cells].every(cell => cell.textContent)) {
        winnerMessage.textContent = '¡Es un empate!';
    } else {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }
}

function checkWin(player) {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    return winPatterns.some(pattern =>
        pattern.every(index => cells[index].textContent === player)
    );
}
