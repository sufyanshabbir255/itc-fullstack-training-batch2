// weather.js - type a city, click the button, show the weather on the page

// ===== [FETCH] weather for a city =====
const getWeather = async (city) => {
  // 1. City name -> latitude and longitude
  const geoResponse = await fetch("https://geocoding-api.open-meteo.com/v1/search?name=" + city + "&count=1");
  
  console.log(geoResponse);
  
  const geoData = await geoResponse.json();
  const place = geoData.results[0];

  

  // 2. Latitude and longitude -> current weather
  const weatherResponse = await fetch(
    "https://api.open-meteo.com/v1/forecast?latitude=" + place.latitude + "&longitude=" + place.longitude + "&current=temperature_2m,wind_speed_10m"
  );
  console.log(weatherResponse);
  const weatherData = await weatherResponse.json();

  // 3. Show it on the page
  const result = document.getElementById("result");
  result.textContent = place.name + ", " + place.country + ": " +
    weatherData.current.temperature_2m + " °C, wind " +
    weatherData.current.wind_speed_10m + " km/h";
};

// ===== [BUTTON CLICK] run getWeather with what was typed =====
const button = document.getElementById("search-btn");
button.addEventListener("click", () => {
  const city = document.getElementById("city").value;
  getWeather(city);
});