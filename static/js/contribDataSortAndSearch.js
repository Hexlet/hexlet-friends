function renderTableRows() {
  repoRows.forEach((row, i) => {
    row.append(...Object.values(reposData[i]));
  });
}

const inverseOrderNames = {
  '': 'desc',
  asc: 'desc',
  desc: 'asc',
};

function compareNumbers(a, b) {
  return a - b;
}

function compareStrings(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
  }

function sortByColumn({ currentTarget }) {
  const field = currentTarget.id;
  const numComparer = {
    asc: (repo1, repo2) => compareNumbers(repo1[field].innerText, repo2[field].innerText),
    desc: (repo1, repo2) => compareNumbers(repo2[field].innerText, repo1[field].innerText),
  };
  const strComparer = {
    asc: (repo1, repo2) => compareStrings(repo1[field].innerText, repo2[field].innerText),
    desc: (repo1, repo2) => compareStrings(repo2[field].innerText, repo1[field].innerText),
  };
  const comparer = (field === 'repo-name') ? strComparer : numComparer;
  const order = inverseOrderNames[currentTarget.dataset.sorting];
  reposData.sort(comparer[order]);

  // Change the value of the sorting attribute
  headers.forEach((header) => {
    header.dataset.sorting = '';
  });
  currentTarget.dataset.sorting = order;
  renderTableRows();
}

function searchForRepositories({ target }) {
  repoRows.forEach((row) => {
    const repoName = row.querySelector('[data-field="repo-name"]').innerText;
    row.style.display = repoName.includes(target.value) ? '' : 'none';
  });
}

const table = document.getElementById('contrib-details');
const reposData = [];
const repoRows = table.querySelectorAll('.repo-contributions');
repoRows.forEach((row) => {
  const repoData = {};
  const cells = row.children;
  for (const cell of cells) {
    repoData[cell.dataset.field] = cell;
  }
  reposData.push(repoData);
});
const headers = table.querySelectorAll('thead th');
headers.forEach((header) => header.addEventListener('click', sortByColumn));

const searchField = document.getElementById('repo-search-field');
searchField.addEventListener('input', searchForRepositories);
