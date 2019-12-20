// Returns the ISO week of the date.
Date.prototype.getWeek = function() {
   var date = new Date(this.getTime());
   date.setHours(0, 0, 0, 0);
   // Thursday in current week decides the year.
   date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
   // January 4 is always in week 1.
   var week1 = new Date(date.getFullYear(), 0, 4);
   // Adjust to Thursday in week 1 and count number of weeks from date to week1.
   return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                         - 3 + (week1.getDay() + 6) % 7) / 7);
 }
 
 // Returns the four-digit year corresponding to the ISO week of the date.
 Date.prototype.getWeekYear = function() {
   var date = new Date(this.getTime());
   date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
   return date.getFullYear();
 }


 var PopupCalendar = function() {
   self = this, // I need this to not loose the scope of this
   this.selectedMonth = null,
   this.init = function(e) {
       var me = e;
       addListener(e, 'click', function(e) {
           self.form = me;
           self.selectedMonth = null;
           self.render(e);
       });
   },
   
   // Change selected stat of the days in the calendar and update the value of the form
   this.updateForm = function(e) {
       // If using a date time form we want to preserve the time set
       var selectedDateArr = self.form.value.split(' ');
       if (selectedDateArr.length > 1) {
           selectedDateArr[0] = this.attributes['data-date'].value;
           self.form.value = selectedDateArr.join(' ');
       } else {
           self.form.value = this.attributes['data-date'].value;
       }
       var dp = document.getElementById('dp_datepicker');
       var dpSelected = dp.getElementsByClassName('selected');
       if (dpSelected.length === 1) {
           removeClass(dpSelected[0], 'selected');
       }
       addClass(this, 'selected');
       self.destroy();
   },
   
   // Add a click event on each day so that it can change selected stat and update the form when clicked
   this.addEventToDays = function() {
       var dayDivs = document.getElementsByClassName('dpDay');
       var i = 0;
       while (i < dayDivs.length) {
           addListener(dayDivs[i], 'click', self.updateForm);
           i++;
       }
   },
   
   // Add a click event that changes month
   this.addEventChangeMonth = function(e) {
       var el = e;
       // Find the next and previous month
       var prev = document.getElementById('dpPrev');
       addListener(prev, 'click', function() {
           var dateArr = self.selectedMonth.split('-');
           if (parseInt(dateArr[1], 10) === 1) { dateArr[1] = 12; dateArr[0]--; }
           else { dateArr[1]--; }
           self.selectedMonth = dateArr.join('-');
           self.render(el);
           self.render(el);
       });

       var next = document.getElementById('dpNext');
       addListener(next, 'click', function() {
           var dateArr = self.selectedMonth.split('-');
           if (parseInt(dateArr[1], 10) === 12) { dateArr[1] = 1; dateArr[0]++; }
           else { dateArr[1]++; }
           self.selectedMonth = dateArr.join('-');
           self.render(el);
           self.render(el);
       });
   },
 
   this.render = function(e) {
       // Get selected Date We also want the picker to work on time fields 0000-00-00 00:00:00
       var selectedDateArr = e.target.value.split(' ');
       var selectedDate = selectedDateArr[0];
       var selectedDateJS = new Date(selectedDate);
       
       // Get current Date
       var d = new Date();
       var currentDate = d.toLocaleDateString('sv-SE');
       
       // Decide which month to show
       var showDate = self.selectedMonth;
       if (showDate === null) {
           showDate = currentDate;
           if (selectedDate !== '' && selectedDate !== '0000-00-00') {
               showDate = selectedDate;
           }
       }
       self.selectedMonth = showDate;
       
       // Build a list of days for the month to show
       // Get the find the first Monday prior to the first day of this month if the first is not a Monday
       var showDateJS = new Date(showDate);
       var firstDay = showDateJS.getFullYear() + '-' + (showDateJS.getMonth()+1) + '-01';
       var firstDayJS = new Date(firstDay);
       var currDay = firstDayJS.getDay(); // 1 is monday
       var startDayJS = firstDayJS;
       if (firstDayJS.getDay() !== 1) {
           if (firstDayJS.getDay() === 0) {
               currDay = 7;
           }
           // Calculate days to Monday
           var daysUntilMonday = (-currDay + 1);
           // Find the first Monday to display
           startDayJS.setTime(Date.parse(firstDayJS.toLocaleDateString('sv-SE')) + (daysUntilMonday*24*3600*1000));
       }
       var monthArr = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
       var monthHead = '<div id="dpPrev" class="dpNav"><</div><div id="dpMonth">'
                       + showDateJS.getFullYear() + ' ' + monthArr[showDateJS.getMonth()] 
                       + '</div><div id="dpNext" class="dpNav">></div>';
       
       var dayList = '<div class="dpDayCol">Mo</div>'
                   + '<div class="dpDayCol">Tu</div>'
                   + '<div class="dpDayCol">We</div>'
                   + '<div class="dpDayCol">Th</div>'
                   + '<div class="dpDayCol">Fr</div>'
                   + '<div class="dpDayCol">Sa</div>'
                   + '<div class="dpDayCol">Su</div>'
                   ;
       var hide = false;
       for (var i = 0; i < 42; i++) {
           var currMonthStyle = '';
           var today = '';
           if (startDayJS.getMonth() !== showDateJS.getMonth()) {
               currMonthStyle = 'other_month';
           }
           if (startDayJS.toLocaleDateString() === d.toLocaleDateString()) {
               today = 'today';
           }
           var selected = '';
           if (startDayJS.toLocaleDateString() === selectedDateJS.toLocaleDateString()) {
               selected = 'selected';
           }
           if (currMonthStyle !== '' && i === 35) {
               hide = true;
           }
           if (!hide) {
               dayList += '<div class="dpDay ' + currMonthStyle + ' ' + today + ' ' + selected + '" data-date="' + startDayJS.toLocaleDateString('sv-SE') + '">' + startDayJS.getDate() + '</div>';
           }
           startDayJS.setTime(Date.parse(firstDayJS.toLocaleDateString('sv-SE')) + (1*24*3600*1000));
       }
       // Create the frame structure for our component
       var dc = document.getElementById('dpContainer');
       if (dc === null) {
           var dpString = '<div id="dp_datepicker"><div id="dpHead">' + monthHead + '</div><div id="dpBody">' + dayList + '</div></div>';
           // We can not append a string, so we need to create a container element that we can add
           // If we add a string to the document.body.innerHTML all events will be removed
           var elem = document.createElement("div");
           elem.id = 'dpContainer';
           elem.innerHTML = dpString;
           // Add our component to the DOM
           document.body.appendChild(elem);
           var dp = document.getElementById('dp_datepicker');
           // Get the position
           var pos = getPosition(e.target);
           dp.style.top = (pos.y + 22) + 'px';
           dp.style.left = (pos.x - 2) + 'px';

           // Here this is the html element so I need to use self instead to call my methods
           self.addEventToDays();
           // Add month change trigger
           self.addEventChangeMonth(e);
       } else {
           self.destroy();
       }
   },
   // Remove the calender pop up from the DOM
   this.destroy = function() {
       var dc = document.getElementById('dpContainer');
       document.body.removeChild(dc);
   }
};

// Here is how you implement the plug in
var dp = new PopupCalendar;
var calendarObj = document.getElementsByClassName('datepicker');
var i = 0;
while (i < calendarObj.length) {
   dp.init(calendarObj[i]);
   i++;
}