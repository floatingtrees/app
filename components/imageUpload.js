import { useState } from 'react';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [message, setMessage] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const [oldCategory, setOldCategory] = useState('');
  const [newCategory, setNewCategory] = useState('');

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
    <div style={{margin: '50px', display: 'flex',  justifyContent:'center', alignItems:'center'}}>
      <img src={imageSrc} alt="Fetched from Server"/>
    </div>
    </form>
    

  );
};

export default ImageUploader;
