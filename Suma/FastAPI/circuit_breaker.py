failure_count=0
threshold=3
def call_service():
      global failure_count
      if failure_count>=threshold:
        print("circuit open-request blocked")
        return
try:
      print("calling service..")
      raise Exception("service unavailable")
except Exception:
      failure_count+=1
      print("service failed")
      print("failure count:",failure_count)
      if failure_count>=threshold:
        print("circuit is now open")
call_service()#fails
call_service()#fails
call_service()#circuit opens
call_service()#request blocked

