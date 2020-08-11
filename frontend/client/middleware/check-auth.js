export default ({ store, req }) => {
  store.dispatch('initAuth', req)
}
