<template>
  <section>
    <h1>List Events</h1>
    <div class="search">
      <div class="search_item">
        <label for="search" class="visually-hidden">Search event</label>
        <input v-model="search" type="text" placeholder="Search event" name="search" autocomplete="off" />
      </div>
      <div class="search_item">
        <select v-model="selected">
          <option v-for="option in options" :key="option.key" :value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Event date</th>
          <th>In archive</th>
          <th>To repeat</th>
          <th>Delete?</th>
        </tr>
      </thead>
      <tbody>
        <EventItem
          v-for="event in searchEvent"
          :key="event.id"
          :event="event"
          @delete="onDeleted"
        />
      </tbody>
    </table>
  </section>
</template>

<script>
import EventItem from '~/components/event/EventItem'

export default {
  name: 'ListEvents',
  components: {
    EventItem,
  },
  props: {
    listEvents: {
      type: Array,
      required: true,
      default: () => []
    },
  },
  data() {
    const now = new Date()
    const lastMonth = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000))
    const lastWeek = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
    const lastDay = new Date(now.getTime() - (1 * 24 * 60 * 60 * 1000))
    return {
      events: this.listEvents,
      search: '',
      selected: '',
      options: [
        { text: '---', value: '', key: 1 },
        { text: 'For the month', value: lastMonth, key: 2 },
        { text: 'For the week', value: lastWeek, key: 3 },
        { text: 'For the day', value: lastDay, key: 4 },
      ]
    }
  },
  computed: {
    searchEvent() {
      return this.events.filter((event) => {
        return event.title.toLowerCase()
          .match(this.search.toLowerCase())
      })
        .filter((event) => {
          return new Date(event.event_date) > this.selected
        })
    },
  },
  methods: {
    onDeleted(eventData) {
      const eventIndex = this.events.findIndex(
        event => event.id === eventData.id
      )
      this.events.splice(eventIndex, 1)
      this.$store.dispatch('deleteEvent', eventData)
    },
  }
}
</script>

<style scoped>
</style>
