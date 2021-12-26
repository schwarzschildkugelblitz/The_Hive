// const totalTimeBox = document.querySelector('#time-box')
// const totalCountBox = document.querySelector('#count-box')

// const startBtn = document.querySelector('#start-btn')
// const stopBtn = document.querySelector('#stop-btn')
// const resetBtn = document.querySelector('#reset-btn')

// const pSlider = document.querySelector('#p-slider')
// const iSlider = document.querySelector('#i-slider')
// const dSlider = document.querySelector('#d-slider')
// const pInput = document.querySelector('#p-input')
// const iInput = document.querySelector('#i-input')
// const dInput = document.querySelector('#d-input')

// let pValue = parseInt(40)
// let iValue = parseInt(40)
// let dValue = parseInt(40)
// // adding chart varible 
// let angle_time_graph = document.getElementById('angle_time_graph').getcontext('2d')

// pSlider.addEventListener('input', sliderUpdate)
// iSlider.addEventListener('input', sliderUpdate)
// dSlider.addEventListener('input', sliderUpdate)

// pInput.addEventListener('input', inputUpdate)
// iInput.addEventListener('input', inputUpdate)
// dInput.addEventListener('input', inputUpdate)

// function sliderUpdate() {
//     if(this === pSlider) {
//         pInput.value = this.value;
//         pValue = this.value;
//     }
//     else if(this === iSlider) {
//         iInput.value = this.value;
//         iValue = this.value;
//     }
//     else if(this === dSlider) {
//         dInput.value = this.value;
//         dValue = this.value;
//     }
// }

// function inputUpdate() {
//     if(this === pInput) {
//         pSlider.value = this.value;
//         pValue = this.value;
//     }
//     else if(this === iInput) {
//         iSlider.value = this.value;
//         iValue = this.value;
//     }
//     else if(this === dInput) {
//         dSlider.value = this.value;
//         dValue = this.value;
//     }
// }
new Chart(document.getElementById("angle_time_graph"), {
    type: 'line',
    data: {
      labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
      datasets: [ { 
          data: [6,3,2,2,7,2,8,1,3,4],
          label: "North America",
          borderColor: "#c45850",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'World population per region (in millions)'
      }
    }
  });

  new Chart(document.getElementById("idk_time_graph"), {
    type: 'line',
    data: {
      labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
      datasets: [{ 
          data: [86,11,10,10,10,11,13,22,78,24,37, 78, 90 ,99],
          label: "Africa",
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'World population per region (in millions)'
      }
    }
  });