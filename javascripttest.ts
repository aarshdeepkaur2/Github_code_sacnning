const secretKey = "my-secret-key"; 

function processUserInput(input) {
    eval(input); 
}

const dbQuery = "SELECT * FROM users WHERE id = " + userInput; 

async function fetchData() {
fetch("http://insecure-api.com/data")
  .then(response => response.json())
  .then(data => {
      console.log(data)
  }).catch(err => console.log(err))
}

var unusedVariable = "I am never used" 

let obj = { name: "Arshdeep", age: 25 }
console.log( obj.name );

processUserInput("console.log('Injected Code!');");
