export function sortByLabel(a, b) {
  return a.value - b.value
}

export function removeByValue(arr, val) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].value === val) {
      arr.splice(i, 1)
      break
    }
  }
}
