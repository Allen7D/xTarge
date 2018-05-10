import request from '@/utils/request'

export function fetchAlert() {
  return request({
    url: '/api/v1.0/alerts',
    method: 'get'
  })
}

export function deleteAlert(query) {
  return request({
    url: `/api/v1.0/alerts/${query}`,
    method: 'delete'
  })
}