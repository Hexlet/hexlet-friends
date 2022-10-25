function start(time_note) {
  const tops = document.querySelector(`.${time_note}`);
  const tabs = tops.querySelectorAll('.nav-link');
  tabs.forEach((tab) => tab.addEventListener('click', (e) => {
    e.preventDefault();
    const activeTab = tops.querySelector('.nav-link.active');
    const activeList = tops.querySelector(`.list-group.${activeTab.name}`);
    activeTab.classList.remove('active');
    activeList.classList.add('d-none');

    const newActiveTab = e.target;
    const newActiveList = tops.querySelector(`.list-group.${newActiveTab.name}`);
    newActiveTab.classList.add('active');
    newActiveList.classList.remove('d-none');
  }));
}


function time_note() {
  const tops = document.querySelector('.top-10-items');
  const tabs = tops.querySelectorAll('.time-note');
  tabs.forEach((tab) => tab.addEventListener('click', (e) => {
    e.preventDefault();
    const activeTab = tops.querySelector('.time-note.active');
    const activeList = tops.querySelector(`.top-10-of-time.${activeTab.name}`);
    activeTab.classList.remove('active');
    activeList.classList.add('d-none');

    const newActiveTab = e.target;
    const newActiveList = tops.querySelector(`.top-10-of-time.${newActiveTab.name}`);
    newActiveTab.classList.add('active');
    newActiveList.classList.remove('d-none');
    start(newActiveTab.name)
  }));
}


document.addEventListener('DOMContentLoaded', start('top-week'));
document.addEventListener('DOMContentLoaded', time_note);
