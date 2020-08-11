export default ({ store, req, res }) => {
  store.dispatch('initAuth', req)
}
