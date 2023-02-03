function MakeCompare(val){

  const fields ={
    'cit':'commits',
    'cit-add':'additions',
    'cit-del':'deletions',
    'pr':'pull_requests',
    'iss':'issues',
    'cnt':'comments',
  }

  if (val === -1) {
    for (const key in fields) {
      $('#contributor_' + key).html('');
      $('#own-' + key).removeClass();
    }
  } else {
    const json_data = $.parseJSON($('#contributors_data').text());
    const result = json_data.filter(el => {
      return el.id == val
    })[0];
    for (const key in fields) {
      $('#contributor_' + key).html(result[fields[key]]);
      ColoringField($('#own-'+key),result[fields[key]])
    }
  }
}

function  ColoringField(field, value){
  field.removeClass()
  if (parseInt(field.text()) > value) {
    field.addClass('bg-success')
  } else {
    if (parseInt(field.text()) === value) {
      field.addClass('bg-warning')
    } else {
      field.addClass('bg-danger')
    }
  }
}
