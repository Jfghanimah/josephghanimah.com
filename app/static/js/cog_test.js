document.addEventListener('DOMContentLoaded', () => {
    let level = 1;
    let lives = 3;
    let startTime;
    let gameStarted = false;
    let results = [];
    const baseMemorizeTime = 3000; // 3 seconds

    const livesElement = document.getElementById('lives');
    const levelElement = document.getElementById('level');
    const numberElement = document.getElementById('number');
    const inputElement = document.getElementById('input');
    const startButton = document.getElementById('start-button');
    const nextButton = document.getElementById('next-button');
    const progressBar = document.querySelector('.progress');
    const timerBar = document.getElementById('timer-bar');
    const messageElement = document.getElementById('message');

    startButton.addEventListener('click', startGame);
    nextButton.addEventListener('click', startLevel);
    inputElement.addEventListener('keyup', (event) => {
        if (event.key === 'Enter' && gameStarted) {
            checkAnswer();
        }
    });

    function startGame() {
        gameStarted = true;
        startButton.style.display = 'none';
        startLevel();
    }

    function startLevel() {
        nextButton.style.display = 'none';
        messageElement.textContent = '';
        numberElement.textContent = generateNumber(level);
        numberElement.style.display = 'block';
        inputElement.style.display = 'none';
        inputElement.value = '';
        progressBar.style.display = 'block';
        startTimer();
        setTimeout(() => {
            numberElement.style.display = 'none';
            inputElement.style.display = 'block';
            inputElement.focus();
            startTime = new Date().getTime();
        }, baseMemorizeTime +  1000 * level);
    }

    function generateNumber(length) {
        let result = '';
        for (let i = 0; i < length; i++) {
            result += Math.floor(Math.random() * 10);
        }
        return result;
    }

    function startTimer() {
        let width = 100;
        const intervalId = setInterval(() => {
            if (width <= 0) {
                clearInterval(intervalId);
            } else {
                width -= 100 / ((baseMemorizeTime +  1000 * level) / 50);
                timerBar.style.width = width + '%';
            }
        }, 50);
    }

    function checkAnswer() {
        const userInput = inputElement.value;
        const number = numberElement.textContent;

        if (userInput === number) {
            const endTime = new Date().getTime();
            const answerTime = (endTime - startTime) / 1000;
            results.push({ level: level, time: answerTime });
            level++;
            levelElement.textContent = level;
            messageElement.textContent = 'Correct! Click "Next" or press Enter to proceed.';
            nextButton.style.display = 'block';
        } else {
            lives--;
            livesElement.textContent = lives;
            results.push({ level: level, livesLost: 1 });
            if (lives === 0) {
                endGame();
            } else {
                messageElement.textContent = `Wrong answer! You have ${lives} lives left.`;
                startLevel();
            }
        }
    }

    function endGame() {
        gameStarted = false;
        startButton.style.display = 'block';
        inputElement.style.display = 'none';
        progressBar.style.display = 'none';
        messageElement.textContent = 'Game over! Check the console for your results.';
        console.log('Results:', results);
        level = 1;
        lives = 3;
        results = [];
        livesElement.textContent = lives;
        levelElement.textContent = level;
    }
});