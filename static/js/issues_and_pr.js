function issues_and_pr_grouping(time_group) {
  const tops = document.querySelector(`.${time_group}`);
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

function issues_time_note_executor() {
  const tops = document.querySelector('.latest-issues');
  const tabs = tops.querySelectorAll('.issues-and-pr-time-note');
  tabs.forEach((tab) => tab.addEventListener('click', (e) => {
    e.preventDefault();
    const activeTab = tops.querySelector('.issues-and-pr-time-note.active');
    const activeList = tops.querySelector(`.latest-issues-and-pr.${activeTab.name}`);
    activeTab.classList.remove('active');
    activeList.classList.add('d-none');

    const newActiveTab = e.target;
    const newActiveList = tops.querySelector(`.latest-issues-and-pr.${newActiveTab.name}`);
    newActiveTab.classList.add('active');
    newActiveList.classList.remove('d-none');
    start(newActiveTab.name)
  }));
}

document.addEventListener('DOMContentLoaded', issues_and_pr_grouping('issues-and-pr-for-week'));
document.addEventListener('DOMContentLoaded', issues_time_note_executor);
