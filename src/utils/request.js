import axios from 'axios'

// create an axios instance
const service = axios.create({
  baseURL: process.env.BASE_API // api的base_url
})

// request interceptor
service.interceptors.request.use(config => {
  // Do something before request is sent
  config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

export default service
