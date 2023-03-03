(function ($) {
  "use strict";
  var event_data = {
    events: [],
  };
  var fechaGlobal = "";
  // Setup the calendar with the current date
  $(document).ready(function () {
    var date = new Date();
    //Eventos de turnos
    let { args } = window.data;
    args = args.replace(/"/g, "'").replace(/'/g, '"');
    var turnos = JSON.parse(args);
    //console.log(turnos);
    event_data = {
      events: turnos,
    };
    var today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({ date: date }, next_year);
    $(".left-button").click({ date: date }, prev_year);
    $(".month").click({ date: date }, month_click);

    $("#add-button").click({ date: date }, new_event);
    // Set current month as active
    $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
    var events = check_events(today, date.getMonth(), date.getFullYear());
    show_events(events, months[date.getMonth()], today);
  });

  // Initialize the calendar by appending the HTML dates
  function init_calendar(date,fake=false) {
    $(".tbody").empty();
    $(".events-container").empty();
    var calendar_days = $(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");
    var today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    var first_day = date.getDay();
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for (var i = 0; i < 35 + first_day; i++) {
      // Since some of the elements will be blank,
      // need to calculate actual date from index
      var day = i - first_day + 1;
      // If it is a sunday, make a new row
      if (i % 7 === 0) {
        calendar_days.append(row);
        row = $("<tr class='table-row'></tr>");
      }
      // if current index isn't a day in this month, make it blank
      if (i < first_day || day > day_count) {
        var curr_date = $("<td class='table-date nil'>" + "</td>");
        row.append(curr_date);
      } else {
        var curr_date = $("<td class='table-date'>" + day + "</td>");
        var events = check_events(day, month, year,fake);
        //console.log(events)
        if (today === day && $(".active-date").length === 0) {
          curr_date.addClass("active-date");
          show_events(events, months[month], day);
        }
        // If this date has any events, style it with .event-date
        if (events.length !== 0) {
          curr_date.addClass("event-date");
        }
        // Set onClick handler for clicking a date
        curr_date.click(
          {
            events: events,
            year: year,
            month: months[month],
            mes: month + 1,
            day: day,
          },
          date_click
        );
        row.append(curr_date);
      }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
  }

  // Get the number of days in a given month/year
  function days_in_month(month, year) {
    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);
  }

  // Event handler for when a date is clicked
  function date_click(event) {
    fechaGlobal = event.data.year + "-" + event.data.mes + "-" + event.data.day;
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    show_events(event.data.events, event.data.month, event.data.day);
  }

  // Event handler for when a month is clicked
  function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    var date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    var new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
  }

  // Event handler for when the year right-button is clicked
  function next_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear() + 1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
  }

  // Event handler for when the year left-button is clicked
  function prev_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear() - 1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
  }

  // Event handler for clicking the new event button
  function new_event(event) {
    //console.log("primero esto")
    // if a date isn't selected then do nothing
    if ($(".active-date").length === 0) return;
    // remove red error input on click
    $("input").click(function () {
      $(this).removeClass("error-input");
    });
    // empty inputs and hide events
    $("#dialog input[type=text]").val("");
    $(".events-container").hide(250);
    $("#dialog").show(250);
    // Event handler for cancel button
    $("#cancel-button").click(function () {
      $("#name").removeClass("error-input");
      $("#doctor").removeClass("error-input");
      $("#dialog").hide(250);
      $(".events-container").show(250);
    });
    // Event handler for ok button
    $("#ok-button")
      .unbind()
      .click({ date: event.data.date }, function () {
        var date = event.data.date;
        // Obtener el día, mes y año de la fecha
        if (!fechaGlobal) {
            fechaGlobal=new Date();
            var dia = fechaGlobal.getDate();
            var mes = fechaGlobal.getMonth() + 1; // Los meses comienzan en 0, por lo que se debe sumar 1
            var anio = fechaGlobal.getFullYear();
          // Formatear la fecha en formato  2023-02-28
            fechaGlobal = anio + "-" + mes + "-" + dia;
        }
        var place = $("#name").val().trim();
        var doctor = parseInt($("#doctor").val().trim());
        var day = parseInt($(".active-date").html());
        const csrftoken = getCookie("csrftoken");
        // Basic form validation
        if (place.length === 0) {
          $("#name").addClass("error-input");
        } else if (isNaN(doctor)) {
          $("#doctor").addClass("error-input");
        } else {
          $("#dialog").hide(250);

          $.ajax({
            url: "../../dashboard/turnomodal/",
            headers: { "X-CSRFToken": csrftoken },
            mode: "same-origin",
            method: "POST",
            data: {
              date: fechaGlobal,
              place: place,
              doctor: doctor,
            },
            success: function (respuesta) {
              // Manejar la respuesta de la llamada AJAX
              console.log(respuesta);
              //location.reload();
            },
          });
          console.log("enviando turno");
          //console.log(fechaGlobal);
          new_event_json(place, $('#doctor option:selected').text(), fechaGlobal, day);
          date.setDate(day);
          init_calendar(date,true);
        }
      });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Adds a json event to event_data
  function new_event_json(place, doctor, date, day) {
    
    var event = {
        fields:{
            date: date,
            place:place,
            doctor: doctor
        },
        day: day,
    };
    event_data["events"].push(event);
  }

  // Display all events of the selected date in card views
  function show_events(events, month, day) {
    // Clear the dates container
    $(".events-container").empty();
    $(".events-container").show(250);
    //console.log(event_data["events"]);
    // If there are no events for this date, notify the user
    if (events.length === 0) {
      var event_card = $("<div class='event-card'></div>");
      var event_name = $(
        "<div class='event-name'>No hay turnos registrados para " +
          month +
          " " +
          day +
          ".</div>"
      );
      $(event_card).css({ "border-left": "10px solid #FF1744" });
      $(event_card).append(event_name);
      $(".events-container").append(event_card);
    } else {
      // Go through and add each event as a card to the events container
      for (var i = 0; i < events.length; i++) {
        var event_card = $("<div class='event-card'></div>");
        var event_name = $(
          "<div class='event-name text-white fs-5'> ** Lugar: " +
            events[i]["fields"]["place"] +
            " - Doctor: " +
            events[i]["fields"]["doctor"] +
            "</div>"
        );

        $(event_card).append(event_name);
        $(".events-container").append(event_card);
      }
    }
  }

  // Checks if a specific date has any events
  function check_events(day, month, year,fake=false) {
    var events = [];
    //console.log(event_data)
    //console.log(day,month,year)
    for (var i = 0; i < event_data["events"].length; i++) {
      var event = event_data["events"][i];
      let fecha = new Date(event["fields"]["date"]);
      let fechaComparar=fake?fecha:fechaPeru(fecha,event);
      let dia=fechaComparar.getDate() ;
      //console.log(dia)
      if (
        dia === day &&
        fechaComparar.getMonth() === month &&
        fechaComparar.getFullYear() === year
      ) {
        events.push(event);
      }
    }

    return events;
  }

  function fechaPeru(fecha,event) {
    const timezoneOffset = fecha.getTimezoneOffset() / 60;
    const timezoneOffsetString = `-0${timezoneOffset}:00`.slice(-6);
    const isoDateWithTimezone = `${event["fields"]["date"].slice(0, -1)}${timezoneOffsetString}`;
    let fechaValida=new Date(isoDateWithTimezone)
    return fechaValida
  }


  // Given data for events in JSON format

  const months = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];
})(jQuery);
