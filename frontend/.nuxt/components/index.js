export { default as PageHeader } from '../../components/PageHeader.vue'
export { default as SignForm } from '../../components/auth/SignForm.vue'
export { default as EventDetail } from '../../components/event/EventDetail.vue'
export { default as EventItem } from '../../components/event/EventItem.vue'
export { default as ListEvents } from '../../components/event/ListEvents.vue'

export const LazyPageHeader = import('../../components/PageHeader.vue' /* webpackChunkName: "components/PageHeader" */).then(c => c.default || c)
export const LazySignForm = import('../../components/auth/SignForm.vue' /* webpackChunkName: "components/auth/SignForm" */).then(c => c.default || c)
export const LazyEventDetail = import('../../components/event/EventDetail.vue' /* webpackChunkName: "components/event/EventDetail" */).then(c => c.default || c)
export const LazyEventItem = import('../../components/event/EventItem.vue' /* webpackChunkName: "components/event/EventItem" */).then(c => c.default || c)
export const LazyListEvents = import('../../components/event/ListEvents.vue' /* webpackChunkName: "components/event/ListEvents" */).then(c => c.default || c)
