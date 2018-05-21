import request from '@/utils/request'

export function fetchCmnt(params) {
  return request({
    url: '/api/v1.0/cmnts',
    method: 'get',
    params: params
  })
}

export function deleteCmnt(query) {
  return request({
    url: `/api/v1.0/cmnts/${query}`,
    method: 'delete'
  })
}