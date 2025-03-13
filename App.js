import React, { useEffect, useState } from "react";

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/users")
      .then((response) => response.json())
      .then((json) => setUsers(json))
      .catch((error) => console.error("Ошибка загрузки:", error));
  }, []);

  return (
    <div>
      <h1>Список пользователей</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.username} ({user.FIO}) - {user.phone}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
