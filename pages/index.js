   import { useState } from 'react';
   import ImageUploader from '../components/imageUpload'
   import React from 'react';





   export default function HomePage() {
     const [message, setMessage] = useState('');
     const handleClick = async (e) => {
        const response = await fetch('/api/retrieve-image', {
        method: 'POST',
        body: formData,
      });
     };


     return (
       <div>
       <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}> <p style={{ fontSize: '24px' }}> Protect your artwork from Web Scrapers </p> </div>
       <ImageUploader/>
         
       </div>
     );
   }

