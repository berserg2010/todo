<template>
  <tr>
    <td>
      <nuxt-link :to="{ path: `/${ event.id }` }">
        {{ event.title }}
      </nuxt-link>
    </td>
    <td>{{ event.description }}</td>
    <td>{{ event.event_date | date }}</td>
    <td>{{ convertingBooleanValue(event.in_archive) }}</td>
    <td>{{ convertingBooleanValue(event.to_repeat) }}</td>
    <td>
      <button type="button" @click="onDelete">
        Delete
      </button>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'EventItem',
  props: {
    event: {
      type: Object,
      require: false,
      default: () => {} //!
    }
  },
  data() {
    return {
      eventData: this.event
    }
  },
  methods: {
    onDelete() {
      this.$emit('delete', this.eventData)
    },
    convertingBooleanValue(value) {
      return value ? 'Yes' : 'No'
    }
  }
}
</script>

<style scoped>

</style>
