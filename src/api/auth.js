import request from '@/utils/request'

export function authLogin(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}