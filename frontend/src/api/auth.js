import http from './http'

export const authApi = {
  /**
   * Login using OAuth2 password flow.
   * Returns { access_token, token_type }
   */
  login(email, password) {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return http.post('/auth/token', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  /**
   * Register a new user account.
   */
  register(email, password, fullName) {
    return http.post('/auth/register', { email, password, full_name: fullName })
  },
}
