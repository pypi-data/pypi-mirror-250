import random
import time

from snqueue.service import SnQueueService

sqs_url = "https://sqs.us-east-1.amazonaws.com/284584416663/service_test"

def task(
    message: str,
    _: SnQueueService
) -> int:
  print("Processing message:")
  print(message)
  wait_seconds = random.randint(2, 5)
  time.sleep(wait_seconds)
  print(f"Done in {wait_seconds} seconds.")
  print(message)
  return wait_seconds

if __name__ == "__main__":
  service = SnQueueService("test", "terminus-dev", task, MaxNumberOfMessages=5, MaxWorkers=2)
  print(service._config)
  service.listen(sqs_url)