import request from '@/utils/request'

export function fetchOperate() {
  return request({
    url: '/api/v1.0/ops',
    method: 'get'
  })
}

export function deleteOperate(query) {
  return request({
    url: `/api/v1.0/ops/${query}`,
    method: 'delete'
  })
}