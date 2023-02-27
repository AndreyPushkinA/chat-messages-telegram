document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("multiply").addEventListener("click", function () {
      var channelName = document.getElementById("channelName").value;
      var startDate = document.getElementById("startDate").value;
      var endDate = document.getElementById("endDate").value;
      document.getElementById("result").textContent = "Channel " + channelName + " between " + startDate + " and " + endDate;
    });
  });