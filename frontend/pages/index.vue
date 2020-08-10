<template>
  <ListEvents :list-events="loadedEvents" />
</template>

<script>
import ListEvents from '~/components/event/ListEvents'

export default {
  components: {
    ListEvents,
  },
  middleware: ['check-auth', 'auth'],
  async asyncData(context) {
    context.$axios.setHeader('Authorization', `Token ${context.store.state.token}`)
    return await context.$axios.$get('/events/')
      .then((data) => {
        const eventsArray = []
        for (const key in data) {
          eventsArray.push({ ...data[key] })
        }
        context.store.dispatch('setEvents', eventsArray)
      })
      .catch(e => console.info(e))
  },
  computed: {
    loadedEvents() {
      return this.$store.getters.loadedEvents
    }
  }
}
</script>

<style>
</style>
