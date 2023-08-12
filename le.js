const levelGrid = document.getElementById('level-grid');

// Generate the level grid dynamically
for (let row = 0; row < 7; row++) {
  for (let col = 0; col < 4; col++) {
    const tile = document.createElement('div');
    tile.classList.add('tile');
    tile.setAttribute('data-row', row);
    tile.setAttribute('data-col', col);
    
  }
}



const lessonContainer = document.getElementById('lesson-container');


// The lessons array
const lessons = [
  {
    title: 'أ',locked: false 
  },
  {
    title:'ب',locked: true
  },
  {
    title: 'ت',locked: true
    
  },{
    title: 'ث',locked: true
  },{
    title: 'ج',locked: true
  },{
    title: 'ح',locked: true
  },{
    title: 'خ',locked: true
  },{
    title: 'د',locked: true
  },{
    title: 'ذ',locked: true
  },{
    title: 'ر',locked: true
  },{
    title: 'ز',locked: true
  },{
    title: 'س',locked: true
  },{
    title: 'ش',locked: true
  },{
    title: 'ص',locked: true
  },{
    title: 'ض',locked: true
  },{
    title: 'ط',locked: true
  },{
    title: 'ظ',locked: true
  },{
    title: 'ع',locked: true
  },{
    title: 'غ',locked: true
  },{
    title: 'ف',locked: true
  },{
    title: 'ق',locked: true
  },{
    title: 'ك',locked: true
  },{
    title: 'ل',locked: true
  },{
    title: 'م',locked: true
  },{
    title: 'ن',locked: true
  },{
    title: 'ه',locked: true
  },{
    title: 'و',locked: true
  },{
    title: 'ى',locked: true
  },
];
function updateLessonStatus(index) {
  if (index < lessons.length - 1) {
    lessons[index + 1].locked = false;
  }
}
function completeLesson(index) {
  updateLessonStatus(index);
  // Update the UI to reflect the new lesson status
}

