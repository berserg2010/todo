export default ({ store, route, redirect }) => {
  const isAuthenticated = store.getters.isAuthenticated
  const isAuthPage = route.name === 'auth'
  if (!isAuthenticated && isAuthPage) {
    return null
  } else if (isAuthenticated && isAuthPage) {
    redirect('/')
  } else if (!isAuthenticated && !isAuthPage) {
    redirect('/auth')
  }
}
