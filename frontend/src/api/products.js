import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export function searchProducts({ q = '', page = 1, page_size = 20, grade = '', category = '', country = '' } = {}) {
  return api.get('/products/search', {
    params: { q, page, page_size, grade, category, country },
  }).then(r => r.data)
}

export function getProduct(barcode) {
  return api.get(`/products/${barcode}`).then(r => r.data)
}
