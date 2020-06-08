function generateMonths() {
  const months = [];
  moment.locale(document.documentElement.lang);
  for (let i = 1; i <= 12; i += 1) {
    months.push(moment().add(i, 'months').format('MMM'));
  }
  return months;
}

const contributions = JSON.parse(document.getElementById('contributions_for_year').textContent);

const ctx = document.getElementById('yearActivityChart').getContext('2d');
const config = {
  type: 'bar',
  data: {
    labels: generateMonths(),
    datasets: [
      {
        label: gettext('Commits'),
        data: contributions.commits,
        backgroundColor: 'rgba(87, 173, 219, 0.7)',
      },
      {
        label: gettext('Pull requests'),
        data: contributions.pull_requests,
        backgroundColor: 'rgba(82, 206, 97, 0.7)',
      },
      {
        label: gettext('Issues'),
        data: contributions.issues,
        backgroundColor: 'rgba(226, 113, 90, 0.7)',
      },
      {
        label: gettext('Comments'),
        data: contributions.comments,
        backgroundColor: 'rgba(242, 232, 96, 0.7)',
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    animation: {
      duration: 0,
    },
    scales: {
      xAxes: [{
        stacked: true,
      }],
      yAxes: [{
        stacked: true,
      }],
    },
  },
};
const yearActivityChart = new Chart(ctx, config);
