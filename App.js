// frontend/src/App.js
import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  // Делаем запрос к API при загрузке компонента
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data')  // Запрос к backend
      .then(response => response.json())
      .then(data => setData(data))  // Обновляем состояние данными из ответа
      .catch(error => console.error('Error fetching data:', error));
  }, []);  // Пустой массив, чтобы запрос выполнился только при монтировании компонента

  return (
    <div className="App">
      <h1>Данные с сервера:</h1>
      <ul>
        {data.map(item => (
          <li key={item.id}>
            <strong>{item.name}</strong>: {item.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
