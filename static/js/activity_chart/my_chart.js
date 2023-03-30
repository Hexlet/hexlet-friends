function generateMonths() {
  const months = [];
  moment.locale(document.documentElement.lang);
  for (let i = 1; i <= 12; i += 1) {
    months.push(moment().add(i, 'months').format('MMM'));
  }
  return months;
}

const my_contributions = JSON.parse(document.getElementById('my_contributions_for_year').textContent);
const my_ctx = document.getElementById('my_yearActivityChart').getContext('2d');
const my_config = {
  type: 'bar',
  data: {
    labels: generateMonths(),
    datasets: [
      {
        label: gettext('Commits'),
        data: my_contributions.commits,
        backgroundColor: 'rgba(87, 173, 219, 0.7)',
      },
      {
        label: gettext('Pull requests'),
        data: my_contributions.pull_requests,
        backgroundColor: 'rgba(82, 206, 97, 0.7)',
      },
      {
        label: gettext('Issues'),
        data: my_contributions.issues,
        backgroundColor: 'rgba(226, 113, 90, 0.7)',
      },
      {
        label: gettext('Comments'),
        data: my_contributions.comments,
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
const my_yearActivityChart = new Chart(my_ctx, my_config);
