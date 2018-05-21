export function sortByID(a, b) {
  return a.id - b.id
}

export function removeByValue(arr, val) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].id === val) {
      arr.splice(i, 1)
      break
    }
  }
}

export function convertData(oldData) {
  const newData = []
  oldData.forEach((item, index) => {
    newData.push({
      key: index,
      label: item.value,
      seq: item.value.split(' ')[0]
    })
  })
  return newData
}

export function matchID(arr, id) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].id === id) {
      return arr[i]
    }
  }
}