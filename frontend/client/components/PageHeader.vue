<template>
  <header>
    <button
      v-if="!isNewEvent"
      type="button"
      @click="$router.push('/new-event')"
    >
      Create Event
    </button>

    <button type="button" @click="onLogout">
      Sign out
    </button>
  </header>
</template>

<script>
export default {
  name: 'PageHeader',
  computed: {
    isNewEvent() {
      return this.$route.name === 'new-event'
    },
  },
  methods: {
    onLogout() {
      this.$store.dispatch('logout')
      this.$router.push('/auth')
    }
  }
}
</script>

<style lang="scss">

</style>
