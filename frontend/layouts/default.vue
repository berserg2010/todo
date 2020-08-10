<template>
  <div class="container">
    <PageHeader v-if="$route.name !== 'auth'" />
    <main>
      <Nuxt />
    </main>
  </div>
</template>

<script>
import PageHeader from '~/components/PageHeader'

export default {
  components: {
    PageHeader,
  },
}
</script>

<style>
</style>
