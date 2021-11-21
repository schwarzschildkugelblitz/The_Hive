const totalTimeBox = document.querySelector('#time-box')
const totalCountBox = document.querySelector('#count-box')

const startBtn = document.querySelector('#start-btn')
const stopBtn = document.querySelector('#stop-btn')
const resetBtn = document.querySelector('#reset-btn')

const pSlider = document.querySelector('#p-slider')
const iSlider = document.querySelector('#i-slider')
const dSlider = document.querySelector('#d-slider')
const pInput = document.querySelector('#p-input')
const iInput = document.querySelector('#i-input')
const dInput = document.querySelector('#d-input')

let pValue = parseInt(40)
let iValue = parseInt(40)
let dValue = parseInt(40)

pSlider.addEventListener('input', sliderUpdate)
iSlider.addEventListener('input', sliderUpdate)
dSlider.addEventListener('input', sliderUpdate)

pInput.addEventListener('input', inputUpdate)
iInput.addEventListener('input', inputUpdate)
dInput.addEventListener('input', inputUpdate)

function sliderUpdate() {
    if(this === pSlider) {
        pInput.value = this.value;
        pValue = this.value;
    }
    else if(this === iSlider) {
        iInput.value = this.value;
        iValue = this.value;
    }
    else if(this === dSlider) {
        dInput.value = this.value;
        dValue = this.value;
    }
}

function inputUpdate() {
    if(this === pInput) {
        pSlider.value = this.value;
        pValue = this.value;
    }
    else if(this === iInput) {
        iSlider.value = this.value;
        iValue = this.value;
    }
    else if(this === dInput) {
        dSlider.value = this.value;
        dValue = this.value;
    }
}