
'''
Target Manager Application
'''

import view.MainView as mv
import client.KeepAlive as ka
import server.TargetSimulator as ts
from threading import Thread

## Utility methods


## MAIN APP
if __name__ == "__main__":
    
    app = mv.GUI() 

    sim_target = ts.TargetSimulator("localhost", 5005) 
    sim_target.start()

    loc_client = ka.KeepAlive("localhost", 5005, "Hello Worldlings!")
    loc_client.start()

    app.mainloop()

    
