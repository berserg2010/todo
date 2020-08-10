import Vuex from 'vuex'
import Cookie from 'js-cookie'

const createStore = () => {
  return new Vuex.Store({
    state: {
      loadedEvents: [],
      token: null
    },
    mutations: {
      setEvents(state, listEvents) {
        state.loadedEvents = listEvents
      },
      addEvent(state, eventToAdd) {
        state.loadedEvents.push(eventToAdd)
      },
      editEvent(state, eventToEdit) {
        const eventIndex = state.loadedEvents.findIndex(
          event => event.id === eventToEdit.id
        )
        state.loadedEvents[eventIndex] = eventToEdit
      },
      deleteEvent(state, eventToDelete) {
        const eventIndex = state.loadedEvents.findIndex(
          event => event.id === eventToDelete.id
        )
        state.loadedEvents = state.loadedEvents.splice(eventIndex)
      },
      setToken(state, token) {
        state.token = token
      },
      clearToken(state) {
        state.token = null
      },
      setDefaultState(state) {
        state.loadedEvents = []
        state.token = null
      },
    },
    actions: {
      setEvents({ commit }, events) {
        commit('setEvents', events)
      },
      addEvent({ commit }, event) {
        this.$axios.setHeader('Authorization', `Token ${this.state.token}`)
        return this.$axios.$post('/events/', event)
          .then((data) => {
            commit('addEvent', { ...data })
          })
          .catch(e => console.error(e))
      },
      editEvent({ commit }, event) {
        this.$axios.setHeader('Authorization', `Token ${this.state.token}`)
        return this.$axios.$put(`/events/${event.id}/`, event)
          .then((res) => {
            commit('editEvent', event)
          })
          .catch(e => console.error(e))
      },
      deleteEvent({ commit }, event) {
        this.$axios.setHeader('Authorization', `Token ${this.state.token}`)
        return this.$axios.$delete(`/events/${event.id}/`, event)
          .then((res) => {
            commit('deleteEvent', event)
          })
          .catch(e => console.error(e))
      },
      async authenticateUser({ commit, dispatch }, authData) {
        let authUrl, data
        if (authData.isLoginPage) {
          authUrl = '/auth/token/login/'
          data = {
            username: authData.username,
            password: authData.password,
          }
        } else {
          authUrl = '/auth/users/'
          data = {
            username: authData.username,
            email: authData.email,
            password: authData.password,
          }
        }
        return await this.$axios.$post(authUrl, data)
          .then((res) => {
            commit('setDefaultState')
            commit('setToken', res.auth_token)
            localStorage.setItem('token', res.auth_token)
            Cookie.set('jwt', res.auth_token)
          })
          .catch((e) => {
            commit('setDefaultState')
            console.error(e)
          })
      },
      initAuth({ commit, dispatch }, req) {
        let token
        if (req) {
          if (!req.headers.cookie) {
            return
          }
          const jwtCookie = req.headers.cookie
            .split('')
            .find(c => c.trim().startsWith('jwt='))
          if (!jwtCookie) {
            return
          }
          token = jwtCookie.split('=')[1]
        } else if (process.client) {
          token = localStorage.getItem('token')
        }
        if (!token) {
          console.info('No token or invalid token')
          dispatch('clearCache')
          return
        }
        commit('setToken', token)
      },
      logout({ commit, dispatch }) {
        this.$axios.setHeader('Authorization', `Token ${this.state.token}`)
        this.$axios.$post('/auth/token/logout/')
          .then(res => console.info('Logout'))
          .catch(e => console.error(e))
        dispatch('clearCache')
        commit('setDefaultState')
      },
      clearCache({ commit }) {
        commit('clearToken')
        Cookie.remove('jwt')
        if (process.client) {
          localStorage.removeItem('token')
        }
      }
    },
    getters: {
      loadedEvents(state) {
        return state.loadedEvents
      },
      getEvent: state => (idEvent) => {
        const eventIndex = state.loadedEvents.findIndex(
          event => event.id === idEvent
        )
        return state.loadedEvents[eventIndex]
      },
      isAuthenticated(state) {
        return state.token != null
      },
    }
  })
}

export default createStore
