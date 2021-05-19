console.log('client side file is loading')



const weatherform = document.querySelector('form')
const search = document.querySelector('input')
const messageOne = document.querySelector('#message-1')
const messageTwo = document.querySelector('#message-2')




weatherform.addEventListener('submit', (e) => {
    e.preventDefault()
    messageOne.textContent = 'Loading'
    messageTwo.textContent = '  '


    const location  = search.value
    const addr = 'http://localhost:3000/weather?address='+location
    fetch(addr).then((response) => {
    response.json().then((data) => {
        if(data.error)
        {
            messageOne.textContent = data.error
            messageTwo.textContent = '  '
        }
        else
        {
            messageOne.textContent = data.address
            messageTwo.textContent = data.forecast
        }
    })
})
})