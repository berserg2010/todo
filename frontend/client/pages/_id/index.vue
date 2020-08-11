<template>
  <EventDetail :event="event" @submit="onSubmitted" @delete="onDeleted" />
</template>

<script>
import EventDetail from '~/components/event/EventDetail'

export default {
  components: {
    EventDetail
  },
  middleware: ['check-auth', 'auth'],
  computed: {
    event() {
      return this.$store.getters.getEvent(+this.$route.params.id)
    }
  },
  methods: {
    onSubmitted(eventData) {
      this.$store.dispatch('editEvent', eventData)
        .then(() => {
          this.$router.push('/')
        })
    },
    onDeleted(eventData) {
      this.$store.dispatch('deleteEvent', eventData)
        .then(() => {
          this.$router.push('/')
        })
    },
  },
  validate({ params }) {
    // Must be a number
    return /^\d+$/.test(params.id)
  },
}
</script>

<style>

</style>
