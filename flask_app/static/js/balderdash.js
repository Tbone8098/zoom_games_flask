var allBtnJs = document.querySelectorAll('.btnJs')

for (const btn of allBtnJs) {
    btn.addEventListener('click', function(){
        var action = btn.getAttribute('action')
        if (action === 'form'){
            openForm(btn)
        }
    })
}

function openForm(button){
    var allForms = document.querySelectorAll('.form')
    for (const form of allForms) {
        form.style.display = 'none'
    }
    var form = document.querySelector('.' + button.getAttribute('data'))
    if (form.style.display == 'block'){
        form.style.display = 'none'
    }else {
        form.style.display = 'block'
    }
    console.log(form.style.display);
}