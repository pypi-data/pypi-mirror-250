import airgen

c: airgen.MultirotorClient = airgen.client.connect_airgen('multirotor')
c.enableApiControl(True)
c.takeoffAsync().join() 