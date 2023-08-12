document.addEventListener('DOMContentLoaded', function() {
	const email = prompt('Please enter your email');
	const imgUrl = localStorage.getItem(email);
  
	if (imgUrl) {
	  const img = document.createElement('img');
	  img.src = imgUrl;
	  imgArea.appendChild(img);
	  imgArea.classList.add('active');
	}
  });

const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');

selectImage.addEventListener('click', function() {
  inputFile.click();
});

inputFile.addEventListener('change', function() {
  const image = this.files[0];
  if (image.size < 2000000) {
    const reader = new FileReader();
    reader.onload = () => {
      const allImg = imgArea.querySelectorAll('img');
      allImg.forEach(item => item.remove());
      const imgUrl = reader.result;
      const img = document.createElement('img');
      img.src = imgUrl;
      imgArea.appendChild(img);
      imgArea.classList.add('active');

      const email = prompt('Please enter your email');
      localStorage.setItem(email, imgUrl);
    };
    reader.readAsDataURL(image);
  } else {
    alert('Image size more than 2MB');
  }
});