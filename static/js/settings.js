//DOM
const save_settings = document.getElementById('save_settings')
const fire = document.getElementById('fire')
const activate_modals = document.getElementsByClassName('activate_modal')

//GLOBAL
state = 0

//MODALS - Event Listener 
for (const button of activate_modals) {
    button.addEventListener('click', function(e) {
        const type = e.target.id
        const modal = document.querySelector(`.${type}`)        
        modal.style.visibility = 'visible' 
        const close = modal.firstElementChild.children[0]
        close.addEventListener('click', function() {
            modal.style.visibility = 'hidden'
        })
    });
}

//SETTINGS
save_settings.addEventListener('click', function() {
    const animate_bg = document.getElementById('animate_bg')
    const bodyEle = document.querySelector('body')
    
    if(animate_bg.checked) {     
        bodyEle.classList.add('animate_bg')
    } else {
        bodyEle.classList.remove('animate_bg')
    }
    const modal = save_settings.parentElement.parentElement.parentElement.parentElement
    console.log(modal)
    modal.style.visibility = 'hidden'
})

fire.addEventListener('click', function() {
    if(fire.checked) {
        alert("Looks dangerous... click 'SAVE' if you're sure")
    } else {
        alert("Maybe that's for the best...")
    }
})
