function updateTimer(deadline) {
  function changeTimezone(date, ianatz) {
    // suppose the date is 12:00 UTC
    var invdate = new Date(
      date.toLocaleString("en-US", {
        timeZone: ianatz,
      })
    );

    // then invdate will be 07:00 in Toronto
    // and the diff is 5 hours
    var diff = date.getTime() - invdate.getTime();

    // so 12:00 in Toronto is 17:00 UTC
    return new Date(date.getTime() - diff); // needs to substract
  }
  var here = new Date();
  var there = changeTimezone(here, "America/Los_Angeles");
  var time = deadline - there;

  let days = Math.floor(time / (1000 * 60 * 60 * 24));
  let hours = Math.floor((time / (1000 * 60 * 60)) % 24);
  let minutes = Math.floor((time / 1000 / 60) % 60);
  let seconds = Math.floor((time / 1000) % 60);
  if (hours <= 0 && days <= 0 && minutes <= 0 && seconds <= 0) {
    document.getElementById("geeks-countdown").style.display = "none";
    document.getElementById("maincontainer").style.display = "block";
  }
  return {
    days: Math.floor(time / (1000 * 60 * 60 * 24)),
    hours: Math.floor((time / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((time / 1000 / 60) % 60),
    seconds: Math.floor((time / 1000) % 60),
    total: time,
  };
}

function animateClock(span) {
  span.className = "turn";
  setTimeout(function () {
    span.className = "";
  }, 700);
}

function startTimer(id, deadline) {
  var timerInterval = setInterval(function () {
    var clock = document.getElementById(id);
    var timer = updateTimer(deadline);

    clock.innerHTML =
      "<span>" +
      timer.days +
      "</span>" +
      "<span>" +
      timer.hours +
      "</span>" +
      "<span >" +
      timer.minutes +
      "</span>" +
      "<span  >" +
      timer.seconds +
      "</span>";

    //animations
    var spans = clock.getElementsByTagName("span");
    animateClock(spans[3]);
    if (timer.seconds == 59) animateClock(spans[2]);
    if (timer.minutes == 59 && timer.seconds == 59) animateClock(spans[1]);
    if (timer.hours == 23 && timer.minutes == 59 && timer.seconds == 59)
      animateClock(spans[0]);

    //check for end of timer
    if (timer.total < 1) {
      clearInterval(timerInterval);
      clock.innerHTML =
        "<span>0</span><span>0</span><span>0</span><span>0</span>";
    }
  }, 1000);
}

window.onload = function () {
  let backendDate = document.getElementById("time").innerHTML;
  var deadline = new Date(backendDate); // deadline - end time of countdown
  console.log(deadline, "time");

  function changeTimezone(date, ianatz) {
    // suppose the date is 12:00 UTC
    var invdate = new Date(
      date.toLocaleString("en-US", {
        timeZone: ianatz,
      })
    );

    // then invdate will be 07:00 in Toronto
    // and the diff is 5 hours
    var diff = date.getTime() - invdate.getTime();

    // so 12:00 in Toronto is 17:00 UTC
    return new Date(date.getTime() - diff); // needs to substract
  }

  // E.g.
  var here = new Date();
  var there = changeTimezone(here, "America/Los_Angeles");
  var time = deadline - there;

  console.log(time, "time");
  // console.log(`Here: ${here.toString()}\nToronto: ${there}`);

  let days = Math.floor(time / (1000 * 60 * 60 * 24));
  let hours = Math.floor((time / (1000 * 60 * 60)) % 24);
  let minutes = Math.floor((time / 1000 / 60) % 60);
  let seconds = Math.floor((time / 1000) % 60);
  let total = time;

  if (hours <= 0 && days <= 0 && minutes <= 0 && seconds <= 0) {
    document.getElementById("geeks-countdown").style.display = "none";
  } else {
    document.getElementById("maincontainer").style.display = "none";
    startTimer("clock", deadline);
  }
};
