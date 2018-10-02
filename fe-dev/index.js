console.log('index js!')

window.onscroll = function (e) {
    // console.log(window.scrollY); // Value of scroll Y in px
    if (window.scrollY >= 60){
        if (!$('.arduino-nav').hasClass('collapsed')) {
            $('.arduino-nav').addClass('collapsed')
            $('.branding-text').addClass('fucking-hidden')
            setTimeout(()=>{
                $('.larger-logo').addClass('fucking-hidden')
                $('.smaller-logo').removeClass('fucking-hidden')
            },500)
        }
    } else {
        if ($('.arduino-nav').hasClass('collapsed')) {
            $('.arduino-nav').removeClass('collapsed')
            $('.smaller-logo').addClass('fucking-hidden')
            $('.larger-logo').removeClass('fucking-hidden')
            setTimeout(()=>{
                $('.branding-text').removeClass('fucking-hidden')
            },200)
        }
    }
};

document.addEventListener("DOMContentLoaded", function(event) {
    console.log("Document ready!");

    
    // number of cars rn
    cars = 150
    val = cars
    $('#data-number-of-cars').text(val)

    // avg light intensity
    val = 70
    new Chartist.Pie('#chart-avg-light-intensity', {
        series: [val]
      }, {
        donut: true,
        donutWidth: 20,
        startAngle: 0,
        total: 100,
        showLabel: false
      });
    $('#data-avg-light-intensity').text(val + 'kWh')
    
    // available bays
    totalbays = 321
    available = totalbays - cars
    new Chartist.Pie('#chart-available-bays', {
        series: [cars]
      }, {
        donut: true,
        donutWidth: 20,
        startAngle: 0,
        total: totalbays,
        showLabel: false
      });
    $('#data-available-bays').text( available + ' / ' + totalbays)

    // daily green energy used
    val = 14
    new Chartist.Pie('#chart-daily-green-energy-used', {
        series: [val]
      }, {
        donut: true,
        donutWidth: 20,
        startAngle: 0,
        total: 100,
        showLabel: false
      });
    $('#data-daily-green-energy-used').text( val + ' kWh')

    // daily green energy used
    val = 42
    new Chartist.Pie('#chart-daily-brown-energy-used', {
        series: [val]
      }, {
        donut: true,
        donutWidth: 20,
        startAngle: 0,
        total: 100,
        showLabel: false
      });
    $('#data-daily-brown-energy-used').text( val + ' kWh')

    // daily chart
    const updatedailystats = () => {
        console.log('mouseup')
        setTimeout(() => {
            var data = {
                labels: ['Floor B1', 'Floor B2', 'Floor B3', 'Floor B4', 'Floor B5'],
                series: [
                [30, 21, 24, 11, 10]
                ]
            };
            
            var options = {
                seriesBarDistance: 20
            };
            
            var responsiveOptions = [
                ['screen and (max-width: 640px)', {
                seriesBarDistance: 5,
                axisX: {
                    labelInterpolationFnc: function (value) {
                    return value[0];
                    }
                }
                }]
            ];
            new Chartist.Bar('.chart-daily-parking-bays', data, options, responsiveOptions);
        })

    }
    $('.statsdaily').on('click', updatedailystats);
    $('#statistics').on('click', updatedailystats);

    // weekly chart
    const weeklydata = {
        labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        series: [
          [1, 12, 9, 7, 8, 5, 4],
          [2, 2, 1, 3.5, 7, 3, 2],
          [3, 1, 3, 4, 5, 6, 9]
        ]
      }

    $('.statsweekly').on('click', () => {
        setTimeout(() => {
            new Chartist.Line('.chart-weekly-energy-line', weeklydata, {
                fullWidth: true,
                chartPadding: {
                  right: 40
                }
            });
        }, 20)
        
    });

    setTimeout(() => {
        new Chartist.Line('.chart-weekly-energy-line-dashboard', weeklydata, {
            fullWidth: true,
            chartPadding: {
              right: 40
            }
        });
    }, 20)

    // monthly chart
    $('.statsmonthly').on('click', () => {
        setTimeout(() => {
            new Chartist.Line('.chart-monthly-energy-line', {
                labels: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'],
                series: [
                  [1, 12, 9, 7, 8, 5, 4,2, 2, 1, 3.5, 7, 3, 2,9,3,1,9,13,3,6,12,3,1,2,5,7,9,2,1],
                  [2, 2, 1, 3.5, 7, 3, 2, 3.5, 7, 3,2, 2, 12, 9, 7, 8, 5, 4,2,2,9,1,5,7,3,5,8,3,4,2],
                  [3, 1, 3, 4, 5, 6, 9,2, 2, 1,2,9,12,13,14,3,6,8,3,5,12,10,9,3,5,7,2,5,1,9]
                ]
              }, {
                fullWidth: true,
                chartPadding: {
                  right: 40
                }
              });
        }, 20)
        
    });

    setInterval(()=> {
        console.log('lightwaaaaaaaaave')
        lightWave()
    }, 10000)

});


const lightWave = () => {
    let i = 1
    const lightWaveAux = () => {
        if (i < 21) {
            let id = 'lb' + i;
            toggleLights(id)
        } else {
            clearMe()
            console.log('cleared!')
        }
        i += 1
    }
    const clearMe = () => {
        clearInterval(damnlights)
    }
    const damnlights = setInterval(lightWaveAux, 300)
}



const toggleLights = (id='none') => {
    if (id == 'none'){
        $('.lightson').addClass('templights')
        $('.lightson').removeClass('lightson')
        $('.lightsoff').addClass('lightson')
        $('.lightsoff').removeClass('lightsoff')
        $('.templights').addClass('lightsoff')
        $('.templights').removeClass('templights')
    } else {
        let lol1 = '.lightson#' + id;
        let lol2 = '.lightsoff#' + id;
        let lol3 = '.templights#' + id;
        $(lol1).addClass('templights')
        $(lol1).removeClass('lightson')
        $(lol2).addClass('lightson')
        $(lol2).removeClass('lightsoff')
        $(lol3).addClass('lightsoff')
        $(lol3).removeClass('templights')
    }
}




