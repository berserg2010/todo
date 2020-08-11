<template>
  <div class="container">
    <main>
      <SignForm />
    </main>
  </div>
</template>

<script>
import SignForm from '~/components/auth/SignForm'

export default {
  name: 'AuthPage',
  components: {
    SignForm,
  },
  layout: 'Public',
  middleware: ['check-auth', 'auth'],
}
</script>

<style scoped>
</style>
