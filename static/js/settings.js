//DOM
const button = document.getElementById('settings_button')
const settings = document.getElementById('cog')


//Event Listeners
button.addEventListener('click', function(e) {
    const partymode = document.getElementById('party_mode')
    if(partymode.value === "on") {
        const bodyEle = document.getElementsByTagName('body');
        bodyEle.classList.add('party');
    }
})

settings.addEventListener('click', function() {
    const modal = document.getElementById('modal')
    const close = document.getElementById('button_close')
    modal.style.visibility = 'visible'
    close.addEventListener('click', function() {
        modal.style.visibility = 'hidden'
    })
})