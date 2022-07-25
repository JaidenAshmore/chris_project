//DOM
const answer = document.getElementById('answer');
const buttons = document.getElementsByClassName('button-hero');
const heroForm = document.getElementById('hero-form')


//Event Listeners
const activate_buttons = () => {
    for (const button of buttons) {
        button.addEventListener('click', function(e) {
            const clicked = e.target
            const allButtons = clicked.parentElement.children;
            if (clicked.textContent === answer.value) {
                const newInput = document.createElement('input')
                newInput.type = 'hidden'
                newInput.name = 'clicked'
                newInput.value = clicked.textContent
                console.log(newInput)
                heroForm.appendChild(newInput)
                clicked.classList.add('correct');
            } else {
                clicked.classList.add('incorrect');
            }
            for(const a of allButtons) {
                a.classList.add('no-click');
            }
        })
    }
}

activate_buttons()