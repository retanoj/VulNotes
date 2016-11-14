export function auth(request, next) {
  var token = localStorage.getItem('token')
  if (token !== null && token !== 'undefined') {
    request.headers.auth = token
  }

  next((response) => {
    if (response.status === 401) {
      localStorage.removeItem('token')
    }
    if (response.headers && response.headers.auth) {
      localStorage.setItem('token', response.headers.auth)
    }
  })
}

