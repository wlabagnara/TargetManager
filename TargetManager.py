
'''
Target Manager Application
'''

import view.MainView as mv
import client.KeepAlive as ka
import server.TargetSimulator as ts

## MAIN APP
if __name__ == "__main__":
    
    sim_target = ts.TargetSimulator("localhost", 5005) 
    loc_client = ka.KeepAlive("localhost", 5005, "Hello Worldlings!")
    
    app = mv.GUI(loc_client, sim_target) 

    app.mainloop()

    
