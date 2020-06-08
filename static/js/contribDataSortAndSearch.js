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

function getComparer(type) {
  const typesToFunctions = {
    str: compareStrings,
    num: compareNumbers
  };
  return (direction) => {
    const directionsToFunctions = {
      asc: (field) => (obj1, obj2) => typesToFunctions[type](obj1[field], obj2[field]),
      desc: (field) => (obj1, obj2) => typesToFunctions[type](obj2[field], obj1[field]),
    };
    return directionsToFunctions[direction];
  };
}

function renderTableRow(repo) {
  const tr = document.createElement('tr');
  tr.classList.add('repo-contributions');
  tr.innerHTML = (
    `<tr class="repo-contributions">
      <td data-field="repo-name"><a href="${repo['url']}">${repo['repo-name']}</a></th>
      <td data-field="cit">${repo['cit']}</td>
      <td data-field="cit-add">${repo['cit-add']}</td>
      <td data-field="cit-del">${repo['cit-del']}</td>
      <td data-field="pr">${repo['pr']}</td>
      <td data-field="iss">${repo['iss']}</td>
      <td data-field="cnt">${repo['cnt']}</td>
    </tr>`
  );
  return tr;
}

function renderRepos(tbody, state) {
  tbody.innerHTML = '';
  const sortedColumn = document.querySelector('#contrib-details th:not([data-sorting=""])');
  sortedColumn.dataset.sorting = '';
  const newSortedColumn = document.getElementById(state.order.by);
  newSortedColumn.dataset.sorting = state.order.direction;
  state.filter.repos.forEach((repo) => tbody.appendChild(renderTableRow(repo)));
}

function renderFilteredRepos(tbody, state) {
  tbody.innerHTML = '';
  state.filter.repos.forEach((repo) => tbody.appendChild(renderTableRow(repo)));
}

function getData() {
  const reposData = [];
  const repoRows = document.querySelectorAll('#contrib-details .repo-contributions');
  repoRows.forEach((row) => {
    const repoData = {};
    repoData['url'] = row.querySelector('a').href;
    const cells = row.children;
    for (const cell of cells) {
      repoData[cell.dataset.field] = cell.innerText;
    }
    reposData.push(repoData);
  });
  return reposData;
}

function start() {
  const data = getData();
  const state = {
    data,
    order: {
      by: 'repo-name',
      direction: 'asc',
    },
    filter: {
      value: '',
      repos: data,
    },
  };

  const tbody = document.querySelector('#contrib-details tbody');

  const headers = document.querySelectorAll('#contrib-details th');
  headers.forEach((header) => header.addEventListener('click', ({ currentTarget }) => {
    state.order = {
      by: currentTarget.id,
      direction: inverseOrderNames[currentTarget.dataset.sorting],
    };
    const { by, direction } = state.order;
    const type = (by === 'repo-name') ? 'str' : 'num';
    const comparer = getComparer(type)(direction)(by);
    state.filter.repos.sort(comparer);
    renderRepos(tbody, state);
  }));

  const searchField = document.getElementById('repo-search-field');
  searchField.addEventListener('input', ({ target }) => {
    state.filter.value = target.value;
    state.filter.repos = state.data.filter((repo) => repo['repo-name'].includes(state.filter.value));
    renderFilteredRepos(tbody, state);
  });
}

document.addEventListener('DOMContentLoaded', start);
