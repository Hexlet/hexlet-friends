function start() {
  const tops = document.querySelector('.top-10');
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

document.addEventListener('DOMContentLoaded', start);
