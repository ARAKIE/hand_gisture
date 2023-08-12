class StrokeList {
  constructor() {
    this.stroke_list = [[]];
  }

  add_pt(pt) {
    this.stroke_list.at(-1).push(pt);
  }

  clear() {
    this.stroke_list = [[]];
  }

  erase(erase_pos, radius) {
    this.filter((index, pt) => Point.distance(erase_pos, pt) > radius);
  }

  new_stroke() {
    if (!this.stroke_list.length || this.stroke_list.at(-1).length) {
      this.stroke_list.push([]);
    }
  }

  draw(context) {
    context.lineJoin = "round";
    context.strokeStyle = "white";
   
    context.shadowBlur = 10;
    context.lineWidth = 5;
    for (const stroke of this.stroke_list) {
      if (stroke.length) {
        context.beginPath();
        context.moveTo(stroke[0].x, stroke[0].y);
        for (const pt of stroke.slice(1)) {
          context.lineTo(pt.x, pt.y);
        }
        context.stroke();
      }
    }
  }

  download() {
    return new Blob([JSON.stringify(this.stroke_list.flat(), null, 2)], {
      type: "text/plain",
    });
  }

  filter(criterion) {
    /*
        criterion is a function (index,element) => bool which tells wether element at a given index
        should be kept 
        */
    let old_stroke_list = this.stroke_list.slice();
    this.stroke_list = [[]];
    const n = old_stroke_list.length;
    let count = 0;
    for (let k = 0; k < n; k++) {
      let n_k = old_stroke_list[k].length;
      for (let i = 0; i < n_k; i++) {
        if (criterion(count, old_stroke_list[k][i])) {
          this.add_pt(old_stroke_list[k][i]);
        } else {
          this.new_stroke();
        }
        count++;
      }
      this.new_stroke();
    }
    this.new_stroke();
  }

  // Use a DL on the sequence to predict wether the user wanted to draw or not
  async  predict() {
    const canvas = document.getElementById('croppedCanvas');
    const context = canvas.getContext('2d');
  
    // Define the crop dimensions
    const cropWidth = 450;
    const cropHeight = 300;
    const cropX = (canvas.width - cropWidth) / 2;
    const cropY = (canvas.height - cropHeight) / 2;
  
    const smallCanvas = document.createElement('canvas');
    smallCanvas.width = 32;
    smallCanvas.height = 32;
    const smallContext = smallCanvas.getContext('2d', { willReadFrequently: true });
    smallContext.drawImage(canvas, cropX, cropY, cropWidth, cropHeight, 0, 0, 32, 32);
  
    // Convert the image to grayscale
    const imageData = smallContext.getImageData(0, 0, 32, 32);
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
      const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
      data[i] = avg;
      data[i + 1] = avg;
      data[i + 2] = avg;
    }
  
    // Convert the grayscale image to base64 data URL
    const base64 = smallCanvas.toDataURL();
  
    try {
      // Send the image data to the server using fetch
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_data: base64 })
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Get the prediction result from the server
      const result = await response.json();
  
      // Display the prediction result text on the webpage
      const predictionText = document.getElementById('predictionText');
if (result.prediction[0] > 0.5) {
        predictionText.innerHTML = `congratulations 👏`;
        predictionText.classList.add('balloons-effect');
      
        // Add confetti
        for (let i = 0; i < 100; i++) {
          const confetti = document.createElement('div');
          confetti.classList.add('confetti');
          confetti.style.left = Math.random() * 100 + '%';
          confetti.style.animationDelay = Math.random() * 2 + 's';
          document.getElementById('confetti').appendChild(confetti);
        }
      
        // Add balloons
        for (let i = 0; i < 20; i++) {
          const balloon = document.createElement('div');
          balloon.classList.add('balloon');
          balloon.style.left = Math.random() * 100 + '%';
          balloon.style.animationDelay = Math.random() * 2 + 's';
          document.getElementById('balloons').appendChild(balloon);
        }
      
        setTimeout(() => {
          predictionText.classList.remove('balloons-effect');
      
          // Remove confetti
          const confettiContainer = document.getElementById('confetti');
          while (confettiContainer.firstChild) {
            confettiContainer.removeChild(confettiContainer.firstChild);
          }
      
          // Remove balloons
          const balloonContainer = document.getElementById('balloons');
          while (balloonContainer.firstChild) {
            balloonContainer.removeChild(balloonContainer.firstChild);
          }
        }, 3000);
      } else {
        predictionText.innerHTML = `&#x1F61E; False answer`;
        predictionText.classList.add('False');
        setTimeout(() => {
          predictionText.classList.remove('False');
        }, 3000);
      }


    } catch (error) {
      console.error('Error:', error);
      // Handle the error here
    }
  }
  
  
  
  
  
}

// Takes an array of 2D coordinates and returns an array of 6D values (vx,vy,v,ax,ay,a)
function transformData(data) {
  let new_data = [[0, 0, 0, 0, 0, 0]];
  let n = data.length;
  for (let k = 1; k < n; k++) {
    vx = data[k][0] - data[k - 1][0];
    vy = data[k][1] - data[k - 1][1];
    v = Math.hypot(vx, vy);
    ax = vx - new_data.at(-1)[0];
    ay = vy - new_data.at(-1)[1];
    a = Math.hypot(ax, ay);
    new_data.push([vx, vy, v, ax, ay, a]);
  }
  return new_data;
}
