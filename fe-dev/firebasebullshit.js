
console.log('firebase bullshit!');

setInterval( _ => updateData(), 10000);

var carEventsRef = firebase.database().ref("/car/carEvents");

const updateData = () => {
    console.log('updatedata!')

    carEventsRef.once('value', (snapshot) => {
        var eventJSON = snapshot.toJSON()
        console.log(eventJSON)
        var keys = Object.keys(eventJSON)
        var eventList = []
        $('#the-actual-log').empty()
        for (let i = keys.length - 1; i >= 0 ; i--){
            // console.log(eventJSON[keys[i]])
            eventList.push(eventJSON[keys[i]])

            var log = eventJSON[keys[i]].Log
            var date = eventJSON[keys[i]].Date
            var time = eventJSON[keys[i]].Time
            var carplate = eventJSON[keys[i]].Carplate
            var event = eventJSON[keys[i]].Event

            tableRowHtmlString = `<tr> <td>${log}</td> <td>${date}</td> <td>${time}</td> <td>${carplate}</td> <td>${event}</td> </tr>`
            // console.log(tableRowHtmlString)
            if (event !== 'Motion'){
                $( "#the-actual-log" ).append( tableRowHtmlString );
            }
        }
        console.log('events fetched')
      })
}

document.addEventListener("DOMContentLoaded", function(event) {

    $('.eventlog').bind('mouseover', () => {
        setTimeout(()=>{
            updateData()
        },200)
    });

})
