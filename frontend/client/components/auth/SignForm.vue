<template>
  <section>
    <h1>{{ isLoginPage ? "Sign in" : "Sign up" }}</h1>

    <form @submit.prevent="onSubmit">
      <label for="text">Nickname</label>
      <input
        id="username"
        v-model="username"
        type="text"
        name="username"
        autoFocus
      />

      <label v-if="!isLoginPage" for="email">Email Address</label>
      <input
        v-if="!isLoginPage"
        id="email"
        v-model="email"
        type="email"
        name="email"
      />

      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        type="password"
        name="password"
      />

      <button type="submit">
        Submit
      </button>

      <button type="button" @click="toggle">
        {{ isLoginPage ? "Sign up" : "Sign in" }}
      </button>
    </form>
  </section>
</template>

<script>
export default {
  name: 'SignForm',
  data() {
    return {
      isLoginPage: true,
      username: '',
      email: '',
      password: '',
    }
  },
  methods: {
    onSubmit() {
      this.$store.dispatch('authenticateUser', {
        isLoginPage: this.isLoginPage,
        username: this.username,
        email: this.email,
        password: this.password,
      })
    },
    toggle() {
      this.isLoginPage = !this.isLoginPage
    },
  }
}
</script>

<style scoped>
</style>
