import asyncio
import os
import time

from snqueue.utils.file import download

urls = (
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%80%BE%E6%88%91%E4%B8%80%E4%B8%96%EF%BC%8C%E4%B8%8D%E8%B4%9F%E7%9B%B8%E6%80%9D.txt",
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%81%87%E7%88%B1%E7%9C%9F%E5%90%BB%EF%BC%9A%E4%BA%BF%E4%B8%87%E6%80%BB%E8%A3%81%E6%81%8B%E4%B8%8A%E6%88%91-368.txt",
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%85%A5%E9%AA%A8%E6%9A%96%E5%A9%9A%EF%BC%9A%E6%80%BB%E8%A3%81%E5%A5%BD%E5%A5%BD%E7%88%B1-2.txt",
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%87%B0%E5%A6%83%E9%80%86%E5%A4%A9-542.txt",
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%8C%BB%E5%A6%83%E7%8B%AC%E6%AD%A5%E5%A4%A9%E4%B8%8B-359.txt",
  "https://bcnovel.s3.amazonaws.com/original-text/%E6%8E%8C%E9%98%85/%E5%BA%B6%E5%A5%B3%E7%AD%96%EF%BC%9A%E6%AF%92%E5%A6%83%E5%BD%92%E6%9D%A5.txt"
)

dest_dir = os.path.dirname(__file__)

async def main():
  start = time.perf_counter()
  await download(urls, dest_dir, max_workers=3)
  stop = time.perf_counter()
  print(f"It took {stop - start} seconds to download all the files.")

if __name__ == '__main__':
  asyncio.run(main())
