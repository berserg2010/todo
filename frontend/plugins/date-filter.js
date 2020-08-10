import Vue from 'vue'

const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]

const dateFilter = (value) => {
  return formatDate(value)
}

function formatDate(inputDate) {
  const date = new Date(inputDate)
  const year = date.getFullYear()
  const month = date.getMonth()
  const day = date.getDate()
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const formattedDate = `${day} ${months[month]} ${year} ${hours}:${minutes}`
  return formattedDate
}

Vue.filter('date', dateFilter)
