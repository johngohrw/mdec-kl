console.log('index js!')

window.onscroll = function (e) {
    console.log(window.scrollY); // Value of scroll Y in px
    if (window.scrollY >= 100){
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