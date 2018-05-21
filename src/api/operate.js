import request from '@/utils/request'

export function fetchOperate(params) {
  return request({
    url: '/api/v1.0/opers',
    method: 'get',
    params: params
  })
}

export function createOperate(data) {
  return request({
    url: '/api/v1.0/opers',
    method: 'post',
    data
  })
}