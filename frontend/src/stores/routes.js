import { defineStore } from 'pinia'
import { ref } from 'vue'
import { routesApi } from '@/api/routes'

export const useRoutesStore = defineStore('routes', () => {
  const routes = ref([])
  const currentRoute = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchRoutes(skip = 0, limit = 20) {
    loading.value = true
    error.value = null
    try {
      routes.value = await routesApi.list(skip, limit)
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchRoute(id) {
    loading.value = true
    try {
      currentRoute.value = await routesApi.get(id)
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createRoute(payload) {
    const created = await routesApi.create(payload)
    routes.value.unshift(created)
    return created
  }

  async function deleteRoute(id) {
    await routesApi.remove(id)
    routes.value = routes.value.filter(r => r.id !== id)
  }

  return { routes, currentRoute, loading, error, fetchRoutes, fetchRoute, createRoute, deleteRoute }
})
