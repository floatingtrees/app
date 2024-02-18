   import { useState } from 'react';

   export default function HomePage() {
     const [message, setMessage] = useState('');

     const fetchData = async () => {
       try {
         // Make sure this URL matches your Flask server's route
         const response = await fetch('/api/data', {
          method: "GET", // or 'PUT'
          headers: {
            "Content-Type": "application/json",
          },
        });
         const data = await response.json();
         setMessage(data.message);
       } catch (error) {
         console.error('Error fetching data: ', error);
         setMessage('Error fetching data. Make sure the Flask server is running.');
       }
     };

     return (
       <div>
         <button onClick={fetchData}>Fetch Data from Flask</button>
         <p>{message}</p>
       </div>
     );
   }