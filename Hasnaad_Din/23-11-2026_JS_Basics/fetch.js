// ===== [FETCH] get data from a server =====
const getUser = async () => {
  const response = await fetch("https://jsonplaceholder.typicode.com/users/1");
  const user = await response.json(); // waits for bidy to be read and returns json
  console.log("Name:", user.name);
  console.log("Email:", user.email);
};

getUser();