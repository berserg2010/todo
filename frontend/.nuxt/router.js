import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _554c6ce1 = () => interopDefault(import('../pages/auth/index.vue' /* webpackChunkName: "pages/auth/index" */))
const _4a2858ac = () => interopDefault(import('../pages/new-event/index.vue' /* webpackChunkName: "pages/new-event/index" */))
const _a55fa4e8 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))
const _7dffa277 = () => interopDefault(import('../pages/_id/index.vue' /* webpackChunkName: "pages/_id/index" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/auth",
    component: _554c6ce1,
    name: "auth"
  }, {
    path: "/new-event",
    component: _4a2858ac,
    name: "new-event"
  }, {
    path: "/",
    component: _a55fa4e8,
    name: "index"
  }, {
    path: "/:id",
    component: _7dffa277,
    name: "id"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
