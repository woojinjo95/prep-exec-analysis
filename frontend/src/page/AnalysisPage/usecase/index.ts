import API from '@global/api'

export const prefetchVideoFile = async (
  url: string,
  fetchedCallback: (url: string) => void,
  progressCallback?: (progress: number) => void,
  errorCallback?: (err: unknown) => void,
) => {
  let prev_progress = 0

  try {
    const response = await API.get<MediaSource>(url, {
      responseType: 'blob',
      onDownloadProgress: (progressEvent) => {
        if (!progressEvent.total) return
        const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100)
        if (progress !== prev_progress) {
          prev_progress = progress
          progressCallback?.(progress)
        }
      },
    })

    const blob_url = URL.createObjectURL(response.data)
    fetchedCallback(blob_url)
  } catch (err) {
    errorCallback?.(err)
  }
}
