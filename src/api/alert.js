import request from '@/utils/request'

export function fetchAlert(params) {
  return request({
    url: '/api/v1.0/alerts',
    method: 'get',
    params: params
  })
}

export function deleteAlert(query) {
  return request({
    url: `/api/v1.0/alerts/${query}`,
    method: 'delete'
  })
}