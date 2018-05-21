import request from '@/utils/request'

export function fetchUser(params) {
  return request({
    url: '/api/v1.0/users',
    method: 'get',
    params: params
  })
}

export function deleteUser(query) {
  return request({
    url: `/api/v1.0/users/${query}`,
    method: 'delete'
  })
}

export function updateUser(query, data) {
  return request({
    url: `/api/v1.0/users/${query}`,
    method: 'put',
    data
  })
}

export function createUser(data) {
  return request({
    url: '/api/v1.0/users',
    method: 'post',
    data
  })
}