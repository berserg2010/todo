<template>
  <EventDetail @submit="onSubmitted" />
</template>

<script>
import EventDetail from '~/components/event/EventDetail'

export default {
  components: {
    EventDetail
  },
  middleware: ['check-auth', 'auth'],
  methods: {
    onSubmitted(eventData) {
      this.$store.dispatch('addEvent', eventData)
        .then(() => {
          this.$router.push('/')
        })
    }
  }
}
</script>

<style>

</style>
