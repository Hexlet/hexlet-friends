function ColoringField(field, value) {
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
