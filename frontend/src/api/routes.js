import http from './http'

export const routesApi = {
  list: (skip = 0, limit = 20) =>
    http.get('/routes', { params: { skip, limit } }),

  get: (id) => http.get(`/routes/${id}`),

  create: (payload) => http.post('/routes', payload),

  update: (id, payload) => http.patch(`/routes/${id}`, payload),

  remove: (id) => http.delete(`/routes/${id}`),
}

export const optimizeApi = {
  submit: (routeRequestId, profile = 'driving', algorithm = 'osrm_trip') =>
    http.post('/optimize', { route_request_id: routeRequestId, profile, algorithm }),
}

export const jobsApi = {
  list: (skip = 0, limit = 20) =>
    http.get('/jobs', { params: { skip, limit } }),

  get: (id) => http.get(`/jobs/${id}`),
}

export const healthApi = {
  check: () => http.get('/health'),
  checkDb: () => http.get('/health/db'),
  checkOsrm: () => http.get('/health/osrm'),
}
