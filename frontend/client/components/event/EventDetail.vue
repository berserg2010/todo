<template>
  <section>
    <h1>Event detail</h1>

    <form @submit.prevent="onCreate">
      <div>
        <label for="title">Title</label>
        <input
          id="title"
          v-model="editedEvent.title"
          type="text"
          name="title"
        />
      </div>

      <div>
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="editedEvent.description"
          name="description"
        ></textarea>
      </div>

      <div>
        <label for="eventDate">Event date</label>
        <input
          id="eventDate"
          v-model="editedEvent.event_date"
          type="datetime-local"
          name="eventDate"
          placeholder="YYYY-MM-DD hh:mm"
        />
      </div>

      <div>
        <label for="inArchive">In archive</label>
        <input
          id="inArchive"
          v-model="editedEvent.in_archive"
          type="checkbox"
          name="inArchive"
        />
      </div>

      <div>
        <label for="toRepeat">To repeat</label>
        <input
          id="toRepeat"
          v-model="editedEvent.to_repeat"
          type="checkbox"
          name="toRepeat"
        />
      </div>

      <button type="submit">
        Submit
      </button>
      <button type="button" @click="onCancel">
        Cancel
      </button>
      <button v-if="!isNewEvent" type="button" @click="onDelete">
        Delete
      </button>
    </form>
  </section>
</template>

<script>
export default {
  name: 'EventDetail',
  props: {
    event: {
      type: Object,
      require: false,
      default: () => {} //!
    }
  },
  data() {
    return {
      editedEvent: this.event
        ? { ...this.event }
        : {
          title: '',
          description: '',
          event_date: '',
          in_archive: false,
          to_repeat: false,
        }
    }
  },
  computed: {
    isNewEvent() {
      return this.$route.name === 'new-event'
    }
  },
  methods: {
    onCreate() {
      this.$emit('submit', this.editedEvent)
    },
    onCancel() {
      this.$router.push('/')
    },
    onDelete() {
      this.$emit('delete', this.editedEvent)
    }
  },
}
</script>

<style lang="scss" scoped>

</style>
