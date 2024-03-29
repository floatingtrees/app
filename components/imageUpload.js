import { useState } from 'react';
import TextInput from './text_box';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [message, setMessage] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const [oldCategory, setOldCategory] = useState('unknown');
  const [newCategory, setNewCategory] = useState('unknown');
  const [desiredClass, setDesiredClass] = useState('');


  const refreshText = (e) => {
    setDesiredClass(e.target.value);
  }

  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  const uploadImage = async (e) => {
    e.preventDefault();
    if (!selectedImage) {
      alert('Please select an image.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response2 = await fetch('/api/send-classes', {
        method: 'POST',
        body: desiredClass,
      });
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        setMessage("Success");
        const data = await response.json();
        setNewCategory(data.new_category)
        setOldCategory(data.old_category)
        const image = `data:image/jpeg;base64,${data.image}`
        setImageSrc(image)
      } else {
        alert('Image upload failed.');
      }
    } catch (error) {
      console.error('Error uploading the image:', error);
      alert('Error uploading image.');
    }

  };

  return (
    <form onSubmit={uploadImage}>
    <div style={{margin: '30px', display: 'flex',  justifyContent:'center', alignItems:'center'}}>

      <input type='file' onChange={handleImageChange} accept='image/*' />
      <button type='submit'>Upload Image</button>
      
    </div>
    <div style={{margin: '30px', display: 'flex',  justifyContent:'center', alignItems:'center'}}>
     <TextInput onChange={desiredClass, refreshText}/> 
     </div>


    <div style={{margin: '50px', display: 'flex',  justifyContent:'center', alignItems:'center'}}>
      <img src={imageSrc} alt="Fetched from Server"/>
    </div>
    <div style={{margin: '10px', display: 'flex',  justifyContent:'center', alignItems:'center'}}>
    <p style={{ marginRight: '20px', display: 'inline-block' }}> Previous: {oldCategory}   </p> 
    <p style={{ marginLeft: '20px', display: 'inline-block' }}> Now: {newCategory} </p>
    </div>
     
    </form>
    

  );
};

export default ImageUploader;
