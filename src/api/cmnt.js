import request from '@/utils/request'

export function fetchCmnt() {
  return request({
    url: '/api/v1.0/users',
    method: 'get'
  })
}

export function deleteCmnt(query) {
  return request({
    url: `/api/v1.0/users/${query}`,
    method: 'delete'
  })
}